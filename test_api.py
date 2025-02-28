import os
import unittest
import json
import pprint
import requests
from api import app

# testing an external URL:
# SPACY_API_EXTERNAL_URL=http://localhost:8042 pytest test_api.py

class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super(ApiTests, cls).setUpClass()
        
        external_url = os.environ.get('SPACY_API_EXTERNAL_URL', None)
        if external_url == None:
            cls.client = app.test_client()
            cls.external_url = None
        else:
            cls.external_url = external_url

    @classmethod
    def tearDownClass(cls):
        pass

    def get_query(self, path):
        if self.external_url != None:
            response = requests.get(self.external_url + path, timeout=10)
            response.raise_for_status()
            return response.json()
        else:
            response = self.client.get(path)
            return json.loads(response.data)

    def post_query(self, path, data):
        if self.external_url != None:
            response = requests.post(self.external_url + path, json=data, timeout=10)
            response.raise_for_status()
            return response.json()
        else:
            response = self.client.post(path, json=data)
            return json.loads(response.data)

    def test_languages(self):
        data = self.get_query('/spacy/v1/language_list')
        self.assertIn('en', data)

    def test_spacy_tokenize_english(self):
        text = "I was reading today's paper."

        data = self.post_query('/spacy/v1/tokenize', {'language': 'en', 'text': text})

        pprint.pprint(data)
        
        expected_result = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': 'I',
            'pos_description': 'pronoun, personal',
            'token': 'I'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'be',
            'pos_description': 'verb, past tense',
            'token': 'was'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'read',
            'pos_description': 'verb, gerund or present participle',
            'token': 'reading'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'today',
            'pos_description': 'noun, singular or mass',
            'token': 'today'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': "'s",
            'pos_description': 'possessive ending',
            'token': "'s"},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'paper',
            'pos_description': 'noun, singular or mass',
            'token': 'paper'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': '.',
            'pos_description': 'punctuation mark, sentence closer',
            'token': '.'}]
        
        self.assertEqual(data, expected_result)        

    def test_spacy_tokenize_french(self):
        text = "Le nouveau plan d’investissement du gouvernement."

        data = self.post_query('/spacy/v1/tokenize', data={'language': 'fr', 'text': text})

        pprint.pprint(data)
        
        expected_result = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': 'le',
            'pos_description': 'determiner',
            'token': 'Le'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'nouveau',
            'pos_description': 'adjective',
            'token': 'nouveau'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'plan',
            'pos_description': 'noun',
            'token': 'plan'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': 'd’',
            'pos_description': 'adposition',
            'token': 'd’'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'investissement',
            'pos_description': 'noun',
            'token': 'investissement'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'de',
            'pos_description': 'adposition',
            'token': 'du'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': 'gouvernement',
            'pos_description': 'noun',
            'token': 'gouvernement'},
            {'can_translate': False,
            'can_transliterate': False,
            'lemma': '.',
            'pos_description': 'punctuation',
            'token': '.'}]
        
        self.assertEqual(data, expected_result)                

    def test_spacy_tokenize_chinese_chars(self):
        text = "送外卖的人"

        data = self.post_query('/spacy/v1/tokenize', data={'language': 'zh_char', 'text': text})

        expected_result_chars = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': '送',
            'token': '送'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '外',
            'token': '外'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '卖',
            'token': '卖'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '的',
            'token': '的'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '人',
            'token': '人'}]
        
        self.assertEqual(data, expected_result_chars)                


    def test_spacy_tokenize_chinese_words(self):
        text = "送外卖的人"

        data = self.post_query('/spacy/v1/tokenize', data={'language': 'zh_jieba', 'text': text})

        expected_result_words = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': '送',
            'token': '送'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '外卖',
            'token': '外卖'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '的',
            'token': '的'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '人',
            'token': '人'}]

        self.assertEqual(data, expected_result_words)

    def test_spacy_tokenize_chinese_words_pkuseg(self):
        text = "送外卖的人"

        data = self.post_query('/spacy/v1/tokenize', data={'language': 'zh_pkuseg', 'text': text})

        expected_result_words = [{'can_translate': True,
            'can_transliterate': True,
            'lemma': '送',
            'token': '送'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '外卖',
            'token': '外卖'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '的',
            'token': '的'},
            {'can_translate': True,
            'can_transliterate': True,
            'lemma': '人',
            'token': '人'}]

        self.assertEqual(data, expected_result_words)        

    def test_spacy_more_languages(self):
        input_sentences = [
            {
                'sentence': 'There are many foreigners in China',
                'language_code': 'en'
            },
            {
                'sentence': 'Je ne suis pas intéressé.',
                'language_code': 'fr'
            },
            {
                'sentence': '천천히 말해 주십시오',
                'language_code': 'ko'
            },
            {
                'sentence': '中国有很多外国人',
                'language_code': 'zh_char'
            },
            {
                'sentence': 'おはようございます',
                'language_code': 'ja'
            },
            {
                'sentence': 'улица',
                'language_code': 'ru'
            },
            {
                'sentence': 'Ich esse kein Schweinefleisch.',
                'language_code':'de'
            },
            {
                'sentence': "Qual è l'ora di chiusura?",
                'language_code': 'it'
            }

        ]

        for input_sentence in input_sentences:
            text = input_sentence['sentence']
            language = input_sentence['language_code']
            data = self.post_query('/spacy/v1/tokenize', data={'language': language, 'text': text})
            self.assertTrue(len(data) > 0)

    def test_health(self):
        data = self.get_query('/_health')
        self.assertEqual(data, {'status': 'OK'})

    # pythainlp
    def test_pythainlp_transliterate(self):
        data = self.post_query('/pythainlp/v1/transliterate', data={'text': 'สวัสดี'})
        self.assertEqual(data, 's a ˧ . w a t̚ ˨˩ . d iː ˧')

    def test_pythainlp_romanize(self):
        data = self.post_query('/pythainlp/v1/romanize', data={'text': 'สวัสดี'})
        self.assertEqual(data, 'sawatdi')

    def test_pythainlp_tokenize(self):
        data = self.post_query('/pythainlp/v1/word_tokenize', data={'text': 'ดิฉันอายุยี่สิบเจ็ดปีค่ะ'})
        self.assertEqual(data, ['ดิฉัน', 'อายุ', 'ยี่สิบ', 'เจ็ด', 'ปี', 'ค่ะ'])