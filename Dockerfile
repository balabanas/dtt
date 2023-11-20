FROM python:3.10-buster

RUN mkdir -p /home/app
RUN addgroup --system app && adduser --system app
RUN adduser app app
ENV APP=/home/app
ENV APP_SRC=/home/app/src
RUN mkdir $APP_SRC
RUN mkdir $APP/static
RUN mkdir $APP/media
RUN mkdir $APP/db
WORKDIR $APP_SRC

# install dependencies
COPY ./requirements_prod.txt .
RUN pip install -r requirements_prod.txt

# copy project
COPY . .

# copy entrypoint.prod.sh
COPY ./entrypoint.prod.sh .
RUN sed -i 's/\r$//g'  ./entrypoint.prod.sh
RUN chmod +x  ./entrypoint.prod.sh

# chown all the files to the app user
RUN chown -R app:app $APP

# change to the app user
USER app

# run entrypoint.prod.sh
ENTRYPOINT ["/home/app/src/entrypoint.prod.sh"]