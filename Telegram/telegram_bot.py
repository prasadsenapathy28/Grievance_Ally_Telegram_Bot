import os
import openai
import speech_recognition as sr
import tempfile
import shutil
import uuid
import langid
import soundfile as sf
import config
from pydub import AudioSegment
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

bot=Bot(token="6820088220:AAGS67mxxDK5x24OdFgAH7MCYzs6FMVEYDo")
dp=Dispatcher(bot)
openai.api_key="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"


def generate_answer(text_msg):
     response = openai.Completion.create(
        model= "text-davinci-003",
        prompt = text_msg,
        temperature =0.5,
        max_tokens =1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
     return response.choices[0].text
@dp.message_handler(content_types=types.ContentType.VOICE)
async def handle_voice(message: types.Message):
      voice = message.voice
      ogg_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.ogg'
      print(voice)
      file_info = await bot.get_file(voice.file_id)
      file_path = file_info.file_path
      voice_file = await bot.download_file(file_path)
      with open(ogg_file_path, 'wb') as file:
            file.write(voice_file.getvalue())
      audio_data, sample_rate = sf.read(ogg_file_path)
      wav_file_path = f'{config.OUTPUT_DIR}/{uuid.uuid1()}.wav'
      sf.write(wav_file_path, audio_data, sample_rate)
      audio_file = open(wav_file_path, 'rb')
      print(audio_file)
      print(wav_file_path)
      recognizer = sr.Recognizer()
      with sr.AudioFile(wav_file_path) as source:
           audio_data = recognizer.record(source)
      try:
           text_msg = recognizer.recognize_google(audio_data)
           language, confidence = langid.classify(text_msg)
        #    print(language, confidence)
        #    generate_answer(text_msg)
           await message.reply(generate_answer(text_msg))
      except:
           print("Error")
    #   await message.reply("Voice message received and converted to wav!")
      
@dp.message_handler(commands=['start','help'])
async def welcome(message: types.Message):
    await message.reply('Hello I am Grievnace_Ally Bot, How may I assist you today?')

@dp.message_handler()
async def gpt(message: types.Message):
    
    response = openai.Completion.create(
        model= "text-davinci-003",
        prompt =message.text,
        temperature =0.5,
        max_tokens =1024,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0
        )
    await message.reply(response.choices[0].text)

if __name__ == "__main__":
    executor.start_polling(dp)