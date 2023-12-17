import openai 

from bs4 import BeautifulSoup
import streamlit as st
import requests

def chat(theme, question):
    completion = openai.chat.completions.create( model="gpt-4",  messages=[
            {"role": "system","content": f"Tu es un consultant politique qui répond aux questions des journalistes sur le programme de la France Insoumise. Voici la thématique de la question : {theme}"}, 
            {"role": "user", "content": "Voici la question : " + question},
        ])
    return completion.choices[0].message.content

def get_programme():
    url = 'https://nupes-2022.fr/le-programme/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    li = soup.find('main', 
                class_='elementor-column elementor-col-100 elementor-top-column elementor-element elementor-element-3453020'
                ).find('div', class_='elementor-widget-wrap elementor-element-populated')

    programme = [u.text for u in li.find_all('div') if 'data-id' in u.attrs and u.text.replace('\n', '') != '']

    keys = programme[5::2]
    value = programme[6::2]
    return {keys[i][:-1]: value[i] for i in range(len(keys))}