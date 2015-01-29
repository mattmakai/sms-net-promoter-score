import os
import twilio.twiml as twiml
from flask import Flask, Response

app = Flask(__name__)

# enter your desired SMS response message below
RESPONSE_MESSAGE = "Thank you for your feedback!"

@app.route('/')
def main():
    return "Web application up and running!"


@app.route('/message', methods=['POST'])
def twilio_response():
    response = twiml.Response()
    response.message(RESPONSE_MESSAGE)
    return Response(response.toxml(), mimetype="text/xml")


if __name__ == '__main__':
    # first attempt to get the PORT environment variable because it will be 
    # exposed if we're deploying on Heroku, otherwise default to port 5000
    port = int(os.environ.get("PORT", 5000))
    if port == 5000:
        app.debug = True
    app.run(host='0.0.0.0', port=port)
