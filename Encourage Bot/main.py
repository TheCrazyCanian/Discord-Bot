import os
import discord
from dotenv import load_dotenv
import requests
import json
import random
import mariadb
import sys

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
USERPASSWORD = os.getenv('USER_PASSWORD')

client = discord.Client()

########################################################################################################

sad_words = ["akelig", "afschuwelijk", "afgrijselijk", "alarmerend", "alleen", "achtergesteld", "afgunstig", "armzalig", "aangeklaagd", "afzijdig", "arrogant", "angst", "afsnauwen", "afkeuren",
             "afgedankt", "aso", "aanvallen", "agressief", "achterdochtig", "argwanend", "aarzelen", "beducht", "begoocheld", "bang", "bevreesd", "belast", "bezwaard", "beperkt", "bruut", "beest", "bewogen",
             "besluiteloos", "botsen", "bitter", "bedrogen", "beroofd", "bijtend", "beschuldig", "beklaagd", "beschaamd", "bedriegen", "bezwaarlijk", "boos", "benauwd", "bezorgd", "beschamend", "bedrieglijk",
             "bedroevend", "bevooroordeeld", "beperkt", "bende", "berouw", "belachelijk", "bedreigd", "bekritiseren", "bezwaar", "bezeten", "bestraft", "beledigen", "beroerd", "berispen", "beroven", "bekrompen",
             "cynisch", "conflict", "chagrijnig", "corrupt", "chaotisch", "depressief", "droevig", "deerlijk", "denigrerend", "dol", "dom", "dwaas", "dor", "dwaas", "doosbang", "droefenis", "drama", "dwarsbomend",
             "dwingen", "eigenzinnig", "eigenwijs", "eenzaam", "ellendig", "erbarmelijk", "eigenaardig", "flauw", "fobisch", "gebukt", "gedegradeerd", "gedevalueerd", "gedeprimeerd", "gruwelijk", "geïsoleerd",
             "geschokt", "geklaag", "gek", "gejaagd", "gemeden", "gebrekkig", "gekleineerd", "gekweld", "grimmig", "geschonden", "gekrenkt", "gezondigd", "gedwarsboomd", "gevreesd", "geslagen", "geïntimideerd",
             "gierig", "geruïneerd", "gebrekkig", "gehinderd", "gemarteld", "gealarmeerd", "geïrriteerd", "geërgerd", "gesloopt", "gefrustreerd", "gepijnigd", "huiveringwekkend", "hopeloos", "huiliger", "humeurig",
             "hatend", "hatelijk", "hoogmoedig", "hachelijk", "harteloos", "hulpeloos", "huichelaar", "hypocriet", "hysterisch", "hebzucht", "hinderend", "haatdragend", "incompetent", "ineffectief", "inhalig",
             "inadequaat", "irriterend", "jammerlijk", "jaloers", "jagen", "koppig", "klef", "kapot", "knoeien", "kinderachtig", "kregelig", "krankzinnig", "krachteloos", "kwaad", "kil", "kritisch", "knorrig",
             "kwetsbaar", "lastig", "lafhartig", "lafbek", "lusteloos", "leugenaar", "liegen", "lomp", "leugens", "laaiend", "lui", "misselijk", "misselijkmakend", "misbruikt", "misdeeld", "muiterij", "manipulerend",
             "machteloos", "materialistisch", "moe", "materteling", "mislukt", "meedogenloos", "naar", "namaak", "nep", "neerslachtig", "nalatig", "", "nutteloos", "ongerust", "opgesloten", "onverzettelijk", "onbegrijpelijk"
             "onbegrepen", "onbegrip", "onecht", "onverantwoordelijk", "onvergeeflijk", "ongedurig", "onuitgemaakt", "opgelicht", "ontnormen", "onbekwaam", "opstandig", "oproerend", "onzeker", "onvast", "ongeorganiseerd",
             "ontwricht", "ongeduldig", "opstandig", "onbezonnen", "onvriendelijk", "ondankbaar", "onaangenaam", "onmachtig", "ongelukkig", "onnadenkend", "onhandig", "ontevreden", "onbelangrijk", "onaangenaam", "oppervlakkig",
             "onverstandig", "onderschat", "onoprecht", "onwaardig", "onterecht", "onplezierig", "ontroostbaar", "onvolledig", "ontaard", "ongemakkelijk", "onwetend", "onzinnig", "onverantwoordelijk", "ongebruikt", "onbeschermd",
             "ongedisciplineerd", "onredelijk", "passief", "paniekerig", "pessimistisch", "prikkelbaar", "rammelend", "rauw", "rusteloos", "razend", "rebels", "roerig", "raar", "somber", "stockerend", "schrikken", "strijd", "slap",
             "slecht", "sarcastisch", "spottend", "schrikbarend", "stom", "stommiteit", "schamen", "spijt", "schuchter", "schuldig", "smerig", "smoesjes", "straf", "slaan", "smijten", "schandalig", "schraal", "trouweloos", "terneergeslagen",
             "treurig", "twistend", "troosteloos", "tegengesteld", "teruggetrokken", "twijfel", "twijfelachtig", "terughoudend", "teleurgesteld", "timide", "uitgeput", "uitputtend", "uitgesloten", "uitzetten", "uitbuiten", "verlaten", "vervreemd",
             "verbijsterd", "verbluft", "vergeten", "vreselijk", "verschrikkelijk", "verzettend", "verbolgen", "verguisd", "verkeerd", "vals", "verdrietig", "vaal", "veelbewogen", "verontrust", "verbannen", "verstoten", "verbitterd", "vernederend",
             "verwoest", "verdoemd", "vermoeid", "verzwakt", "verslapt", "vijandig", "verlamd", "verachtend", "vreselijk", "verschrikkelijk", "vervelend", "verdacht", "vijandelijk", "verwaarloosd", "vermeden", "verlegen", "verminkt", "vernederend",
             "verwerpen", "vreugdeloos", "verbitterd", "vuil", "vies", "verstoteling", "verliezen", "verloren", "verontwaardigd", "verkeerd", "vrezen", "vervolgen", "verstikken", "verontrustend", "vrekkig", "vermoeiend", "verwaand", "vervloekt",
             "verspilling", "verraden", "woedend", "wraak", "wanhopig", "woelig", "waardeloos", "wraakzuchtig", "waanzin", "wegsturen", "wrok", "weemoed", "wreed", "wanhopig", "wantrouwen", "wanhopig", "weerzinwekkend", "walgen", "zonde", "zenuwachtig",
             "zenuwslopend", "zenuwen", "zwaar", "zwak", "zorgeloos", "zorgwekkend", "zondig", "sad"]


encouragements = ["Je bent de beste", "Je ziet er prachtig uit vandaag", "Een dag hoeft nooit helemaal goed te zijn, maar er zit altijd iets goeds in de dag", "Accept the things you cannot change, and change the things you cannot accept",
                  "Uw haar zit geweldig", "Je hebt uw best gedaan met uw outfit!", "Everything will be okay in the end. If it isn't ok, then it's not the end…", "Never be a prisoner of your past, but be an architect of your future",
                  "Geluk is heel graag willen wat je al hebt", "Alles komt goed!", "Uw glimlach geeft mij een reden om elke dag op te staan!", "Ik zal er altijd voor jou zijn!", "Jij bent het lichtpunt van mijn leven!"]

########################################################################################################
# Connect to MariaDB Platform, defines global variables conn and cursor
def connect_MariaDB():
    try:
        global conn
        conn = mariadb.connect(
            user="user",
            password=USERPASSWORD,
            host="192.168.76.3",
            port=3306,
            database="Discord_Bots"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    # Get Cursor
    global cursor
    cursor = conn.cursor()

# Inserts the given value's (id and (sad_word or encouragment)) into the table  
def insertValues_MariaDB(table, value1, value2):
    connect_MariaDB()
    try:
        statement = ('INSERT INTO %s VALUES (%s, "%s")' % (table, value1, value2))
        cursor.execute(statement)
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

# Deletes a value from a table 
def deleteValues_MariaDB(table, column, value):
    connect_MariaDB()
    try:
        statement = ("DELETE FROM %s WHERE %s=%s" % (table, column, value))
        cursor.execute(statement)
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

# Deletes a whole table
def deleteWholeTable_MariaDB(table):
    connect_MariaDB()
    try:
        statement = ("DELETE FROM %s" % (table))
        cursor.execute(statement)
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

# Returns list of the cursor, F.E: [(1, sad), (2, akelig)]
# Returns 0 if no match is found for value
def selectAll_MariaDB(table):
    connect_MariaDB()
    try:
        statement = ("SELECT * FROM %s" % (table))
        cursor.execute(statement)
        if type(cursor) == "None":
            return 0
        else:
            return list(cursor)
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

# Returns list of the cursor with the 10 last values (based on id), F.E: [(1, sad), (2, akelig)]
# Returns 0 if no match is found for value 
def selectLast_MariaDB(table):
    connect_MariaDB()
    try:
        statement = ("SELECT * FROM %s ORDER BY id DESC LIMIT 10" % (table))
        cursor.execute(statement)
        if type(cursor) == "None":
            return 0
        else:
            return list(cursor)
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

# Returns list of the cursor, F.E: [(1, sad), (2, akelig)]
# Returns 0 if no match is found for value
def selectSpecific_MariaDB(table, column, value):
    connect_MariaDB()
    try:
        statement = ('SELECT * FROM %s WHERE %s = "%s"' % (table, column, value))
        cursor.execute(statement)
        if type(cursor) == "None":
            return 0
        else:
            return list(cursor)
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

# Returns True if table is empty, False if not empty
def table_IsEmpty(table):
    connect_MariaDB()
    try:
        statement = ("SELECT * FROM %s" % (table))
        cursor.execute(statement)
        test = list(cursor)
        if len(test) == 0:
            return True
        else:
            return False
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.close()

# Returns a list of all the values (not id's) of the given table
def getValuesList_MariaDB(table):
    List = selectAll_MariaDB(table)
    Values = []
    for i in List:
        Values.append(i[1])
    return Values

# Returns the max id of the given table
# Returns one tuple of the cursor in the form: (id, otherColumn)
def getMaxId(table):
    connect_MariaDB()
    try:
        statement = ("SELECT MAX(id) FROM %s" % (table))
        cursor.execute(statement)
        return cursor.fetchone()
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()
   
# updates the encouragements table with an encouraging message 
def InsertNewValue_MariaDB(table, value):
    connect_MariaDB()
    try:
        maxId = getMaxId(table)
        newId = int(maxId[0]) + 1
        statement = ('INSERT INTO %s VALUES (%s, "%s")' % (table, newId, value))
        cursor.execute(statement)
    except mariadb.Error as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()

# Used to execute a given sql statement.
# If the sql statement starts with 'select', the cursor is returned as a list.
# Else, the function returns 0
def ExecuteSQLStatement_MariaDB(statement):
    connect_MariaDB()
    try:
        cursor.execute(("%s" % (statement)))
        if statement.split(' ')[0].lower() == 'select':
            return list(cursor)
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
    conn.commit()
    conn.close()
        
########################################################################################################

# Used to get a random quote from zenquotes.io
def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return(quote)

########################################################################################################

# If the tables are empty, they are filled
if table_IsEmpty("Sad_Words"):
    print("table Sad_Words is being filled")
    a = 1   # Moet beginnen vanaf 1
    for i in sad_words:
        insertValues_MariaDB("Sad_Words", a, i)
        a += 1
if table_IsEmpty("Encouragements"):
    print("table Encouragements is being filled")
    b = 1
    for i in encouragements:
        insertValues_MariaDB("Encouragements", b, i)
        b += 1

########################################################################################################

@client.event
async def on_ready():
    print('We have logged in as %s' % (client.user))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    encouragementsDB = getValuesList_MariaDB("Encouragements")
    
    # Used to check if any message contains a sad word.
    # If it contains a sad word, a random quote or a random encouragement is sent.
    for word in msg.split(' '):
        if len(selectSpecific_MariaDB("Sad_Words", "sad_word", word)) > 0:
            nr = random.randrange(0, 2)
            if nr == 0:
                await message.channel.send(random.choice(encouragementsDB))
            else:
                quote = get_quote()
                await message.channel.send(quote)
            break

    # Used to make a new encouragement
    if msg.startswith("$newE"):
        encouraging_message = msg.split('$newE ', 1)[1]
        newValueCheck = selectSpecific_MariaDB("Encouragements", "encouragement", encouraging_message)
        if len(newValueCheck) > 0:
            await message.channel.send("value already exists with id: %s and value: %s" %(newValueCheck[0][0], newValueCheck[0][1]))
        else:
            InsertNewValue_MariaDB("Encouragements", encouraging_message)
            insertedValues = selectSpecific_MariaDB("Encouragements", "encouragement", encouraging_message)
            await message.channel.send("New encouragement was added with id: %s and value: %s" %(insertedValues[0][0], insertedValues[0][1]))
            
    # Used to make a new sad word      
    if msg.startswith("$newS"):
        sad_message = msg.split('$newS ', 1)[1]
        newValueCheck = selectSpecific_MariaDB("Sad_Words", "Sad_Word", sad_message)
        if len(newValueCheck) > 0:
            await message.channel.send("value already exists with id: %s and value: %s" %(newValueCheck[0][0], newValueCheck[0][1]))
        else:
            InsertNewValue_MariaDB("Sad_Words", sad_message)
            insertedValues = selectSpecific_MariaDB("Sad_Words", "Sad_Word", sad_message)
            await message.channel.send("New sad word was added with id: %s and value: %s" %(insertedValues[0][0], insertedValues[0][1]))

    # Used to delete an encouragement
    if msg.startswith("$delE"):
        delete_id = msg.split('$delE ', 1)[1]
        deleteValueCheck = selectSpecific_MariaDB("Encouragements", "id", delete_id)
        if len(deleteValueCheck) == 0:
            await message.channel.send("'%s' does not exist in the Encouragements table." %(deleteValueCheck))
        else:
            deleteValues_MariaDB("Encouragements", "id", delete_id)
            await message.channel.send("Encouragement was deleted with id: %s" %(delete_id))
            
    # Used to delete an encouragement
    if msg.startswith("$delS"):
        delete_id = msg.split('$delS ', 1)[1]
        deleteValueCheck = selectSpecific_MariaDB("Sad_Words", "id", delete_id)
        if len(deleteValueCheck) == 0:
            await message.channel.send("'%s' does not exist in the Sad_Words table." %(deleteValueCheck))
        else:
            deleteValues_MariaDB("Sad_Words", "id", delete_id)
            await message.channel.send("Sad word was deleted with id: %s" %(delete_id))
     
    # Used to show to full table
    if msg.startswith("$showF"):
        table = msg.split('$showF ', 1)[1]
        list = selectAll_MariaDB(table)
        messageToSend = ""
        try:
            for i in list:
                messageToSend += ("%s -> %s\n" % (i[0], i[1]))
            await message.channel.send(messageToSend)
        except Exception as e:
            await message.channel.send("Error: %s" %(e))
    
    # Used to show the last 10 rows of the table based on id
    if msg.startswith("$showL"):
        table = msg.split('$showL ', 1)[1]
        list = selectLast_MariaDB(table)
        messageToSend = ""
        try:
            for i in list:
                messageToSend += ("%s -> %s\n" % (i[0], i[1]))
            await message.channel.send(messageToSend)
        except Exception as e:
            await message.channel.send("Error: %s" %(e))

    # Used to execute a given sql statement, if the sql statement starts with 'select', the result set is printed. 
    # Else, there is another message printed
    if msg.startswith("$sql"):   
        statement = msg.split('$sql ', 1)[1]  
        try:
            list = ExecuteSQLStatement_MariaDB(statement)
            if list != 0:
                s = ""
                for i in list:
                    s += str(i[0]) + ", " + str(i[1]) + "\n"
                await message.channel.send(s) 
            else:
                 await message.channel.send("SQL statement has no output")           
        except Exception as e:
            await message.channel.send("Error: %s" %(e))
    
    # Explanation of all the functions that can be accessed from Discord.
    if msg.startswith("$help"):
        string = "This is the Encourage Bot. This bot reads messages and when it sees a sad word, it will send an encouraging message or an inspirational quote.\n" \
        "Commands that can be used:\n" \
            "\t**$newE {Value}** -> Creates a new Encouragement in the database with the given value.\n" \
            "\t**$newS {Value}** -> Creates a new Sad Word in the database with the given value.\n" \
            "\t**$delE {id}** -> Deletes an Encouragement with the given id.\n" \
            "\t**$delS {id}** -> Deletes a Sad Word with the given id.\n" \
            "\t**$showF {Encouragements | Sad_Words}** -> Shows the full table. Gives error if table too big.\n" \
            "\t**$showL {Encouragements | Sad_Words}** -> Shows the last 10 rows of the table based on id.\n" \
            "\t**$sql {statement}** -> Allows the user to execute a given SQL statement. If the statement is a SELECT statement, the return value will be printed. Possible databases to work on: Encouragements and Sad_Words.\n" \
            "\t**$help** -> To get the help page printed on screen\n" 
        await message.channel.send(string) 
            
            
client.run(TOKEN)
