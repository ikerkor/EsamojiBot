from dotenv import load_dotenv
import os
import pymongo
import logging
from cryptography.fernet import Fernet

# Ingurune-aldagaiak zamatu, .env fitxategirik badago
load_dotenv()

# Herokun edo lokalean ari garen jakiteko

HEROKU = os.environ.get('HEROKU')

# Telegram bot TOKEN and my user
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
MY_TELEGRAM_USER = os.environ.get('MY_TELEGRAM_USER')

# Set the port number to listen in for the webhook
PORT = int(os.environ.get('PORT', 8443))

# Enable loggingencrypted
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# dbEsamojiak mongoDB datu-basea atzitu
MONGODB_CLUSTER = os.environ.get('MONGODB_CLUSTER')
client = pymongo.MongoClient("mongodb+srv://ikerkor:" + MONGODB_CLUSTER + "@cluster0.icmmd.mongodb.net/dbEsamojiak?retryWrites=true&w=majority")
db = client['dbEsamojiak']

# Zifratze gakoa atzitu eta ferneta sortu
ESAMOJIAK_KEY = os.environ.get('ESAMOJIAK_KEY')
fernet = Fernet(ESAMOJIAK_KEY)

#Aldagai globalak
lstJoeraEmo = ['\U0001F6F8', '\U0001F6F8', '\U00002708', '\U0001F681', '\U0001F6A0', '\U0001F9D7', '\U0001F332', '\U0001FAB4', '\U0001F344']  # Emoji joera adierazleak