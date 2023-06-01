from flask import Flask, request, render_template
import os
import requests, json

global translator_endpoint    
global cog_key    
global cog_region

try:
    cog_key = os.environ.get("COG_SERVICE_KEY")
    cog_region = os.environ.get("COG_SERVICE_REGION")      
    translator_endpoint = 'https://api.cognitive.microsofttranslator.com'   
except Exception as ex:        
    print(ex)

def detect_language(text):
    api_url = translator_endpoint + '/detect?api-version=3.0'
    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-Type': 'application/json'
    }
    body = [{'text': text}]
    response = requests.post(api_url, headers=headers, json=body)
    result = response.json()
    language = result[0]['language']
    return language

def translate_text(text, target_language):
    api_url = translator_endpoint + '/translate?api-version=3.0&to=' + target_language
    headers = {
        'Ocp-Apim-Subscription-Key': cog_key,
        'Ocp-Apim-Subscription-Region': cog_region,
        'Content-Type': 'application/json'
    }
    body = [{'text': text}]
    response = requests.post(api_url, headers=headers, json=body)
    result = response.json()
    translated_text = result[0]['translations'][0]['text']
    return translated_text

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        text = request.form['text']
        source_language = detect_language(text)
        translated_text = translate_text(text, 'en')  # Cambia 'en' por el idioma objetivo deseado
        
        return render_template('home.html', translated_text=translated_text, lang_detected=source_language)
    
    return render_template('home.html')

if __name__ == "__main__":
    app.run(debug=True)
