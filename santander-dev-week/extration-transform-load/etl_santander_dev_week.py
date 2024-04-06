# -*- coding: utf-8 -*-
"""ETL-santander-dev-week.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/144-UO24h0TVZnxUCSIdBACME5xiNG7Dt
"""

sdw2023_api_url = 'https://sdw-2023-prd.up.railway.app'

import pandas as pd
import numpy as np

"""Extract"""

PATH_SDW = '/content/SDW2023.csv'
df = pd.read_csv(PATH_SDW)
user_ids = df['UserID'].tolist() # Devolve todas as informações
print(user_ids)

import requests as rqs # requisição
import json # formatar saidas/ Manipulação dados de retorno/ visualizar

def get_user(id):
  response = rqs.get(f'{sdw2023_api_url}/users/{id}') # uso do get e do path /users/ para devolver o id
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None] # Compreensão de listas [Percorre cada Id da lista de ids user para cada id ele vai fazer uma chamada na função get User// := (formato de uma expressão - limpeza)]
print(json.dumps(users, indent = 2))

!pip install openai==0.28

openia_api_key = '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'

import openai

openai.api_key = openia_api_key

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
      model ='text-davinci-002',
      messages= [
          {
            "role": "system",
            "content": "Você é um especialista em Marketing Bancário."
          },
          {
            "role": "user",
            "content" : f"Crie uma mensagem para o usuário {user['name']} sobre a importancia sobre os investimentos (máximo de 100 caracteres) !"
          }
         ]
       )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)

"""Extract / Transform / Load"""

def update_user(user):
  response = rqs.put(f"{sdw2023_api_url}/users/{user['id']}", json = user)
  return True if response.status_code == 200 else False

for user in users:
  sucess = update_user(user)
  print(f"User {user['name']} update? {sucess}!")