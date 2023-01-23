import discord
import time
import datetime

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

countingChannel = 0
textChannel = 0
token = ''

currentNumber = 0


def get_ETA():
    starttime = 1671495180
    startnumber = 69420
    currentTime = time.time()
    timeElapsed = currentTime-starttime
    numberscounted = startnumber-currentNumber
    numbersPerSecond = numberscounted/timeElapsed
    estimatedEnd = currentTime+currentNumber/numbersPerSecond
    timeStamp = datetime.datetime.fromtimestamp(estimatedEnd)
    return timeStamp




@client.event
async def on_ready():
    global currentNumber
    print(f'We have logged in as {client.user}')
    currentNumber = int(([message async for message in client.get_channel(countingChannel).history(limit=1)])[0].content)
    
    print(currentNumber)

@client.event
async def on_message(message):
    global currentNumber
    if message.author == client.user:
        return

    if message.channel.id == textChannel:
        if message.content == '$calibrate':
            try:
                temp = int(([message async for message in client.get_channel(countingChannel).history(limit=1)])[0].content)
                await client.get_channel(textChannel).send(f"Calibrated successfully. Count is now {str(temp)}.")
                currentNumber = temp
                print(currentNumber)
            except:
                await client.get_channel(textChannel).send("Failed to calibrate! Most recent message in #counting-down is not a valid number!")


        if message.content == "$eta":
            eta = get_ETA()
            await client.get_channel(textChannel).send(f"0 will be reached on {eta}")


    if message.channel.id == countingChannel:
        # Ensure that the message matches the current count
        try:
            messageNumber = int(message.content)
        except:
            messageNumber = False
            await client.get_channel(textChannel).send(str(message.author.mention)+f"!\nThat's not even a number! :bonk:\nEdit your message to be {str(currentNumber-1)}.")
            currentNumber -= 1
            print(currentNumber)
        if messageNumber != False:
            if messageNumber == currentNumber-1:
                currentNumber = messageNumber
                print(currentNumber)
            else:
                # If it doesn't match, ping the user who made the mistake and tell them to edit their message to the correct number
                await client.get_channel(textChannel).send(str(message.author.mention)+f"!\nYou counted wrong! :bonk:\nEdit your message to be {str(currentNumber-1)}.")
                currentNumber -= 1
                print(currentNumber)
        


(
    client.run(token)
)