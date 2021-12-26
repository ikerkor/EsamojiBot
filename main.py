import settings, elkarrizketa, inline
from settings import db
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext, \
    MessageHandler, Filters, ChosenInlineResultHandler, JobQueue


def eguneratu(
        context: CallbackContext):  # KONTUZ! job callbacks take exactly one argument of type telegram.ext.CallbackContext
    """Bilduma bakoitzean ttanttoen arabera batezbestekoak eguneratu eta Top bilduma eguneratu"""
    for stCol in db.list_collection_names():
        if stCol != "Top":
            db[stCol].update_many({}, [{"$set": {"BatezbesteLuze":
                                                     {"$add": ['$BatezbesteLuze', {"$divide": [
                                                         {"$subtract": ['$TtanttoTarte', '$BatezbesteLuze']},
                                                         3456]}]}}}])  # <-- Aldatu! Azken 12 eguneko batezbestekoa: 2880
            db[stCol].update_many({}, [{"$set": {"BatezbesteMotz":
                                                     {"$add": ['$BatezbesteMotz', {
                                                         "$divide": [
                                                             {"$subtract": ['$TtanttoTarte', '$BatezbesteMotz']},
                                                             864]}]}}}])  # <-- ALdatu! Azken 3 eguneko batezbestekoa:
            db[stCol].update_many({'TtanttoTarte': {'$gt': 0}}, {'$set': {'TtanttoTarte': 0}}, upsert=False)
    # Top 49 eguneratu
    db.Top.delete_many({})
    for stCol in db.list_collection_names():
        if stCol != "Top":
            lstColLuze = list(db[stCol].find().sort('BatezbesteLuze', -1).limit(2))
            for dic in lstColLuze:
                db.Top.insert_one(dic)
    print('Lana!')


def main() -> None:
    """Run the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater(settings.TELEGRAM_TOKEN)

    '''Lan periodikoa'''
    updater.job_queue.run_repeating(eguneratu, 300, 300, name="eguneratu")  # Berez, 300, 300

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # EMOJI, ESAMOLDE, GOITIZEN, HERRI egoeradun elkarrizketa kudeatzailea sortu eta gehitu.
    dispatcher.add_handler(elkarrizketa.conv_handler)

    # DIAL, ERANTZUN egoeradun elkarrizketa kudeatzailea sortu eta gehitu.
    dispatcher.add_handler(elkarrizketa.conv_handler_oharra)

    # Lerro barneko queryaren kudeatzailea gehitu
    dispatcher.add_handler(InlineQueryHandler(inline.inlinequery))

    # Lerro barneko queryaren emaitzaren kudeatzailea gehitu
    dispatcher.add_handler(ChosenInlineResultHandler(inline.chosen))

    # Hasi bot-a
    if settings.HEROKU == '0':
        updater.start_polling()
    elif settings.HEROKU == '1':
        updater.start_webhook(listen="0.0.0.0",
                              port=int(settings.PORT),
                              url_path=settings.TELEGRAM_TOKEN,
                              webhook_url='https://esamojibot.herokuapp.com/' + settings.TELEGRAM_TOKEN)

    # Block until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
