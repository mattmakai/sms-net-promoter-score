from flask import Flask, Response
import twilio.twiml as twiml

app = Flask(__name__)

@app.route('/', methods=['POST'])
def twilio_response():
    response = twiml.Response()
    # enter your SMS response message below
    msg = "Thank you for your feedback! Check out http://bit.ly/1rRQ7mS " + \
          "for more information on Python!"
    response.message(msg)
    return Response(response.toxml(), mimetype="text/xml")

if __name__ == '__main__':
    app.run()
