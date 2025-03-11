FROM python:3.13-alpine

RUN adduser -h /app -D padlister

USER padlister
WORKDIR /app

ENV PATH="$PATH:/app/.local/bin"

RUN pip --no-cache-dir install gunicorn

COPY requirements.txt ./
RUN pip --no-cache-dir install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "hedgedoc_pad_lister:create_app()", "-b", "[::0]"]
