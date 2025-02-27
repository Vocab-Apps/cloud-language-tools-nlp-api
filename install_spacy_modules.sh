#!/bin/bash

set -euxo pipefail

python3 -m spacy download en_core_web_trf
python3 -m spacy download fr_dep_news_trf
python3 -m spacy download zh_core_web_trf
python3 -m spacy download ja_core_news_lg
python3 -m spacy download de_dep_news_trf
python3 -m spacy download es_dep_news_trf
python3 -m spacy download ru_core_news_lg
python3 -m spacy download pl_core_news_lg
python3 -m spacy download it_core_news_lg
python3 -m spacy download ko_core_news_lg