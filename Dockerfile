FROM python:3.7-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt
COPY . /app
CMD [ "python", "-m" , "flask", "run", "--host=0.0.0.0"]