import discord
from random import randint
import sqlite3

########################################
#All the SQL setup stuff goes here
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except sqlite3.Error as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection,query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print('Query executed succesfully')
    except sqlite3.Error as e:
        print(f'The error "{e}" occured"')

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        print(f'The error "{e}" occurred')

connection = create_connection('./sm_app.sqlite')

execute_query(connection, """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL
);
""")

execute_query(connection, """
CREATE TABLE IF NOT EXISTS actions (
    id INTEGER PRIMARY KEY,
    actionname TEXT NOT NULL
)
""")

execute_query(connection, """
CREATE TABLE IF NOT EXISTS useraction (
    sendid INTEGER,
    actionid INTEGER,
    recieveid INTEGER,
    count INTEGER,
    FOREIGN KEY (sendid) REFERENCES users (id),
    FOREIGN KEY (actionid) REFERENCES actions (id),
    FOREIGN KEY (recieveid) REFERENCES users (id),
    PRIMARY KEY (sendid, actionid, recieveid)
)
""")

########################################

errorMessage = 'Invalid syntax: for help please use .nkr help'

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = str(message.content)

    if msg.startswith('.nkr'):#command handling code
        msg = msg[5:]

        if msg == 'help':
            await message.channel.send(open('help.txt').read())

        elif msg.startswith('go'):
            msg = msg[3:]

            if msg.startswith('slap'):
                msg = msg[5:]
                phil = discord.File('./giftemp/anislap/' + str(randint(0,106)) + '.gif', filename='gif.gif')
                await message.channel.send("You've been slapped " + msg, file=phil)

            else:
                await message.channel.send(errorMessage)

        elif msg.startswith('say'):
            msg = msg[4:]

            if msg.startswith('-hide'):
                msg = msg[5:]
                await message.delete()

            await message.channel.send(msg)

        elif msg.startswith('test'):
            msg = msg[5:]
            if msg == 'ping':
                await message.channel.send('pong')
            else:
                await message.channel.send(errorMessage)

        else: #last possible case, make sure this is at the end
            await message.channel.send(errorMessage)

client.run(open('apikey').read())
