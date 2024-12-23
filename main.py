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
  print("Registered commands:")
  for command in bot.commands:
    print(f"- {command.name}")


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

@bot.command()
async def log(ctx):
  questions = [
    "What is your timezone? (GMT/EST/AEST)",
    "What is the event start time? (Format: MM/DD/YY HH:MM AM/PM)",
    "What is the event end time? (Format: MM/DD/YY HH:MM AM/PM)",
    "How many attendees were present?",
    "How many passers were there?",
    "What are the names of the passers? (Separate names with commas)"
  ]
  answers = []

  def check(m):
    return m.author == ctx.author and m.channel == ctx.channel

  # Collect the messages to delete
  messages_to_delete = [ctx.message]  # Start with the command message itself
  
  for question in questions:
    bot_msg = await ctx.send(question)
    messages_to_delete.append(bot_msg)
    try:
      msg = await bot.wait_for('message', timeout=60.0, check=check)
      answers.append(msg.content)
      messages_to_delete.append(msg)
    except asyncio.TimeoutError:
      timeout_message = await ctx.send("You took too long to respond! Please try again.")
      messages_to_delete.append(timeout_message)
      return

  try:
    # Parse start and end times
    start_time = datetime.strptime(answers[1], "%m/%d/%y %I:%M %p")
    end_time = datetime.strptime(answers[2], "%m/%d/%y %I:%M %p")

    # Calculate duration in minutes
    duration = int((end_time - start_time).total_seconds() / 60)

    # Collect other details
    timezone = answers[0]
    attendees = int(answers[3])
    passers = int(answers[4])
    passers_names = answers[5]

    # Generate the log message
    log_message = (
      "```"
      f"Host: <@{ctx.author.id}>\n"
      f"Event Type: BMT\n"
      f"Timezone: {timezone}\n"
      f"Event Start Time: {answers[1]}\n"
      f"Event End Time: {answers[2]}\n"
      f"Event Duration: {duration} minutes\n"
      f"Attendees: {attendees}\n"
      f"Passers: {passers}\n"
      f"Passers Names: {passers_names}\n"
      f"RSM: <@&1114263017526407221>\n"
      f"Proof:\n"
      "```"
    )

    # Send the log message
    await ctx.send("All you need to do is include you start and end screenshot when sending it to <#960314396763127909>\n" + log_message)
    # Delete all collected messages except the final log message
    await ctx.channel.purge(limit=None, check=lambda m: m in messages_to_delete)

  except ValueError:
    await ctx.send("Invalid date format. Please use 'MM/DD/YY HH:MM AM/PM' for times.")
  except Exception as e:
    await ctx.send(f"An error occurred: {e}")

@bot.command()
async def intro(ctx):
  intro_embed = discord.Embed(
    title = 'Phase 1 - Introduction',
    description = 'Below you can find each message you need to send to complete the introductory phase.',
    color = discord.Color.green()
  )
  intro_embed.add_field(
    name = '',
    value = '```WELCOME TO YOUR BASIC MILITARY TRAINING. I, SERGEANT MAJOR, LITTLEBLUEFELINE, WILL BE YOUR INSTRUCTOR. IT IS MY JOB TO TRANSFORM YOU FROM CIVILIANS TO SOLDIERS.```',
    inline = False
  )
  intro_embed.add_field(
    name = '',
    value = '```DURING THIS BASIC MILITARY TRAINING, YOU WILL BE EQUIPPED WITH THE KNOWLEDGE AND SKILLS TO BECOME AN ENLISTED MEMBER OF THE BRITISH ARMY.```',
    inline = False
  )
  intro_embed.add_field(
    name = '',
    value = '```YOU ARE EXPECTED TO OBEY EVERY ORDER THAT I GIVE YOU AND WILL ONLY SPEAK WHEN GIVEN PERMISSION TO.```',
    inline = False
  )
  intro_embed.add_field(
    name = '',
    value = ' ```YOU ARE REQUIRED TO RESPOND IMMEDIATELY TO MY QUESTIONS IN FULL CAPITAL LETTERS.```',
    inline = False
  )
  intro_embed.add_field(
    name = '',
    value = '```IF YOU WANT TO SPEAK, YOU WILL BE REQUIRED TO SAY “PERMISSION TO SPEAK, INSTRUCTOR?”```',
    inline = False
  )
  intro_embed.add_field(
    name = '',
    value = '```IF YOU ARE UNABLE TO FOLLOW ORDERS AT ANY POINT, YOU WILL RECEIVE A STRIKE. IF YOU RECEIVE 3 STRIKES, YOU WILL BE DISMISSED.```',
    inline = False
  )
  intro_embed.add_field(
    name = '',
    value = '```YOU MUST ADDRESS ME AS “INSTRUCTOR”, AND “INSTRUCTOR” ONLY.```',
    inline = False
  )
  intro_embed.add_field(
    name = '',
    value = '```AM I UNDERSTOOD?```',
    inline = False
  )
  await ctx.send(
    f"{ctx.author.mention}",
    embed = intro_embed,
    delete_after = 600
  )
  await ctx.message.delete()

@bot.command()
async def drills(ctx):
  drills_embed = discord.Embed(
    title = 'Phase 2 - Drill Commands',
    description = 'Below you can find each message you need to send to complete the drill commands phase.',
    color = discord.Color.green()
  )
  drills_embed.add_field(
    name = '',
    value = '```I WILL NOW GO OVER THE DRILLS.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```THESE WILL BE VALUABLE FOR YOUR ENDEAVOURS WITHIN THE BRITISH ARMY.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```YOU MUST WATCH ME BUT DO NOT COPY ME.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```LEFT, TURN! - THIS IS A 90 DEGREE TURN TO YOUR LEFT FROM YOUR CURRENT POSITION.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```LEFT, INCLINE! - THIS IS A 45 DEGREE INCLINE TO YOUR LEFT FROM YOUR CURRENT POSITION.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```ABOUT, TURN! - THIS IS A 180 DEGREE TURN. YOU WILL FACE THE OPPOSITE DIRECTION THAT YOU CURRENTLY ARE.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```RIGHT, TURN! - THIS IS A 90 DEGREE TURN TO YOUR RIGHT, NO MATTER WHAT POSITION YOU ARE IN.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```RIGHT, INCLINE! - THIS IS A 45 DEGREE INCLINE TO YOUR RIGHT.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```CENTRE, TURN! - YOU MUST FACE THE DIRECTION OF THE HOST.```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```IF THE DRILL IS SPELT INCORRECTLY OR "SQUAD," IS NOT SAID, YOU WILL NOT PERFORM THE DRILL!```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```DOES EVERYONE UNDERSTAND THE DRILLS?```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```YOU WILL NOW DEMONSTRATE THE DRILLS!```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```GREAT JOB ON THE DRILLS!```',
    inline = False
  )
  drills_embed.add_field(
    name = '',
    value = '```' + 'IT IS TIME TO HEAD TO THE CLASSROOM IN ORDER TO LEARN ABOUT THE GENERAL RULES OF THE BRITISH ARMY.' + '```',
    inline = False
  )
  await ctx.send(
    f'{ctx.author.mention}',
    embed = drills_embed,
    delete_after = 600
  )
  await ctx.message.delete()

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
