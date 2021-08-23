FROM python:3.7-alpine


ENV PYTHONNUNBUFFERED 1 

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client jpeg-dev

# these libs are related to postgresql(psycopg2) and pillow
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

RUN pip install -r /requirements.txt

RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# media and static files dirs 
RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
# add permisiion to user to access these dirs 
RUN chown -R user:user /vol/
#other people can read and execute from the dir
RUN chmod -R 755 /vol/web
USER user