import discord
from discord.ext import commands
import requests
from dotenv import load_dotenv
from PIL import Image
import os
import asyncio

discord_token = "YOUR_DISCORD_TOKEN_HERE"

load_dotenv()
client = commands.Bot(command_prefix="*", intents=discord.Intents.all())
directory = os.getcwd()
print(directory)

async def download_image(url, filename, message):
    response = requests.get(url)
    if response.status_code == 200:

        # Define the input and output folder paths
        input_folder = "input"
        output_folder = "output"

        # Check if the output folder exists, and create it if necessary
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Check if the input folder exists, and create it if necessary
        if not os.path.exists(input_folder):
            os.makedirs(input_folder)
        with open(f"{directory}/{input_folder}/{filename}", "wb") as f:
            f.write(response.content)
        print(f"Image downloaded: {filename}")
        input_file = os.path.join(input_folder, filename)

        if "Image #" not in filename:
            file_prefix = os.path.splitext(filename)[0]
            # Split the image
            split_image(input_file, file_prefix)
            #top_left, top_right, bottom_left, bottom_right = split_image(input_file)
            # Save the output images with dynamic names in the output folder
            #top_left.save(os.path.join(output_folder, file_prefix + "_0.png"))
            #top_right.save(os.path.join(output_folder, file_prefix + "_1.png"))
            #bottom_left.save(os.path.join(output_folder, file_prefix + "_2.png"))
            #bottom_right.save(os.path.join(output_folder, file_prefix + "_3.png"))
        else:
            os.rename(f"{directory}/{input_folder}/{filename}", f"{directory}/{output_folder}/{filename}")
        # Delete the input file
        os.remove(f"{directory}/{input_folder}/{filename}")
      
def split_image(image_file, file_prefix):
    with Image.open(image_file) as im:
        # Get the width and height of the original image
        width, height = im.size
        # Calculate the middle points along the horizontal and vertical axes
        mid_x = width // 2
        mid_y = height // 2
        # Split the image into four equal parts
        top_left = im.crop((0, 0, mid_x, mid_y))
        top_right = im.crop((mid_x, 0, width, mid_y))
        bottom_left = im.crop((0, mid_y, mid_x, height))
        bottom_right = im.crop((mid_x, mid_y, width, height))
        
        # Save the output images with dynamic names
        top_left.save(f"{file_prefix}_0.png")
        top_right.save(f"{file_prefix}_1.png")
        bottom_left.save(f"{file_prefix}_2.png")
        bottom_right.save(f"{file_prefix}_3.png")
        
        # return top_left, top_right, bottom_left, bottom_right

async def handle_special_image(input_file, output_folder, filename):     
    os.rename(input_file, os.path.join(output_folder, filename))

@client.event
async def on_ready():
    print("Bot connected")
    
@client.event
async def on_message(message):
    print(message.content)
    
    # Determine the output folder based on the channel's ID
    # The folder has format channelname_uniqueid this is due to perhaps channel naming across servers
    output_folder = f"output_{message.channel.name}_{message.channel.id}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for attachment in message.attachments:
        if "Upscaled by" in message.content or "Upscaled (2x) by" in message.content or "Upscaled (4x) by" in message.content:
            try:
                response = requests.get(attachment.url)
                if response.status_code == 200:
                    output_folder = f"output_{message.channel.name}_{message.channel.id}"
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                     # Add "-upscale" to the filename before the extension
                    filename = os.path.splitext(attachment.filename)[0] + "-upscale" + os.path.splitext(attachment.filename)[1]
                    with open(os.path.join(output_folder, filename), "wb") as f:
                        f.write(response.content)
            
                    # Call download_image with the message parameter
                    await download_image(attachment.url, filename, message)
                    await message.channel.send("done")
                                
            except Exception as e:
                print(f"Error saving upscaled image: {e}")
                await asyncio.sleep(10)
                continue
    
        # exit the loop
        # return
        
        if "Image #" in message.content and attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            try:
                response = requests.get(attachment.url)
                if response.status_code == 200:
                    output_folder = f"output_{message.channel.name}_{message.channel.id}"
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    with open(os.path.join(output_folder, attachment.filename), "wb") as f:
                        f.write(response.content)
                    
                    # Call download_image with the message parameter
                    await download_image(attachment.url, attachment.filename, message)
                    await message.channel.send("done")
                                            
            except:
                await asyncio.sleep(10)
                continue
                
        elif attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
            try:
                response = requests.get(attachment.url)
                if response.status_code == 200:
                    input_folder = "input"
                    output_folder = f"output_{message.channel.name}_{message.channel.id}"
                    if not os.path.exists(input_folder):
                        os.makedirs(input_folder)
                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                    with open(f"{directory}/{input_folder}/{attachment.filename}", "wb") as f:
                        f.write(response.content)
                    print(f"Image downloaded: {attachment.filename}")
                    await message.channel.send("done")
                    input_file = os.path.join(input_folder, attachment.filename)
                    file_prefix = os.path.splitext(attachment.filename)[0]
                    top_left, top_right, bottom_left, bottom_right = split_image(input_file)
                    top_left.save(os.path.join(output_folder, file_prefix + "_0.png"))
                    top_right.save(os.path.join(output_folder, file_prefix + "_1.png"))
                    bottom_left.save(os.path.join(output_folder, file_prefix + "_2.png"))
                    bottom_right.save(os.path.join(output_folder, file_prefix + "_3.png"))
                    os.remove(f"{directory}/{input_folder}/{attachment.filename}")
                    
                    # Call download_image with the message parameter
                    await download_image(attachment.url, attachment.filename, message)
                    # await message.channel.send("done")
                                        
            except:
                await asyncio.sleep(10)
                continue
                
            # Save the message content as a text file
            if attachment.filename.lower().endswith((".png", ".jpg", ".jpeg", ".gif")):
                try:
                    # Create a folder to store text files if it doesn't exist
                    text_folder = "message_text"
                    if not os.path.exists(text_folder):
                        os.makedirs(text_folder)

                    # Save the message content to a text file
                    message_text = message.content
                    text_filename = f"{attachment.filename}.txt"
                    with open(os.path.join(text_folder, text_filename), "w", encoding="utf-8") as text_file:
                        text_file.write(message_text)
                except Exception as e:
                    print(f"Error saving message text: {e}")
                    
client.run(discord_token)
