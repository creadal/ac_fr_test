from telegram.ext import Updater
import logging
from telegram.ext import MessageHandler
from telegram.ext.filters import Filters
from pathlib import Path
import soundfile as sf
import subprocess
from os import listdir
from os import remove
from os.path import isfile, join
import face_recognition



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


updater = Updater(token='1182597894:AAEPIBt9WHSfz0ukUxTzOVpZEq1JzoOyDyY', use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def download_voice(update, context):
    file = context.bot.getFile(update.message.voice.file_id)
    print("file_id: " + str(update.message.voice.file_id))

    path = '{}/{}'.format(update.message.chat.username, update.message.voice.file_id + '.oga')

    Path(update.message.chat.username).mkdir(parents=True, exist_ok=True)
    file.download(path)

    onlyfiles = [f for f in listdir(update.message.chat.username + '/') if isfile(join(update.message.chat.username + '/', f)) and f.split('.')[-1] == 'wav']
    if len(onlyfiles) > 0:
        ind = max([int(f.split('.')[0].split('_')[-1]) for f in onlyfiles]) + 1
    else:
        ind = 0

    src_filename = update.message.chat.username + '/' + update.message.voice.file_id + '.oga'
    dest_filename = update.message.chat.username + '/' + 'audio_message_' + str(ind) + '.wav'

    process = subprocess.run(['ffmpeg', '-i', src_filename,  '-ar', '16000', dest_filename])
    if process.returncode != 0:
        raise Exception("Something went wrong")

    remove(src_filename)


def find_face(update, context):
    file = context.bot.getFile(update.message.photo[0].file_id)
    file.download(update.message.photo[0].file_id + '.jpg')

    image = face_recognition.load_image_file(update.message.photo[0].file_id + '.jpg')
    face_locations = face_recognition.face_locations(image)

    if len(face_locations) == 0:
        remove(update.message.photo[0].file_id + '.jpg')



voice_handler = MessageHandler(Filters.voice, download_voice)
face_handler = MessageHandler(Filters.photo, find_face)

dispatcher.add_handler(voice_handler)
dispatcher.add_handler(face_handler)

updater.start_polling()
