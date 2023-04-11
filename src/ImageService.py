import openai
from flask import Flask, jsonify, request

app = Flask(__name__)
openai.api_key = os.environ.get('OPENAI_API_KEY')

@app.route('/image')
def image():
    prompt = request.args.get('prompt')
    if not prompt:
        return jsonify(error="Prompt parameter is missing"), 400

    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="512x512",
            response_format="url"
        )
        return jsonify(response=response['data'][0]['url'])
    except Exception as e:
        return jsonify(error=str(e)), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5004)