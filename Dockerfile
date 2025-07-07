FROM python:3.10-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN apk add --no-cache bash curl build-base libffi-dev musl-dev postgresql-dev \
    && pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN curl -sS https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh -o /wait-for-it.sh && \
    chmod +x /wait-for-it.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

CMD ["/entrypoint.sh"]
