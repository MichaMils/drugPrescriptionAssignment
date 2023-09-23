FROM python:3.9-alpine

RUN apk add --no-cache bash

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/app.py"]
