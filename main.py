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

bot = commands.Bot(
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

##############################################################################################################################################

# Tickel panel
@bot.command()
async def tpnl(ctx):
  # Embed Button Handling
  class TicketPanel(discord.ui.View):
    def __init__(self):
      super().__init__(timeout=None)

    @discord.ui.button(label="Management Ticket", style=discord.ButtonStyle.danger, custom_id="create_mgmt_ticket")
    async def create_mgmt_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
      guild = interaction.guild
      category = discord.utils.get(guild.categories, name="TICKETS")
      if not category:
        category = await guild.create_category("TICKETS")
      mgmt_ticket_channel = await category.create_text_channel(f"{interaction.user.name}-management")
      await mgmt_ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True, embed_links=True, attach_files=True)
      ticket_support_role1 = discord.utils.get(guild.roles, name="MSRPC | High Ranks")
      ticket_support_role2 = discord.utils.get(guild.roles, name='MSRPC | Super High Ranks')
      await mgmt_ticket_channel.set_permissions(ticket_support_role1, read_messages=True, send_messages=True, embed_links=True, attach_files=True)
      await mgmt_ticket_channel.set_permissions(guild.default_role, read_messages=False)
      ManagementOpenEmbed = discord.Embed(
        title = 'New Management Ticket!',
        description = f'Ticket created by {interaction.user.mention}',
        color = discord.Color.green()
      )
      ManagementOpenEmbed.add_field(
        name = 'Please state your problem while you wait for staff to respond!',
        value = '',
        inline = False
      )
      ticket_id = ticket_channel.id
      await interaction.response.send_message(f"Ticket created! <#{ticket_id}>", ephemeral=True)

      class ManagementTicketClose(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
          
        @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close_mgmt_ticket")
        async def close_mgmt_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
          if interaction.user.id == 770484893657333761:
            await interaction.response.send_message("Ticket closed!", ephemeral=True)
            await mgmt_ticket_channel.edit(name = f'closed-{interaction.user.name}-mgmt')
            await mgmt_ticket_channel.set_permissions(interaction.user, read_messages=False, send_messages=False, embed_links=False, attach_files = False)
          else:
            await interaction.response.send_message("You do not have permission to close this ticket!", ephemeral=True)
      await mgmt_ticket_channel.send('@everyone', embed=OpenEmbed, view=ManagementTicketClose())
    
    @discord.ui.button(label="General Ticket", style=discord.ButtonStyle.green, custom_id="create_gen_ticket")
    async def create_gen_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
      guild = interaction.guild
      category = discord.utils.get(guild.categories, name="TICKETS")
      if not category:
        category = await guild.create_category("TICKETS")
      gen_ticket_channel = await category.create_text_channel(f"{interaction.user.name}-general")
      await gen_ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True, embed_links=True, attach_files=True)
      ticket_support_role1 = discord.utils.get(guild.roles, name="MSRPC | High Ranks")
      ticket_support_role2 = discord.utils.get(guild.roles, name='MSRPC | Super High Ranks')
      ticket_support_role3 = discord.utils.get(guild.role, name='MSRPC | Middle Ranks')
      await gen_ticket_channel.set_permissions(ticket_support_role1, read_messages=True, send_messages=True, embed_links=True, attach_files=True)
      await gen_ticket_channel.set_permissions(ticket_support_role2, read_messages=True, send_messages=True, embed_links=True, attach_files=True)
      await gen_ticket_channel.set_permissions(ticket_support_role3, read_messages=True, send_messages=True, embed_links=True, attach_files=True)
      await gen_ticket_channel.set_permissions(guild.default_role, read_messages=False)
      GeneralOpenEmbed = discord.Embed(
        title = 'New General Ticket!',
        description = f'Ticket created by {interaction.user.mention}',
        color = discord.Color.green()
      )
      GeneralOpenEmbed.add_field(
        name = 'Please state your problem while you wait for staff to respond!',
        value = '',
        inline = False
      )
      general_ticket_id = gen_ticket_channel.id
      await interaction.response.send_message(f"Ticket created! <#{general_ticket_id}>", ephemeral=True)
        
        
      class GeneralTicketClose(discord.ui.View):
        def __init__(self):
          super().__init__(timeout=None)
          
        @discord.ui.button(label="Close Ticket", style=discord.ButtonStyle.red, custom_id="close_gen_ticket")
        async def close_gen_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
          if interaction.user.id == 770484893657333761:
            await interaction.response.send_message("Ticket closed!", ephemeral=True)
            await gen_ticket_channel.edit(name = f'closed-{interaction.user.name}-gen')
            await gen_ticket_channel.set_permissions(interaction.user, read_messages=False, send_messages=False, embed_links=False, attach_files = False)
          else:
            await interaction.response.send_message("You do not have permission to close this ticket!", ephemeral=True)
      await gen_ticket_channel.send('@everyone', embed=OpenEmbed, view=GeneralTicketClose())
  # Panel Embed
  embed = discord.Embed(
    title = 'Ticket Panel',
    description = 'Click the button below to create a ticket! Our staff are more than happy to help with any issue you may have :P',
    color = discord.Color.blurple()
  )
  await ctx.send(embed=embed, view=TicketPanel())
  await ctx.message.delete(delay=0)

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

bot.run(os.environ["DISCORD_TOKEN"])
