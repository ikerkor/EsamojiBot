import settings
from settings import db, fernet
import time
import emoji as emo
import datetime
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler, CommandHandler, MessageHandler, Filters

# Aldagai globalak
EMOJI, ESAMOLDE, GOITIZEN, HERRI = range(4)  # Elkarrizketa-egoera-makinako egoerak
DIAL, ERANTZUN= range(2)  # Oharretako elkarrizketa-egoera-makinako egoera.
dicSarrera = {}  # Sarrerak gordetzeko hiztegia (aldibereko erabiltzailea saiesteko, azpihiztegiak)



# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def gehitu(update: Update, context: CallbackContext) -> int:
    """Elkarrizketa hasi eta esamoji berria sortzeko beharrezko datuak eskatuko dizkio"""
    update.message.reply_text('\U0001F9DE')
    time.sleep(0.5)
    update.message.reply_text(
        'Kaixo! Esamoji berri bat argitaratzen lagunduko dizut elkarrizketa bidez. Uneren batean prozesua eten nahi'
        ' baduzu, /utzi esan besterik ez duzu. Bestalde, botaren inguruko iradokizun edo iruzkinik egin nahi badidazu, '
        'sarrera amaitu ala eten eta gero, bidal iezadazu /oharra.'
    )
    time.sleep(2.5)
    update.message.reply_text('Hasteko, bidal iezadazu esamoldatu nahi duzun emojia: ')
    return EMOJI


def emoji(update: Update, context: CallbackContext) -> int:
    """Emojia gorde eta esamoldea eskatu"""
    stEmoji = update.message.text
    time.sleep(1)
    if not emo.is_emoji(stEmoji):  # Ez bada emoji bakar bat
        update.message.reply_text('Emojia (bakarra) behar du izan:')
        return EMOJI
    else:  # Emoji bakar bat denean
        if stEmoji in db.list_collection_names():  # kolekzioa jada sortua badago
            # Sortzaileak lehenago emoji honentzako zenbat sarrera dituen aztertu eta 2ra mugatuko da
            stSortzaile = str(update.message.from_user.id)
            lstdicSortzaileak = list(db[stEmoji].find({}, {'Sortzaile': 1, '_id': 0}))
            cnt = 0
            for dicSortzaile in lstdicSortzaileak:
                if bytes(stSortzaile, 'UTF-8') == fernet.decrypt(dicSortzaile['Sortzaile']):
                    cnt += 1
                    if cnt == 2:
                        break
            if cnt == 2:  # Zerrendako sarrera mugara iritsi bada <-- Aldatu!
                update.message.reply_text('Honezkero bi sarrera dituzu emoji honentzat. Saiatu beste batekin ala /utzi')
                return EMOJI
            elif len(lstdicSortzaileak) == 49:  # Beteta badago <-- Aldatu!
                lstdicBatezbesteLuze = list(db[stEmoji].find({}, {'BatezbesteLuze': 1, '_id': 0}))
                lstBatezbesteLuze = []
                for i, dic in enumerate(lstdicBatezbesteLuze):
                    lstBatezbesteLuze.append(dic["BatezbesteLuze"])
                minBatezbesteLuze = min(lstBatezbesteLuze)
                if minBatezbesteLuze <= 2 / 3456:  # <-- Aldatu!! 12 egunean bitan (edo sei egunean behin) gutxienez lekua gordetzeko
                    db[stEmoji].delete_one({"BatezbesteLuze": minBatezbesteLuze})
                    update.message.reply_text('Xarmanki')
                    dicSarrera[update.message.chat.id] = {}
                    dicSarrera[update.message.chat.id]['Emoji'] = stEmoji
                    time.sleep(1)
                    update.message.reply_text('Esamoldea orain:')
                    return ESAMOLDE
                else:
                    update.message.reply_text(
                        "Lastima! Zerrenda beteta dago eta sarrera bat bera ere ezin da ezabatu oraingoz. Saiatu berriro apur batean (/utzi) ala aukeratu beste emoji bat")
                    return EMOJI
            else:
                update.message.reply_text('Xarmanki')
                dicSarrera[update.message.chat.id] = {}
                dicSarrera[update.message.chat.id]['Emoji'] = stEmoji
                time.sleep(1)
                update.message.reply_text('Esamoldea orain:')
                return ESAMOLDE
        else:
            update.message.reply_text('Xarmanki')
            dicSarrera[update.message.chat.id] = {}
            dicSarrera[update.message.chat.id]['Emoji'] = stEmoji
            time.sleep(1)
            update.message.reply_text('Esamoldea orain:')
            return ESAMOLDE


def esamolde(update: Update, context: CallbackContext) -> int:
    """Esamoldea gorde eta goitizena eskatu"""
    stEsamolde = update.message.text
    bHasEmoji = False
    for kar in stEsamolde:
        if emo.is_emoji(kar):
            bHasEmoji = True
            break
    if bHasEmoji:
        update.message.reply_text('Lastima! Esamoldeak ezin du emojirik izan bere baitan. Saiatu berriro ala /utzi')
        return ESAMOLDE
    elif len(stEsamolde) >= 41:
        update.message.reply_text('Esamoldeak, asko jota, 40 karaktere izan behar ditu. Saiatu berriro ala /utzi')
        return ESAMOLDE
    else:
        dicSarrera[update.message.chat.id]['Esamolde'] = stEsamolde
        time.sleep(1)
        update.message.reply_text(
            '\U0001F926\U0001F3FB\U0000200D\U00002642\U0000FE0F')  # U+1F3FC #'\U0001F926\U0000200D\U00002642\U0000FE0F'
        time.sleep(1)
        update.message.reply_text('Benetan?')
        time.sleep(3.5)
        update.message.reply_text('\U0001F923 \U0001F923 \U0001F923')
        update.message.reply_text('Txantxetan ari naiz, lasai; okerragoak irakurri ditut \U0001F609')
        time.sleep(2)
        update.message.reply_text('Zein da zure goitizena?')
        return GOITIZEN


def goitizen(update: Update, context: CallbackContext) -> int:
    """Goitizena gorde eta goitizena eskatu"""
    stGoitizen = update.message.text
    if stGoitizen == 'top' or stGoitizen == "TOP":
        update.message.reply_text('Lastima; gako-hitza da hori')
        update.message.reply_text('Saiatu berriro ala /utzi')
    elif len(stGoitizen) > 15:
        update.message.reply_text('Abizen bizkaitarrik ez, mesedez; 15 karaktere gehienez \U0001F648')
        update.message.reply_text('Saiatu berriro ala /utzi')
        return GOITIZEN
    else:
        dicSarrera[update.message.chat.id]['Goitizen'] = stGoitizen
        stId = fernet.encrypt(bytes(str(update.message.from_user['id']), 'utf-8'))
        dicSarrera[update.message.chat.id]['Sortzaile'] = stId
        dicSarrera[update.message.chat.id]['AzkenErabiltzaile'] = stId
        update.message.reply_text('Eta zure herria?')
        return HERRI


def herri(update: Update, context: CallbackContext) -> int:
    """Herria gorde eta elkarrizketa amaitu"""
    stHerri = update.message.text
    if stHerri == 'top' or stHerri == "TOP":
        update.message.reply_text('Lastima; gako-hitza da hori')
        update.message.reply_text('Saiatu berriro ala /utzi')
    elif len(stHerri) > 18:
        update.message.reply_text('Dedio! Ataun baino luzeagoa da hori!')
        update.message.reply_text('Gehienez, 18 karaktere onartuko dira. Saiatu berriro ala /utzi')
        return HERRI
    else:
        dicSarrera[update.message.chat.id]['Herri'] = stHerri
        """Denbora gorde, ttantoak hasieratu eta sarrera berariazko zerrendei gehitu. Zerrenda sortu existitzen ez bada"""
        if dicSarrera[update.message.chat.id][
            'Emoji'] not in db.list_collection_names():  # Emoji horretara gehitzen den lehen aldian egin beharrekoa
            dicSarrera[update.message.chat.id]['BatezbesteLuze'] = 1 / 3456  # 12 egunean behin
        else:  # Jada daturik badago, BatezbesteLuze zerrendakoen batezbestekoa izango da.
            dicSarrera[update.message.chat.id]['BatezbesteLuze'] = \
                list(db[dicSarrera[update.message.chat.id]['Emoji']].aggregate(
                    [{'$group': {'_id': None, 'batezbeste': {'$avg': '$BatezbesteLuze'}}}]))[0][
                    'batezbeste']
        dicSarrera[update.message.chat.id]['_id'] = str(datetime.datetime.now())
        dicSarrera[update.message.chat.id]['Ttantto'] = 0
        dicSarrera[update.message.chat.id]['TtanttoTarte'] = 0
        dicSarrera[update.message.chat.id]['BatezbesteMotz'] = 0
        print(dicSarrera[update.message.chat.id])
        db[dicSarrera[update.message.chat.id]['Emoji']].insert_one(dicSarrera.pop(update.message.chat.id))  # DBan sartu eta gero dicSarrerako erabiltzaileari dagokion gakoa borratu egingo da

        update.message.reply_text('\U0001F3CC\U0000FE0F\U0000200D\U00002640\U0000FE0F')
        time.sleep(3.5)
        update.message.reply_text('-------------\U0001F386'.rjust(5))
        update.message.reply_text('-------------------------\U0001F387')
        time.sleep(0.3)
        update.message.reply_text('\U0001F30C')
        update.message.reply_text('\U0001F30C')
        update.message.reply_text('\U0001F30C')
        time.sleep(2)
        update.message.reply_text('---------\U0001F387')
        time.sleep(0.1)
        update.message.reply_text('-----\U0001F386')
        time.sleep(0.5)
        update.message.reply_text('----------------------------------\U0001F386')
        update.message.reply_text('---------------------------\U0001F387')
        update.message.reply_text('----------------------------------------\U0001F387')
        update.message.reply_text('-----------------------------------------------------------------\U0001F386')
        time.sleep(0.3)
        update.message.reply_text('\U0001F632\U0001F632\U0001F632\U0001F632\U0001F632\U0001F632\U0001F632')
        update.message.reply_text('\U0001F632\U0001F632\U0001F632\U0001F632\U0001F632\U0001F632\U0001F632')
        time.sleep(1.5)
        update.message.reply_text('\U0001F4A5')
        time.sleep(0.3)
        update.message.reply_text('\U0001F4A5')
        time.sleep(0.3)
        update.message.reply_text('\U0001F4A5')
        update.message.reply_text('Mila esker zure sarrerarengatik! Berehala izango da erabilgarri')

        return ConversationHandler.END


def oharra(update: Update, context: CallbackContext) -> int:
    """Elkarrizketa hasi eta esamoji berria sortzeko beharrezko datuak eskatuko dizkio"""
    update.message.reply_text('\U0001F916')
    time.sleep(0.5)
    update.message.reply_text(
        'Laudorio/iruzkin/iradokizunetarako, sakatu "1"\n'
        'Birao/mehatxu/bonba-gutunetarako, sakatu "2"\n'
        'Prozesua eteteko, /utzi'
    )
    return DIAL


def dial(update: Update, context: CallbackContext) -> int:
    stDial = update.message.text
    if stDial == '1':
        update.message.reply_text("Bota, ba, bota beharrekoa:")
        return ERANTZUN
    elif stDial == '2':
        update.message.reply_text('\U0001F4A5\U0001F4A5\U0001F4A5\U0001F4A5\U0001F4A5')
        update.message.reply_text('-----------------------------------------------\U0001F9B5')  # Hanka
        update.message.reply_text('------------------------\U0001F643')  # Burua buruz behera
        update.message.reply_text('------------------------\U0001F9E0')  # Burmuina
        update.message.reply_text('----------\U0001F44B')  # Eskua
        update.message.reply_text('----------------------------------------------------------------\U0001F9B6')  # Oina
        update.message.reply_text('-------------------------------------------------\U0001F4AA')  # Besoa
        update.message.reply_text('--------------\U0001FAC1')  # Birikak
        update.message.reply_text('---------------------------\U0001F442')  # Belarria
        time.sleep(2)
        update.message.reply_text('\U0001F441-------------------------------------')  # Begia
        time.sleep(0.5)
        update.message.reply_text('\U0001FAC0---------')  # Bihotza
        time.sleep(2)
        update.message.reply_text('\U0001F612 ibili... \U0001F612')
        return ConversationHandler.END
    else:
        update.message.reply_text('"1" edo "2", motel. Ez da hain zaila')
        return DIAL


def erantzun(update: Update, context: CallbackContext) -> int:
    stOhar = update.message.text
    print(stOhar)
    context.bot.send_message(chat_id=settings.MY_TELEGRAM_USER, text='#feedback: ' + stOhar)
    update.message.reply_text("Mila esker. Kontuan hartuko dut (ala ez)")
    return ConversationHandler.END


def utzi(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    update.message.reply_text(
        'Aio! Hurrengora arte!'
    )
    del dicSarrera[update.message.chat.id]
    return ConversationHandler.END


# EMOJI, ESAMOLDE, GOITIZEN, HERRI egoeradun elkarrizketa kudeatzailea sortu eta gehitu
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('gehitu', gehitu)],
    states={
        EMOJI: [MessageHandler(Filters.text & ~Filters.command, emoji)],
        ESAMOLDE: [MessageHandler(Filters.text & ~Filters.command, esamolde)],
        GOITIZEN: [MessageHandler(Filters.text & ~Filters.command, goitizen)],
        HERRI: [MessageHandler(Filters.text & ~Filters.command, herri)],
    },
    fallbacks=[CommandHandler('utzi', utzi)],
)

# Oharretarako elkarrizketa kudeatzailea

conv_handler_oharra = ConversationHandler(
    entry_points=[CommandHandler('oharra', oharra)],
    states={
        DIAL: [MessageHandler(Filters.text & ~Filters.command, dial)],
        ERANTZUN: [MessageHandler(Filters.text & ~Filters.command, erantzun)],
    },
    fallbacks=[CommandHandler('utzi', utzi)],
)
