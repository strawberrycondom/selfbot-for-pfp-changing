import discord
import os
import asyncio
import random

TOKEN = 'token'
FOLDER_PATH = 'folder'
CHANGE_INTERVAL = 2400  

client = discord.Client()


images = [f for f in os.listdir(FOLDER_PATH) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

async def change_avatar():
    if not images:
        print("No images found in folder.")
        return None

    image_name = random.choice(images)
    image_path = os.path.join(FOLDER_PATH, image_name)
    with open(image_path, 'rb') as img_file:
        try:
            await client.user.edit(avatar=img_file.read())
            print(f"Changed avatar to {image_name}")
            return image_name
        except Exception as e:
            print(f"Failed to change avatar: {e}")
            return None

async def auto_change_task():
    while True:
        await change_avatar()
        await asyncio.sleep(CHANGE_INTERVAL)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (selfbot)')
    client.loop.create_task(auto_change_task())

@client.event
async def on_message(message):
    if message.author.id != client.user.id:
        return

    if message.content.strip().lower() == '*change':
        image_name = await change_avatar()
        if image_name:
            await message.channel.send(f"Avatar changed to {image_name}")

async def main():
    await client.login(TOKEN)   
    await client.connect()      

asyncio.run(main())
