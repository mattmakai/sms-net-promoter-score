from flask import Flask, request, Response
import twilio.twiml as twiml

app = Flask(__name__)

@app.route('/', methods=['POST'])
def twilio_response():
    response = twiml.Response()
    # enter your SMS response message below
    msg = "Thank you! Email me at makai@twilio.com with questions."
    response.message(msg)
    return Response(response.toxml(), mimetype="text/xml")

if __name__ == '__main__':
    app.run()
