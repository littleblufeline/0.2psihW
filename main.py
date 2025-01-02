# This example requires the 'message_content' privileged intents
import aiohttp
import asyncio
import datetime
import io
import os
import random
from aiohttp.hdrs import LINK
import time
import urllib.parse
from datetime import datetime, timedelta

import discord
from discord import guild
from discord.ext import commands
from discord.ext.commands import Bot

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True

bot = commands.AutoShardedBot(
  intents = intents,
  command_prefix='!'
)
bot.remove_command('help')

# Startup
@bot.event
async def on_ready():
  activity = discord.Activity(
    name='👀',
    type=3
  )
  await bot.change_presence(
    status=discord.Status.online,
    activity=activity
  )
  print(f"Logged into {bot.user}")
  print(f"Bot Id: {bot.user.id}")
  print(f'Shards: {bot.shard_count}')
  print("Registered commands:")
  for command in bot.commands:
    print(f"- {command.name}")


##############################################################################################################################################

# Rule Embed / Verify Embed
@bot.command()
async def remb(ctx):
  # Verify Button Handling - include emoji
  class VerifyButton(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)
    @discord.ui.button(label='Verify', style=discord.ButtonStyle.green, custom_id= 'verify_button', disabled = True)
    async def verify_button(self, interaction: discord.Interaction, button: discord.ui.Button):
      role1 = discord.utils.get(interaction.guild.roles, name='GR | Verified')
      role2 = discord.utils.get(interaction.guild.roles, name = 'GR | Unverified')
      await interaction.user.add_roles(role1)
      await interaction.user.remove_roles(role2)
      embed = discord.Embed(
        title = 'Verification Successfull! :white_check_mark:',
        description = 'You have been verified! Enjoy your stay!',
        color = discord.Color.green()
      )
      await interaction.response.send_message('', embed=embed, ephemeral=True)
  RuleEmbed = discord.Embed(
    title = 'MSRPC Rules',
    description = 'Here you can find all of our rules, from discord and in-game!',
    color = discord.Color.blurple()
  )
  RuleEmbed.add_field(
    name = 'Discord Rules',
    value = '```\nDISCORD RULES - CHANNELS\n```' + '\n\n',
    inline = False
  )
  await ctx.send('# Coming soon bc im too lazy 🤑', embed=RuleEmbed, view=VerifyButton())
  await ctx.message.delete(delay=0)

@bot.command()
async def resroles(ctx):
  guild = ctx.message.channel.guild
  channel_id = ctx.message.channel.id
  message_id = ctx.message.id
  author_id = ctx.message.author.id
  author = ctx.message.author.mention

  if author_id == guild.owner.id:
    in_progress_embed = discord.Embed(
    title = 'In Progress',
    description = 'Working on deleting all roles 👍',
    color = discord.Color.red()
    )
    in_progress_embed.add_field(
      name = 'Information',
      value = f'Command Initiated by: {author} ({author_id})'
    )
    await ctx.send(embed = in_progress_embed, delete_after = 600)
    await ctx.message.delete()
    for role in guild.roles:
      if role.is_bot_managed() or role.is_integration() or role.is_default():
        continue
      try:
        await role.delete(reason = f'Role Reset, Requested & Initiated by: {author}')
        await ctx.send(f'Role Deletion Success: Deleted "**{role.name}**"', delete_after = 10)
      except discord.Forbidden:
        await ctx.send(f'Unable to delete role: "**{role.name}**" (Insufficient permissions)')
      except discord.HTTPException as e:
        await ctx.send(f'Failed to delete role: "**{role.name}**" ({str(e)})')
  else:
    await ctx.reply(':warning: | Only the server owner and entrusted users may use this command!', delete_after = 10)

@bot.command()
async def reschannels(ctx):
  guild = ctx.message.channel.guild
  channel_id = ctx.message.channel.id
  message_id = ctx.message.id
  author_id = ctx.message.author.id
  author = ctx.message.author.mention

  if author_id == guild.owner.id:
    in_progress_embed = discord.Embed(
    title = 'In Progress',
    description = 'Working on deleting all channels 👍',
    color = discord.Color.red()
    )
    in_progress_embed.add_field(
      name = 'Information',
      value = f'Command Initiated by: {author} ({author_id})'
    )
    await ctx.send(embed = in_progress_embed, delete_after = 600)
    await ctx.message.delete()
    for channel in guild.channels:
      try:
        if channel.name == 'bgub-reset-logging':
          await ctx.send(f'Ignoring #bgub-reset-logging')
        else:
          await channel.delete(reason = f'Channel Reset, Requested & Initiated by: {author}')
          await ctx.send(f'Channel Deletion Success: Deleted "**{channel.name}**"', delete_after = 10)
      except discord.Forbidden:
        await ctx.send(f'Unable to delete channel: "**{channel.name}**" (Insufficient permissions)')
      except discord.HTTPException as e:
        await ctx.send(f'Failed to delete channel: "**{channel.name}**" ({str(e)})')
  else:
    await ctx.reply(':warning: | Only the server owner and entrusted users may use this command!', delete_after = 10)

@bot.command()
async def wakey(ctx, member: discord.Member, repeat: int = 3):
  if ctx.author.id == 770484893657333761:
    repeat = min(repeat, 25)
    # Create a thread from the command message
    thread = await ctx.message.create_thread(name=f"WAKE UP! {member.name}")
    # Send pings in the thread
    for _ in range(repeat):
      await thread.send(f"WAKEUP {member.mention}!")
      await asyncio.sleep(1)  # Add a delay between pings to avoid being too aggressive
    # Optional: Archive the thread after use
    await thread.edit(archived=True, locked=True)

############################################################################################################################################

# Welcomer
@bot.event
async def on_member_join(member):
  channel = discord.utils.get(guild.channels, name="『📌』welcome")
  embed = discord.Embed(
    title = 'Welcome!',
    description = f'Welcome to **Montana State Roleplay Community (MSRPC)**, {member.mention}!',
    color = discord.Color.blurple()
  )
  embed.add_field(
    name = 'Come chat with us!',
    value = '<#1255337358899810324>',
    inline = False
  )
  await channel.send(f'{member.mention}', embed=embed)

@bot.event
async def on_shard_ready(shard_id):
  print(f"Shard {shard_id} is ready.")

@bot.event
async def on_shard_disconnect(shard_id):
  print(f"Shard {shard_id} disconnected.")

bot.run(os.environ["DISCORD_TOKEN"])
