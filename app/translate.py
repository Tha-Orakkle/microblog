from flask import current_app
from flask_babel import _
import requests


def translate(text, source_language, dest_language):
    """helper function to translate text to another language"""
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = {
        'Ocp-Apim-Subscription-Key': current_app.config['MS_TRANSLATOR_KEY'],
        'Ocp-Apim-Subscription-Region': 'westus'
    }

    r = requests.post(
        'https://api.cognitive.microsofttranslator.com'
        '/translate?api-version=3.0&from={}&to={}'.format(
            source_language, dest_language), headers=auth,
        json=[{'Text': text}])

    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return r.json()[0]['translation'][0]['text']
