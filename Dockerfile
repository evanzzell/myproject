FROM python:3.12.3-alpine


COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

ADD . /app
WORKDIR /app

CMD ["python", "app.py"]