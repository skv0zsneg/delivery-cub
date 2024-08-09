FROM python

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update 
RUN apt-get install -y netcat-traditional
RUN pip install --upgrade pip

WORKDIR /src

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENTRYPOINT ["/src/scripts/entrypoint.dev.sh"]