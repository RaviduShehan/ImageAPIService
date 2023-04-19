FROM python:buster
WORKDIR /ImageApp
COPY requirements.txt .
COPY src/serviceAccountKey.json .
RUN pip install -r requirements.txt

COPY src src
# Set environment variables for Firestore connection
ENV GOOGLE_APPLICATION_CREDENTIALS="./serviceAccountKey.json"
RUN pip install google-cloud-firestore
RUN pip install firebase-admin

EXPOSE 5004
ENTRYPOINT ["python", "./src/ImageService.py"]