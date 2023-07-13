FROM python:3.10-alpine
WORKDIR /usr/src/app/
COPY . .
RUN pip install pipenv
RUN pipenv sync --system
