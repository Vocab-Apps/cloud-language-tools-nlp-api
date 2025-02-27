# running locally:
# docker run --name spacy_api -d -p 0.0.0.0:8042:8042/tcp lucwastiaux/spacy-api:20220918-3
# stopping:
# docker container stop spacy_api
# docker container rm spacy_api

FROM python:3.11-slim-bookworm

# update pip
RUN pip3 install --upgrade pip

# install spacy modules
RUN pip3 install --no-cache-dir spacy && pip3 cache purge
RUN python3 -m spacy download en_core_web_trf
RUN python3 -m spacy download fr_dep_news_trf
RUN python3 -m spacy download zh_core_web_trf
RUN python3 -m spacy download ja_core_news_lg
RUN python3 -m spacy download de_dep_news_trf
RUN python3 -m spacy download es_dep_news_trf
RUN python3 -m spacy download ru_core_news_lg
RUN python3 -m spacy download pl_core_news_lg
RUN python3 -m spacy download it_core_news_lg
RUN python3 -m spacy download ko_core_news_lg
RUN pip3 install --no-cache-dir spacy-pkuseg && pip3 cache purge

# install requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt && pip3 cache purge

# copy app files
COPY api.py start.sh ./

EXPOSE 8042
ENTRYPOINT ["./start.sh"]
