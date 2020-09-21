import discord
import yaml
from discord.ext import commands

bot_version = "2020.9.20"

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)
token = cfg["token"]

bot = commands.Bot(command_prefix="$",
                   description="The official bot for Netsoc at Ontario Tech University",
                   owner_id=cfg["owner-id"],
                   case_insensitive=True,
                   activity=discord.Game(name="with your firewalls - v{1}".format("$", bot_version)))


@bot.event
async def on_ready():
    print("Netsoc Bot is now ready!")
    print("Running version {0}".format(bot_version))


async def is_owner(ctx):
    return ctx.author.id == ctx.message.guild.owner_id


async def deletemsg(ctx):
    try:
        await ctx.message.delete()
        print("INFO: Applicant {0} - Succesfully delete message: {1}"
              .format(ctx.message.author.name, ctx.message.content))
    except discord.Forbidden as e:
        await ctx.message.author.send(
            "{0}, could not delete command message. Permission denied. Please DM an Executive ASAP!"
                .format(ctx.author.mention))
        print("ERROR: Applicant {0} - Could not delete message (Forbidden): {1}"
              .format(ctx.message.author.name, ctx.message.content))
        print(e)
    except discord.NotFound as e:
        await ctx.message.author.send(
            "{0}, could not delete command message. Message not found. Please DM an Executive ASAP!"
                .format(ctx.author.mention))
        print("ERROR: Applicant {0} - Could not delete message (NotFound): {1}"
              .format(ctx.message.author.name, ctx.message.content))
        print(e)
    except discord.HTTPException as e:
        await ctx.message.author.send(
            "{0}, could not delete command message. Deletion failed. Please DM an Executive ASAP!"
                .format(ctx.author.mention))
        print("ERROR: Applicant {0} - Could not delete message (HTTPException): {1}"
              .format(ctx.message.author.name, ctx.message.content))
        print(e)


@bot.command(pass_context=True)
async def apply(ctx, email, year_raw, rules):
    # Make the characters lowercase
    email.lower()
    rules.lower()

    # Ensure they agree to the rules
    if rules != "yes":
        await ctx.message.author.send("{0}! You must agree to the rules found in #welcome-and-rules! "
                                      "Please DM an Executive if you believe there is an error!"
                                      .format(ctx.message.author.mention))
        await deletemsg(ctx)
        print("INFO: Application Denied - Reason: Rules - Applicant: {0}".format(ctx.message.author.name))
        print(ctx.message.content)
        return
    # Ensure their grad year is valid
    if len(year_raw) > 4 and year_raw[0] != "2" and year_raw[1] != "0" and (year_raw[2] != "2" or year_raw[2] != "1"):
        await ctx.message.author.send("{0}! You must provide a valid grad year! "
                                      "Accepted years are 2010-2029. Please DM an Executive "
                                      "if you believe there is an error!"
                                      .format(ctx.message.author.mention))
        await deletemsg(ctx)
        print("INFO: Application Denied - Reason: Invalid Grad Year - Applicant: {0}".format(ctx.message.author.name))
        print(ctx.message.content)
        return
    # Ensure they provide a valid email
    if email.split("@")[1] != "ontariotechu.net":
        await ctx.message.author.send("{0}! You must provide a valid OntarioTechu.net email! "
                                      "Please DM an Executive is believe there is an error!"
                                      .format(ctx.message.author.mention))
        await deletemsg(ctx)
        print("INFO: Application Denied - Reason: Invalid OTU Email - Applicant: {0}".format(ctx.message.author.name))
        print(ctx.message.content)
        return

    # Save their email to a file
    print("INFO: Applicant: {0} - Saving email to file...".format(ctx.message.author.name))
    f = open("emails.txt", "a")
    f.write(email + "\n")
    f.close()
    print("INFO: Applicant: {0} - Successfully saved email to file.".format(ctx.message.author.name))

    # Get the members nickname based on their email address
    print("INFO: Applicant {0} - Determining First name and Last initial...".format(ctx.message.author.name))
    try:
        fname_raw = email.split(".")
        fname = fname_raw[0]
        lname_raw = fname_raw[1].split("@")
        lname = str(lname_raw[0])[0].upper() + "."
        name = str(fname).capitalize() + " " + str(lname)
        print("INFO: Applicant {0} - Determined First name and Last initial: {1}".format(ctx.message.author.name, name))
    except ValueError as e:
        await ctx.message.author.send("{0}! There was an error with your email address! "
                                      "Please DM an Executive for assistance."
                                      .format(ctx.message.author.mention))
        await deletemsg(ctx)
        print("ERROR: Applicant {0} - ValueError determining the users name based on their email!")
        print(e)
        return

    # Set the members nickname
    print("INFO: Applicant {0} - Setting nickname to {1}...".format(ctx.message.author.name, name))
    try:
        await ctx.message.author.edit(nick=name)
        print("INFO: Applicant {0} - Successfully set nickname to {1}".format(ctx.message.author.name, name))
    except discord.HTTPException as e:
        await ctx.message.author.send("{0}! There was an error setting your nickname! "
                                      "Please DM an Executive for assistance."
                                      .format(ctx.message.author.mention))
        await deletemsg(ctx)
        print("ERROR: Applicant {0} - Could not set nickname (HTTPException)".format(ctx.message.author.name))
        print(e)
        return

    # Add them to their year role
    print("INFO: Applicant {0} - Setting year role and Verified roles...")
    try:
        year = "Class of " + year_raw
        roleyr = discord.utils.get(ctx.guild.roles, name=year)
        vrfyrl = discord.utils.get(ctx.guild.roles, name="Verified")
        await ctx.message.author.add_roles(vrfyrl, roleyr)
        print("INFO: Applicant {0} - Successfully added {1} role and Verified role"
              .format(ctx.message.author.name, year))
    except discord.HTTPException as e:
        await ctx.message.author.send("{0}! There was an error adding your roles! "
                                      "Please DM an Executive for assistance."
                                      .format(ctx.message.author.mention))
        await deletemsg(ctx)
        print("ERROR: Applicant {0} - Could not set roles (HTTPException)".format(ctx.message.author.name))
        print(e)
        return

    # Delete their message
    print("INFO: Applicant {0} - Deleting command message...".format(ctx.message.author.name))
    await deletemsg(ctx)

    # Send the user a message to confirm they have registered
    print("INFO: Applicant {0} - Sending success message...".format(ctx.message.author.name))
    success_member = discord.Embed(title="A Huge Success!",
                                   description="Hi! "
                                               "You've successfully registered and verified yourself for the Netsoc "
                                               "OT - Official Discord! Below are the details we gathered from your "
                                               "application, please let us know if there are any issues!"
                                               "\nYour Name: {0}\nEmail: {1}\nGrad Year: {2}\nAccept Rules?: {3}"
                                               "\nThank you for joining us! Make sure to see our role "
                                               "assignment channel for more roles!".format(name, email, year, rules),
                                   colour=discord.Colour.dark_blue())
    await ctx.message.author.send(embed=success_member)
    print("INFO: Applicant {0} - Successfully sent applicant success message".format(ctx.message.author.name))

    # Send the executives a message to confirm a new registration
    print("INFO: Applicant {0} - Sending executive success message...".format(ctx.message.author.name))
    channel = bot.get_channel(620996002316288041)
    success_execs = discord.Embed(title="New Member!",
                                  description="Someone successfully registered and verified themself! "
                                              "Below are the details gathered from the application"
                                              "\nName: {0}\nEmail: {1}\nGrad Year: {2}\nAccept Rules?: {3}"
                                  .format(name, email, year, rules),
                                  color=discord.Colour.dark_blue())
    await channel.send(embed=success_execs)
    print("INFO: Applicant {0} - Successfully sent executive success message".format(ctx.message.author.name))


bot.run(token, bot=True, reconnect=True)
