FROM python:latest
ENV PYTHONBUFFERED 1
RUN mkdir "/api/"
WORKDIR "/api/"
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
