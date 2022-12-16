#!pip install openai twilio flask python-dotenv pyngrok flask-ngrok deep-translator
#!ngrok authtoken '1uO2iVVqH8dBYlG8SlkItcTl5Vw_4xgHSffrH6vfVKkiwNhF2'

from random import choice
from flask import Flask, request
import os

from dotenv import load_dotenv
import openai
from deep_translator import GoogleTranslator


load_dotenv()
openai.api_key = ("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")
completion = openai.Completion()

# Chefbot
def ask_chef(start_sequence, restart_sequence, question, chat_log=None):
  prompt_text = f'{chat_log}{restart_sequence}{question}{start_sequence}'
  response = openai.Completion.create(
#    engine="davinci",
    model="text-davinci-003",
#    model="text-curie-001",
    prompt=prompt_text,
    temperature=0.7,
    max_tokens=96,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0.3,
    stop=["\n"],
  )
  story = response['choices'][0]['text']
  return str(story)

# Friendbot
def ask_friend(start_sequence, restart_sequence, question, chat_log=None):
  prompt_text = f'{chat_log}{restart_sequence}{question}{start_sequence}'
  response = openai.Completion.create(
#      engine="davinci",
    model="text-davinci-003",
#    model="text-curie-001",
    prompt=prompt_text,
    temperature=0.5,
    max_tokens=60,
    top_p=1,
    frequency_penalty=0.5,
    presence_penalty=0,
    stop=["You:"],
  )
  story = response['choices'][0]['text']
  return str(story)

# QNAbot
def ask_qna(start_sequence, restart_sequence, question, chat_log=None):
  prompt_text = f'{chat_log}{restart_sequence}{question}{start_sequence}'
  response = openai.Completion.create(
#      engine="davinci",
    model="text-davinci-003",
#    model="text-curie-001",
    prompt=prompt_text,
    temperature=0,
    max_tokens=100,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0,
    stop=["\n"]
  )
  story = response['choices'][0]['text']
  return str(story)


def image_generator(question, chat_log=None):
  response = openai.Image.create(
    prompt=question,
    n=1,
    size="1024x1024"
  )
  image_url = response['data'][0]['url']
  return str(image_url)

def translate(question,out='id'):
  question = GoogleTranslator(source='auto', target=out).translate(question)  # output -> Weiter so, du bist großartig
  return question

def append_interaction_to_chat_log(start_sequence, restart_sequence, session_prompt, question, answer, chat_log=None):
    if chat_log is None:
        chat_log = session_prompt
    return f'{chat_log}{restart_sequence} {question}{start_sequence}{answer}'
