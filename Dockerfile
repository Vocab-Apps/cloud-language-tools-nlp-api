# running locally:
# docker run --name spacy_api -d -p 0.0.0.0:8042:8042/tcp lucwastiaux/spacy-api:20220918-3
# stopping:
# docker container stop spacy_api
# docker container rm spacy_api

FROM python:3.12-slim-bookworm

# update pip
RUN pip3 install --upgrade pip

# install spacy modules
RUN pip3 install --no-cache-dir spacy && pip3 cache purge
COPY install_spacy_modules.sh ./
RUN ./install_spacy_modules.sh
RUN pip3 install --no-cache-dir spacy-pkuseg && pip3 cache purge

# install flite / lex_lookup (required by epitran)
RUN apt-get update -y && apt-get install -y libasound2 python3-pip git gnupg build-essential wget
RUN wget https://github.com/festvox/flite/archive/refs/tags/v2.2.tar.gz && tar xvzf v2.2.tar.gz && cd flite-2.2 && ./configure && make && make install && cd testsuite && make lex_lookup && cp lex_lookup /usr/local/bin

# install requirements
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt && pip3 cache purge

# post install step (force download of some data files)
COPY post_install.py ./
RUN python3 post_install.py

# copy app files
COPY api.py start.sh ./

EXPOSE 8042
ENTRYPOINT ["./start.sh"]
