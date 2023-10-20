FROM python:3.11
 
WORKDIR /usr/src/app
COPY ./app .

COPY requirements.txt .
RUN pip install -r requirements.txt
 
ENTRYPOINT ["python"]
CMD ["main.py"]