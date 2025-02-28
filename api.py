#!/usr/bin/env python3

from flask import Flask, request
import flask_restful
import logging
import spacy
import pythainlp
import epitran as epitran_module
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(
    dsn="https://a12aca189f024156b8ff4ac1bb2b9e39@o968582.ingest.sentry.io/6758293",
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=0.25
)

logging.basicConfig(format='%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y%m%d-%H:%M:%S',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

app = Flask(__name__)
api = flask_restful.Api(app)

class SpacyManager():
    def __init__(self):
        self.engines = {}

        logger.info('loading engines')

        import en_core_web_trf
        self.engines['en'] = en_core_web_trf.load()
        import fr_dep_news_trf
        self.engines['fr'] = fr_dep_news_trf.load()
        import ja_core_news_lg
        self.engines['ja'] = ja_core_news_lg.load()
        import de_dep_news_trf
        self.engines['de'] = de_dep_news_trf.load()
        import es_dep_news_trf
        self.engines['es'] = es_dep_news_trf.load()
        import ru_core_news_lg
        self.engines['ru'] = ru_core_news_lg.load()
        import pl_core_news_lg
        self.engines['pl'] = pl_core_news_lg.load()
        import it_core_news_lg
        self.engines['it'] = it_core_news_lg.load()
        import ko_core_news_lg
        self.engines['ko'] = ko_core_news_lg.load()
        # chinese models
        import spacy.lang.zh
        self.engines['zh_char'] = spacy.lang.zh.Chinese()
        self.engines['zh_jieba'] = spacy.lang.zh.Chinese.from_config({"nlp": {"tokenizer": {"segmenter": "jieba"}}})
        nlp = spacy.lang.zh.Chinese.from_config({"nlp": {"tokenizer": {"segmenter": "pkuseg"}}})
        nlp.tokenizer.initialize(pkuseg_model="mixed")
        self.engines['zh_pkuseg'] = nlp

        logger.info('finished loading engines')

    def language_list(self):
        return list(self.engines.keys())

    def tokenize(self, language, text):
        nlp_engine = self.engines[language]

        doc = nlp_engine(text)
        result = []
        for token in doc:
            lemma = token.lemma_
            if len(lemma) == 0:
                lemma = str(token)
            pos_description = spacy.explain(token.tag_)
            entry = {
                'token': str(token),
                'lemma': lemma,
                'can_translate': token.is_alpha,
                'can_transliterate': token.is_alpha
            }
            if pos_description != None:
                entry['pos_description'] = pos_description
            result.append(entry)
        return result        


spacy_manager = SpacyManager()

# spacy endpoints
# ===============

class SpacyTokenize(flask_restful.Resource):
    def post(self):
        data = request.json
        return spacy_manager.tokenize(data['language'], data['text'])

class SpacyLanguageList(flask_restful.Resource):
    def get(self):
        return spacy_manager.language_list()

# pythaiNLP endpoints
# ===================

class PythaiNLPTransliterate(flask_restful.Resource):
    def post(self):
        data = request.json
        text = data['text']
        return pythainlp.transliterate(text)

class PythaiNLPRomanize(flask_restful.Resource):
    def post(self):
        data = request.json
        text = data['text']
        return pythainlp.romanize(text, engine='thai2rom')

class PythaiNLPWordTokenize(flask_restful.Resource):
    def post(self):
        data = request.json
        text = data['text']
        return pythainlp.word_tokenize(text)

# EpiTran endpoints
# =================

class EpitranTransliterate(flask_restful.Resource):
    def post(self):
        data = request.json
        language_code = data['language_code']
        text = data['text']
        epi = epitran_module.Epitran(language_code)
        return epi.transliterate(text)


# other endpoints
# ===============

class Health(flask_restful.Resource):
    def get(self):
        return {'status': 'OK'}, 200


# spacy
api.add_resource(SpacyTokenize, '/spacy/v1/tokenize')
api.add_resource(SpacyLanguageList, '/spacy/v1/language_list')
# pythainlp
api.add_resource(PythaiNLPTransliterate, '/pythainlp/v1/transliterate')
api.add_resource(PythaiNLPRomanize, '/pythainlp/v1/romanize')
api.add_resource(PythaiNLPWordTokenize, '/pythainlp/v1/word_tokenize')
# epitran
api.add_resource(EpitranTransliterate, '/epitran/v1/transliterate')
# health
api.add_resource(Health, '/_health')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')