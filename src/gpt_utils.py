import time
from openai import OpenAI
import numpy as np
import tiktoken
import os
import pandas as pd
import re


def load_file(path):
  if path.endswith(".txt"):
      with open(path, 'r', encoding='utf-8') as file:
        return file.read().strip()
  raise Exception("Sorry, the file must be a txt")


def load_from_folder(folder):

  files = os.listdir(folder)
  return [(file_name, load_file(os.path.join(folder, file_name))) for file_name in files if file_name.endswith(".txt")]


def ask_gpt(prompt, KEY, model="gpt-4-turbo-preview", max_tokens=100, temperature=0.4):

    client = OpenAI(api_key=KEY)
    try:
        time.sleep(10)
        response = client.chat.completions.create(
            model=model,
            messages = [{"role": "user", "content": x} for x in prompt],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
      print(e)


def count_tokens(text, model="gpt-4-turbo-preview"):
  return len(tiktoken.encoding_for_model(model).encode(text))


def build_embedding(text, model="text-embedding-3-large"):

    client = OpenAI(api_key=KEY)
    try:
        time.sleep(0.3)
        response = client.embeddings.create(
            model=model,
            input=text
        )
        return np.array(response.data[0].embedding)
    except Exception as e:
      print(e)


def cosine_similarity(embedding_a, embedding_b):
    return np.dot(embedding_a, embedding_b) / (np.linalg.norm(embedding_a) * np.linalg.norm(embedding_b))

def find_most_similar_k(k, df, text):
    y = build_embedding(text)
    df["similarity"] = df["embedding"]
    df["similarity"] = df["similarity"].apply(lambda x : cosine_similarity(x, y))

    return df.sort_values(by=['similarity'], ascending=False) \
        .reset_index() \
        .head(n=k)


# Configured for deterministic output
def ask_gpt_2(prompt, system_prompt, KEY, top_p = 0.1, model="gpt-4-turbo-preview", max_tokens=100, temperature=0.2):

  client = OpenAI(api_key=KEY)
  try:
      response = client.chat.completions.create(
          model=model,
          messages = [{"role": "system", "content": system_prompt},
                      {"role": "user", "content": prompt}] ,
          temperature=temperature,
          top_p = top_p,
          max_tokens=max_tokens
      )
      return response.choices[0].message.content
  except Exception as e:
    print(e)



