from datetime import datetime
import os
from flask import Flask, request, jsonify
import openai
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials

#setup firebase credentials
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')
# Initialize Firestore client with explicit project ID
project_id = "apiservices-384019"
db = firestore.Client(project=project_id)


@app.route('/')
def image():
    # Save service name, status, and timestamp to Firestore
    service_ref = db.collection('Services').document('ImageService_Status')
    print("ImageAPI Service Started.....")
    service_data = {
        'service_name': 'Image',
        'status': 'Starting',
        'timestamp': datetime.now()
    }
    service_ref.set(service_data)
    prompt = request.args.get('prompt')
    if not prompt:
        service_ref.update({'status': 'Empty Prompt'})
        return jsonify(error="Prompt parameter is missing"), 400
    service_ref.update({'status': 'Running'})
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="url"
        )
        return jsonify(response=response['data'][0]['url'])
    except Exception as e:
        service_ref.update({'status': 'Error'})
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)