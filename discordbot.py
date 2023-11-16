from lambda_handler import get_voice_from_text
import discord

import json
import asyncio

import json
import asyncio
import requests

print(discord.__file__)
from discord.ext import commands
import requests


from interactions import Button, ActionRow
from moralis import evm_api

images = [
    "https://github.com/OpenTalker/SadTalker/blob/main/examples/source_image/art_0.png?raw=true",
    "https://github.com/OpenTalker/SadTalker/blob/main/examples/source_image/art_10.png?raw=true",
    "https://github.com/OpenTalker/SadTalker/blob/main/examples/source_image/art_2.png?raw=true",
    "https://github.com/OpenTalker/SadTalker/blob/main/examples/source_image/art_9.png?raw=true",
]
names = [
    "Sir Wigglesworth",
    "Captain Fluffington",
    "Miss Purrfect",
    "Lord Whiskerstein",
]


selected_voices = {}  # Store users' voice selections
selected_nfts = {}  # Store users' voice selections
data = {}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Necessary to interact with member data

bot = commands.Bot(
    command_prefix="!", intents=intents
)  # Replace 'YOUR_BOT_TOKEN_HERE' with your bot's token
import random


class VoiceButton(discord.ui.Button):
    def __init__(self, label, custom_id):
        super().__init__(
            style=discord.ButtonStyle.primary, label=label, custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        # Here, you can handle what happens when the button is clicked.
        print("selected:", interaction.user.id)
        selected_voices[interaction.user.id] = self.custom_id
        await interaction.response.send_message(f"You selected {self.label}")


class VoiceSelectionView(discord.ui.View):
    def __init__(self, voices):
        super().__init__()
        # Choose 5 random voices
        selected_voices = random.sample(voices, 5)
        for voice in selected_voices:
            button = VoiceButton(label=voice["name"], custom_id=voice["voice_id"])
            self.add_item(button)


def download_video(video_url, save_path):
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    with open(save_path, "wb") as video_file:
        for chunk in response.iter_content(chunk_size=8192):
            video_file.write(chunk)


from moviepy.editor import VideoFileClip


def crop_video(video_path, output_path, crop_bottom=20):
    """
    Crop the video from the bottom by the specified amount.
    The crop_bottom parameter is in pixels.
    """
    with VideoFileClip(video_path) as clip:
        cropped_clip = clip.crop(y2=clip.size[1] - crop_bottom)  # crop from the bottom
        cropped_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")


from discord import File


async def generate_video(ctx, text, image):
    did_key = "c2hpdmFtYXR1Y3dAZ21haWwuY29t:0cWFt9EkSQ9O47aIDwfOB"

    url = "https://api.d-id.com/talks"

    payload = {
        "source_url": image,
        "script": {"type": "text", "input": text},
    }
    payload = {
        "script": {
            "type": "text",
            "subtitles": "false",
            "provider": {
                "type": "elevenlabs",
                "voice_id": selected_voices[ctx.message.author.id],
            },
            "ssml": "false",
            "input": text,
        },
        "config": {"fluent": "false", "pad_audio": "0.0"},
        "source_url": image,
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jeF9sb2dpY19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfY3VzdG9tZXJfaWQiOiJjdXNfT2k2VjdrZ1BrWkpINU0iLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDcyMDY4NTU1MDYwMTE0NTA0ODQiLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTU3NTQwNjMsImV4cCI6MTY5NTg0MDQ2MywiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHJlYWQ6Y3VycmVudF91c2VyIHVwZGF0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgb2ZmbGluZV9hY2Nlc3MifQ.aV-yOzZAgz6r5FK0Su9d4l0Ughj8JzDbho8oGFNzz7NM56UR17RJgtW4eO9zFaWIJB_eNNaDah6DTJAtsGf8SFDmqUAPQzhB7-g8lcLwwsf8vP5QaMoNn71ij4Z_4bN7NkqzX9tnvc-XgMkuj43xij98B-U-eHz252SLjrgqoU0j_3uAsWijOsrj1-OI4F79GIvsSF8xmPGauiCiuI1wtAvNEV7kvTTHS7RUwoWoITR3nupp0FRSrIXiOeeCGE7WLRByAJeZfGdmvWa9J4j56_j4vP4EdcJBALyHIjEXwFv_YG8ElpdIJNyaoY_GK3o8jpDaA3AIdKbfs9ZZ3I9NeQ",
    }

    response_clip = requests.post(url, json=payload, headers=headers)
    print(response_clip.text, type(response_clip.text))

    while True:
        url = "https://api.d-id.com/talks/" + json.loads(response_clip.text).get("id")

        headers = {
            "accept": "application/json",
            "authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik53ek53TmV1R3ptcFZTQjNVZ0J4ZyJ9.eyJodHRwczovL2QtaWQuY29tL2ZlYXR1cmVzIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9jeF9sb2dpY19pZCI6IiIsImh0dHBzOi8vZC1pZC5jb20vY2hhdF9zdHJpcGVfc3Vic2NyaXB0aW9uX2lkIjoiIiwiaHR0cHM6Ly9kLWlkLmNvbS9zdHJpcGVfY3VzdG9tZXJfaWQiOiJjdXNfT2k2VjdrZ1BrWkpINU0iLCJpc3MiOiJodHRwczovL2F1dGguZC1pZC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDcyMDY4NTU1MDYwMTE0NTA0ODQiLCJhdWQiOlsiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS9hcGkvdjIvIiwiaHR0cHM6Ly9kLWlkLnVzLmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2OTU3NTQwNjMsImV4cCI6MTY5NTg0MDQ2MywiYXpwIjoiR3pyTkkxT3JlOUZNM0VlRFJmM20zejNUU3cwSmxSWXEiLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIHJlYWQ6Y3VycmVudF91c2VyIHVwZGF0ZTpjdXJyZW50X3VzZXJfbWV0YWRhdGEgb2ZmbGluZV9hY2Nlc3MifQ.aV-yOzZAgz6r5FK0Su9d4l0Ughj8JzDbho8oGFNzz7NM56UR17RJgtW4eO9zFaWIJB_eNNaDah6DTJAtsGf8SFDmqUAPQzhB7-g8lcLwwsf8vP5QaMoNn71ij4Z_4bN7NkqzX9tnvc-XgMkuj43xij98B-U-eHz252SLjrgqoU0j_3uAsWijOsrj1-OI4F79GIvsSF8xmPGauiCiuI1wtAvNEV7kvTTHS7RUwoWoITR3nupp0FRSrIXiOeeCGE7WLRByAJeZfGdmvWa9J4j56_j4vP4EdcJBALyHIjEXwFv_YG8ElpdIJNyaoY_GK3o8jpDaA3AIdKbfs9ZZ3I9NeQ",
        }

        response = requests.get(url, headers=headers)

        print(response.text)
        if json.loads(response.text).get("status") == "done":
            print(response.text, type(response.text))
            video_url = json.loads(response.text).get("result_url")
            download_video(video_url, "downloaded_video.mp4")
            crop_video(
                "downloaded_video.mp4", "cropped_video.mp4", crop_bottom=120
            )  # You'll need to
            await ctx.send(file=File("cropped_video.mp4"))
            break

        await asyncio.sleep(30)  # Sleep for 30 seconds before the next poll


@bot.command(name="create", description="Test")
async def get_voices_command_func(ctx, arg):
    print(ctx.message.author)
    print(
        data[ctx.message.author.id].get("image"),
        data[ctx.message.author.id].get("name"),
    )
    await generate_video(ctx, arg, data[ctx.message.author.id].get("image"))


class NFTButton(discord.ui.Button):
    def __init__(self, label, custom_id):
        super().__init__(
            style=discord.ButtonStyle.primary, label=label, custom_id=custom_id
        )

    async def callback(self, interaction: discord.Interaction):
        # Here, you can handle what happens when the button is clicked.
        selected_nfts[interaction.user.id] = self.custom_id

        data[interaction.user.id] = {
            "image": images[names.index((self.custom_id)) - 1],
            "name": self.custom_id,
        }
        print("Data: ", data)

        await interaction.response.send_message(
            f"{interaction.user.name} selected {self.label}"
        )


class ImageSelectionView(discord.ui.View):
    def __init__(self, images, names):
        super().__init__()
        # Assuming your images are a list of URLs
        for image, name in zip(images, names):
            button = NFTButton(
                label=name, custom_id=name
            )  # You can modify the label if needed
            self.add_item(button)


def get_voices():
    import requests

    url = "https://eynswly4yk.execute-api.us-west-1.amazonaws.com/testing/api/voices"

    response = requests.post(url)

    print(response.status_code)
    print(response.text)
    return response.text


@bot.command(name="select", description="Test")
async def get_voices_command_func(ctx):
    voices = json.loads(get_voices()).get("voices")
    print("voices: ", voices)

    voice_list = [
        "piTKgcLEGmPE4e6mEKli",
    ]

    # Make sure there are at least 5 voices to choose from
    if len(voices) < 5:
        await ctx.send("Not enough voices to display!")
        return

    view = VoiceSelectionView(voices)

    await ctx.send(content="Select a voice:", view=view)


@bot.command(name="image", descrription="Test")
async def test(ctx, arg=""):
    # Create a view with the image buttons
    view = ImageSelectionView(images, names)

    await ctx.send(content="Select an Image:", view=view)


@bot.command(name="voice", descrription="Test")
async def test(ctx, arg):
    # Check if the message is from the channel where the webhook posts messages
    print(ctx.message)
    print(ctx.message.author)

    print("VOICE ID: ", {selected_voices[ctx.message.author.id]})
    get_voice_from_text(f"{selected_voices[ctx.message.author.id]}", arg)
    print(f"Received a message from {ctx.message.author}: {arg}")
    embed = discord.Embed(
        title="Audio File",
        description="Here's your requested audio!",
        color=discord.Color.blue(),
    )

    # embed.set_thumbnail(url="https://cdn-longterm.mee6.xyz/plugins/embeds/images/1154540675048673390/5455d84d111e0a96fa7ace552012720eab3e299935ace9f7127591ef2f5ebe78.png")
    avatar_url = ctx.message.author.avatar.url  # Get the user's avatar URL
    embed.set_thumbnail(url=avatar_url)

    embed.set_footer(text=f"Requested by {ctx.message.author.name}")

    await ctx.send(embed=embed, file=discord.File(f"{arg}.mp3"))


from discord.ext import commands
from discord.utils import get


@bot.command(name="remove_unverified")
@commands.has_permissions(
    administrator=True
)  # Ensure only administrators can use this command
async def remove_unverified(ctx):
    members = []
    async for member in ctx.guild.fetch_members(limit=2000):  # Fetch in chunks of 1000
        members.append(member)

    roles_of_members = {}
    for member in members:
        role_names = [
            role.name for role in member.roles
        ]  # Exclude the default @everyone role
        role_names_str = ", ".join(role_names) if role_names else "None"
        print(f"{member.name}: {role_names_str}")
        roles_of_members[member] = role_names_str

    print("*" * 50)
    count = 0
    for member, role in roles_of_members.items():
        if "Verified" not in role and member.bot == False:
            print(f"Removing {member.name}")
            await member.kick(reason="Not verified")  # Kick the member
            count += 1

    await ctx.send(f"Total members kicked: {count}")


import pandas as pd


@bot.command(name="export")
async def export_members(ctx):
    member_data = []
    async for member in ctx.guild.fetch_members(limit=None):
        member_info = {
            "Name": member.name,
            "Discriminator": member.discriminator,
            "ID": member.id,
            "Creation Date": member.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
        member_data.append(member_info)

    df = pd.DataFrame(member_data)
    df.to_csv("members_creation_date.csv", index=False)
    await ctx.send("Member data exported to CSV file.")


import pandas as pd

# if file exists read it or make it and read it


@bot.command(name="claim_reward")
async def claim_reward(ctx):
    try:
        print("Id: ", ctx.message.author.id)
        print("Claiming reward")
        verified = False
        for role in ctx.message.author.roles:
            if role.name in ["Whitelist", "Early Pretender", "Verified"]:
                verified = True
                break
        print("Verified: ", verified)
        print(ctx.message.content)
        # print author
        print("author name", ctx.message.author.name)
        print(ctx.message.content.split(" ")[1])
        try:
            df = pd.read_csv("members_reward.csv")
        except:
            df = pd.DataFrame(columns=["Name", "Address", "ID"])
        if verified:
            # add to df
            df.loc[len(df)] = [
                ctx.message.author.name,
                ctx.message.content.split(" ")[1],
                ctx.message.author.id,
            ]
            df.to_csv("members_reward.csv", index=False)
            await ctx.send(
                f"Congratulations {ctx.message.author.name}! You should receive your reward soon!"
            )
        else:
            await ctx.send(
                "You are not an early pretender! Please get the early pretender role in the discord to claim your reward!"
            )
    except Exception as e:
        print(e)
        await ctx.send("Error claiming reward")


@bot.event
async def on_ready():
    print(f"Ready! Logged in as {bot.user}")


@bot.event
async def on_message(message):
    print(message)
    await bot.process_commands(message)


BOT_TOKEN = "MTE1NDgxNzcwNDI1NjA4NjA3Nw.G8jr5F.FIn0rVuRZ4jTAsPWFcW2STGqgnKLXUX5LuXXHM"
bot.run(BOT_TOKEN)
