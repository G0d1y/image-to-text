import json
import os
from pyrogram import Client, filters
from PIL import Image
import pytesseract

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

@app.on_message(filters.photo)
async def read_text_from_image(client, message):
    file_path = await message.download()
    
    try:
        image = Image.open(file_path)
        
        extracted_text = pytesseract.image_to_string(image)
        
        await message.reply_text(f"Extracted Text:\n\n{extracted_text}")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hello! Send an image to extract text from it.")

app.run()
