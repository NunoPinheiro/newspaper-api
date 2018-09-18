FROM python:3.7.0-stretch

#Newspaper will be used only to get the top image
RUN git clone https://github.com/codelucas/newspaper.git && \
    cd newspaper && pip install -r requirements.txt

RUN git clone https://github.com/dragnet-org/dragnet.git
RUN cd dragnet && pip install -r requirements.txt && make

RUN pip install --no-cache-dir flask uwsgi

COPY . .
ENV NEWSPAPER_PORT 38765
EXPOSE $NEWSPAPER_PORT
CMD ["uwsgi", "--ini", "./src/wsgi.ini"]
