import json
from pyrogram import Client, filters
from PIL import Image
import pytesseract
import os

# Load configuration from the JSON file
with open('config.json') as config_file:
    config = json.load(config_file)

api_id = int(config['api_id'])
api_hash = config['api_hash']
bot_token = config['bot_token']

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Client(
    "bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

@app.on_message(filters.command("read_text") & filters.photo)
async def read_text_from_image(client, message):
    # Download the image
    file_path = await message.download()
    
    try:
        # Open the image and extract text
        image = Image.open(file_path)
        extracted_text = pytesseract.image_to_string(image)
        
        # Send the extracted text back to the user
        await message.reply_text(f"Extracted Text:\n\n{extracted_text}")
    except Exception as e:
        # Handle errors
        await message.reply_text(f"An error occurred while processing the image: {e}")
    finally:
        # Clean up by removing the downloaded image file
        if os.path.exists(file_path):
            os.remove(file_path)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! Send an image with the /read_text command to extract text from it.")

app.run()
