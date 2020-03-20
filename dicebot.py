import discord
from random import randint

TOKEN = 'NjkwNTI1MTU3MjEwNDU2MDk1.XnStgQ.lMc_tusiNDVMjWlL31jf_v-mz_Q'
client = discord.Client()


def calculate_success(dice, msg):
    copy = dice
    success = 0
    critcount = 0

    # check for crits
    i = 0
    while copy[0] == 10:
        for i in range(len(copy)):
            if copy[i] == 10:
                critcount+=1
                success+=1
                copy[i] = 0
            else:
                break
        if critcount > 0:
            msg += "Extra Rolls: "
        extras = []
        for i in range(critcount):
            roll = randint(1,10)
            extras.append(roll)
        critcount = 0
        msg += ", ".join(str(x) for x in extras)
        msg += "\n"
        for x in extras:
            copy.append(x)
        copy.sort(reverse=True)
    for i in range(len(copy)):
        for j in reversed(range(i+1,len(copy))):
            if copy[i]+copy[j] >= 10:
                success += 1
                copy[i] = 0
                copy[j] = 0
                break
    return msg, success


@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!roll'):
        quote = str(message.content)
        quote = quote.replace('+', ' ')
        quote = quote.replace(',', ' ')
        dice = [int(s) for s in quote.split() if s.isdigit()]
        totalDice = 0
        for die in dice:
            totalDice += die
        dice = []
        for i in range(totalDice):
            dice.append(randint(1,10))
        dice.sort(reverse=True)
        msg = "First Roll: "
        msg += ", ".join(str(x) for x in dice)
        msg += "\n"
        msg, success = calculate_success(dice, msg)
        msg += "Success: " + str(success)
        await message.channel.send(msg)

client.run(TOKEN)



