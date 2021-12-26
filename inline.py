import emoji as emo
from settings import db, lstJoeraEmo, fernet
from telegram import InlineQueryResultArticle, InputTextMessageContent, Update
from telegram.ext import CallbackContext


def fnJoera(lstJoera) -> dict:
    """Joerako emotikonoak esleitzeko funtzioa. lst jaso ta dic itzuli"""
    delta = (len(lstJoeraEmo) - 1) / len(
        lstJoera)  # Bakarra dagonean perretxikoa ateratzea lehenestu da. Eta ovnia aukera asko baino ez daudenean lortzea.
    dicMotz = {}
    for i in range(len(lstJoera)):
        dicMotz[lstJoera[i]['_id']] = lstJoeraEmo[round((i + 1) * delta)]
    return dicMotz


def inlinequery(update: Update, context: CallbackContext) -> None:
    """Handle the inline query."""
    stQuery = update.inline_query.query
    if emo.is_emoji(stQuery):
        results = []
        if stQuery in db.list_collection_names():
            lstColLuze = list(db[stQuery].find().sort('BatezbesteLuze', -1))
            dicMotz = fnJoera(list(db[stQuery].find({}, {'_id': 1}).sort('BatezbesteMotz', -1)))
            for dic in lstColLuze:  # dokumentu kopuruaren arabera iteratu
                results.append(
                    InlineQueryResultArticle(
                        id=dic['Emoji'] + '_' + dic['_id'],
                        title=dic['Esamolde'],
                        description=dicMotz[dic['_id']] + '(' + str(dic['Ttantto']) + ') ' + '| \U0001F636 ' + dic[
                            'Goitizen'] + ' |\U0001F4CD' +
                                    dic['Herri'],
                        # U+2B06 gora;  U+2B07 behera; U+1F636 begiak bakarrik; U+1F4CD txintxeta (kokalekua)
                        thumb_url=None,
                        thumb_width=None,
                        thumb_height=None,
                        input_message_content=InputTextMessageContent(
                            stQuery + " " + dic['Esamolde'] + " " + stQuery))
                )
        else:
            results.append(
                InlineQueryResultArticle(
                    id='EzAurkitua',
                    title=' \U000026A0 ez da sarrerarik aurkitu \U000026A0',  # \U000026A0',
                    description='Saiatu beste batekin edo...',
                    thumb_url=None,
                    thumb_width=None,
                    thumb_height=None,
                    input_message_content=InputTextMessageContent('\U0001F4A9'))
            )
        results.append(
            InlineQueryResultArticle(
                id="argibideak",
                title=" Bota esamojia!",
                description='Esamoji bat gehitzeko hitz egin @esamojiBot botarekin; bila ezazu elkarrizketa artean'
                            ' (goiko barran) eta esaiozu /gehitu.',
                # U+2B06 gora;  U+2B07 behera; U+1F636 begiak bakarrik; U+1F4CD txintxeta (kokalekua)
                thumb_url=None,
                thumb_width=None,
                thumb_height=None,
                input_message_content=InputTextMessageContent('Esamoji bat gehitzeko hitz egin @esamojiBot '
                                                              'botarekin; bila ezazu elkarrizketa artean eta'
                                                              ' esaiozu /gehitu.'))
        )
        update.inline_query.answer(results)
    elif stQuery == 'top':
        results = []
        lstColLuze = list(db.Top.find().sort('BatezbesteLuze', -1).limit(49))
        dicMotz = fnJoera(list(db.Top.find({}, {'_id': 1}).sort('BatezbesteMotz', -1)))
        for dic in lstColLuze:  # dokumentu kopuruaren arabera iteratu
            results.append(
                InlineQueryResultArticle(
                    id=dic['Emoji'] + '_' + dic['_id'],
                    title=dic['Esamolde'],
                    description=dicMotz[dic['_id']] + '(' + str(dic['Ttantto']) + ') ' + '| \U0001F636 ' + dic[
                        'Goitizen'] + ' |\U0001F4CD' +
                                dic['Herri'] + ' | ' + dic['Emoji'],
                    # U+2B06 gora;  U+2B07 behera; U+1F636 begiak bakarrik; U+1F4CD txintxeta (kokalekua)
                    thumb_url=None,
                    thumb_width=None,
                    thumb_height=None,
                    input_message_content=InputTextMessageContent(
                        dic['Emoji'] + " " + dic['Esamolde'] + " " + dic['Emoji']))
            )
        results.append(
            InlineQueryResultArticle(
                id="argibideak",
                title=" Bota esamojia!",
                description='Esamoji bat gehitzeko hitz egin @esamojiBot botarekin; bila ezazu elkarrizketa artean'
                            ' (goiko barran) eta esaiozu /gehitu.',
                # U+2B06 gora;  U+2B07 behera; U+1F636 begiak bakarrik; U+1F4CD txintxeta (kokalekua)
                thumb_url=None,
                thumb_width=None,
                thumb_height=None,
                input_message_content=InputTextMessageContent('Esamoji bat gehitzeko hitz egin @esamojiBot '
                                                              'botarekin; bila ezazu elkarrizketa artean eta'
                                                              ' esaiozu /gehitu.'))
        )
        update.inline_query.answer(results)
    elif 18 >= len(stQuery) > 0:
        for stCol in db.list_collection_names():
            if stCol != "Top":
                lstColBila = list(db[stCol].find({'$or': [{'Goitizen': stQuery}, {'Herri': stQuery}]}))
                if len(lstColBila) != 0:
                    for dic in lstColBila:
                        db[stQuery].insert_one(dic)
        results = []
        if stQuery in db.list_collection_names():  # Bilaketa bilduma batu berri bada
            lstColLuze = list(db[stQuery].find().sort('BatezbesteLuze', -1).limit(49))
            dicMotz = fnJoera(list(db[stQuery].find({}, {'_id': 1}).sort('BatezbesteMotz', -1)))
            db[stQuery].drop()
            for dic in lstColLuze:  # dokumentu kopuruaren arabera iteratu
                results.append(
                    InlineQueryResultArticle(
                        id=dic['Emoji'] + '_' + dic['_id'],
                        title=dic['Esamolde'],
                        description=dicMotz[dic['_id']] + '(' + str(dic['Ttantto']) + ') ' + '| \U0001F636 ' + dic[
                            'Goitizen'] + ' |\U0001F4CD' +
                                    dic['Herri'] + ' | ' + dic['Emoji'],
                        # U+2B06 gora;  U+2B07 behera; U+1F636 begiak bakarrik; U+1F4CD txintxeta (kokalekua)
                        thumb_url=None,
                        thumb_width=None,
                        thumb_height=None,
                        input_message_content=InputTextMessageContent(
                            dic['Emoji'] + " " + dic['Esamolde'] + " " + dic['Emoji']))
                )
            results.append(
                InlineQueryResultArticle(
                    id="argibideak",
                    title=" Bota esamojia!",
                    description='Esamoji bat gehitzeko hitz egin @esamojiBot botarekin; bila ezazu elkarrizketa artean'
                                ' (goiko barran) eta esaiozu /gehitu.',
                    # U+2B06 gora;  U+2B07 behera; U+1F636 begiak bakarrik; U+1F4CD txintxeta (kokalekua)
                    thumb_url=None,
                    thumb_width=None,
                    thumb_height=None,
                    input_message_content=InputTextMessageContent('Esamoji bat gehitzeko hitz egin @esamojiBot '
                                                                  'botarekin; bila ezazu elkarrizketa artean eta'
                                                                  ' esaiozu /gehitu.'))
            )
        else:
            results.append(
                InlineQueryResultArticle(
                    id='EzAurkitua',
                    title=' \U000026A0 ez da sarrerarik aurkitu \U000026A0',  # \U000026A0',
                    description='Saiatu beste batekin edo...',
                    thumb_url=None,
                    thumb_width=None,
                    thumb_height=None,
                    input_message_content=InputTextMessageContent('\U0001F4A9'))
            )
            results.append(
                InlineQueryResultArticle(
                    id="argibideak",
                    title=" Bota esamojia!",
                    description='Esamoji bat gehitzeko hitz egin @esamojiBot botarekin; bila ezazu elkarrizketa artean'
                                ' (goiko barran) eta esaiozu /gehitu.',
                    # U+2B06 gora;  U+2B07 behera; U+1F636 begiak bakarrik; U+1F4CD txintxeta (kokalekua)
                    thumb_url=None,
                    thumb_width=None,
                    thumb_height=None,
                    input_message_content=InputTextMessageContent('Esamoji bat gehitzeko hitz egin @esamojiBot '
                                                                  'botarekin; bila ezazu elkarrizketa artean eta'
                                                                  ' esaiozu /gehitu.'))
            )
        update.inline_query.answer(results)


def chosen(update: Update, context: CallbackContext) -> None:
    # Ttantto bat gehitu aukeratutako dokumentuari
    [stCol, stId] = update.chosen_inline_result.result_id.split('_')
    stUser = update.chosen_inline_result.from_user
    bErabiltzaile = bytes(str(update.chosen_inline_result.from_user.id), 'utf-8')
    if fernet.decrypt(db[stCol].find_one({'_id': stId})['AzkenErabiltzaile']) != bErabiltzaile and fernet.decrypt(
            db[stCol].find_one({'_id': stId})['Sortzaile']) != bErabiltzaile or bErabiltzaile == bytes(settings.MY_TELEGRAM_USER,
                                                                                                       'UTF-8'):  # ALDATU HAU!!! Nire ereabiltzailea salbu! ("or"aren bidez)
        db[stCol].update_one({'_id': stId}, {'$inc': {'Ttantto': 1}}, upsert=False)
        db[stCol].update_one({'_id': stId}, {'$inc': {'TtanttoTarte': 1}}, upsert=False)
        db[stCol].update_one({'_id': stId}, {'$set': {'AzkenErabiltzaile': fernet.encrypt(bErabiltzaile)}},
                             upsert=False)
