#!/usr/bin/env python3

# do some initialization as part of the docker build, to allow caching

import spacy
import pythainlp
import epitran as epitran_module
import spacy.lang.zh

# the following will force a download of some datasets

spacy_engines = {}

spacy_engines['zh_char'] = spacy.lang.zh.Chinese()
spacy_engines['zh_jieba'] = spacy.lang.zh.Chinese.from_config({"nlp": {"tokenizer": {"segmenter": "jieba"}}})
nlp = spacy.lang.zh.Chinese.from_config({"nlp": {"tokenizer": {"segmenter": "pkuseg"}}})
nlp.tokenizer.initialize(pkuseg_model="mixed")