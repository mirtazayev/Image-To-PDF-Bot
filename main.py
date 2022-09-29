import os

from PIL import Image
from pyrogram import Client, filters

TOKEN = '5623507547:AAFNznFmYB4GjeFZuQDsRTC-Z7GY84ZmtEc'

API_ID = '1234567'  # example

API_HASH = 'AAFNznFmYB4GjeFZuQDsRTC-Z7GY84ZmtEc'  # example
app = Client(
    "pdf",
    bot_token=TOKEN, api_hash=API_HASH,
    api_id=API_ID
)

LIST = {}


@app.on_message(filters.command(['start']))
async def start(client, message):
    await message.reply_text(text=f"""Hello {message.from_user.first_name}I'm 𝐈𝐌𝐀𝐆𝐄 𝐓𝐎 𝐏𝐃𝐅 𝐁𝐎𝐓. 

I can convert Image to PDF.

This bot was created by @PythonDew

If you want to convert more Image to PDF, Send image.
""", reply_to_message_id=message.from_user.id)


@app.on_message(filters.private & filters.photo)
async def pdf(client, message):
    if not isinstance(LIST.get(message.from_user.id), list):
        LIST[message.from_user.id] = []

    file_id = str(message.photo.file_id)
    ms = await message.reply_text("Converting to PDF 🔁......")
    file = await client.download_media(file_id)

    image = Image.open(file)
    img = image.convert('RGB')
    LIST[message.from_user.id].append(img)
    await ms.edit(
        f"Successfully Converted your Image to PDF. If you want to convert more Images to PDF, Send them one by one.\n\n **If your process was over, click here 👉 /convert** ")


@app.on_message(filters.command(['convert']))
async def done(client, message):
    images = LIST.get(message.from_user.id)

    if isinstance(images, list):
        del LIST[message.from_user.id]
    if not images:
        await message.reply_text("No image !!")
        return

    path = f"{message.from_user.first_name}" + ".pdf"
    images[0].save(path, save_all=True, append_images=images[1:])

    await client.send_document(message.from_user.id, open(path, "rb"),
                               caption="Here is your PDF!!\n**PDF Created by: @image2pdfrobot**")
    os.remove(path)


app.run()
