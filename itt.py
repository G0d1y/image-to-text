import json
import os
from pyrogram import Client, filters
from PIL import Image, ImageEnhance
import pytesseract
import cv2
import numpy as np

with open('config.json') as config_file:
    config = json.load(config_file)

api_id = int(config['api_id'])
api_hash = config['api_hash']
bot_token = config['bot_token']

app = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

def preprocess_image(image_path):
    image = Image.open(image_path)
    
    
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    
    thresholded_image = cv2.adaptiveThreshold(
        gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
    )
    
    
    denoised_image = cv2.fastNlMeansDenoising(thresholded_image, None, 30, 7, 21)
    
    
    denoised_image = Image.fromarray(denoised_image)
    
    
    denoised_image = denoised_image.resize(
        (denoised_image.width * 2, denoised_image.height * 2), Image.Resampling.LANCZOS
    )
    
    return denoised_image

@app.on_message(filters.photo)
async def read_text_from_image(client, message):
    file_path = await message.download()
    
    try:
        processed_image = preprocess_image(file_path)
        
        
        custom_oem_psm_config = r'--oem 3 --psm 6'
        
        
        extracted_text = pytesseract.image_to_string(processed_image, lang='fas', config=custom_oem_psm_config)
        
        if extracted_text.strip():
            await message.reply_text(f"Extracted Text:\n\n{extracted_text}")
        else:
            await message.reply_text("No text detected or text could not be recognized.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text(
        "Hello! Send an image with Persian text to extract it."
    )

app.run()
