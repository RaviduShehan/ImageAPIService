FROM python:buster
WORKDIR /ImageApp
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src src
EXPOSE 5004
ENTRYPOINT ["python", "./src/ImageService.py"]