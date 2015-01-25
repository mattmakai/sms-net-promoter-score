#!/usr/bin/python

import argparse
import re
import time
from datetime import datetime
from twilio.rest import TwilioRestClient


def get_messages(number, event_date):
    """
        Uses the Twilio Python helper library to iterate through all
        messages sent to a single phone number. Saves the results in
        a dict with the inbound phone number as a key and an array of all
        responses from that phone number as the value.

        Keyword arguments:
            number -- which number to search for messages
            event_date -- string with date in YYYY-MM-DD format

    """
    msgs = {}
    for m in client.messages.iter(to=number, date_sent=event_date):
        if m.from_ in msgs.keys():
            msgs[m.from_].append(m.body)
        else:
            msgs[m.from_] = [m.body]
    return msgs


def filter_scores(msgs):
    """
        Converts a dict with phone numbers as keys and inbound messages
        as arrays for values into an array with just scores from 0-10,
        including any scores with decimal places.

        Keyword arguments:
            msgs -- dict with phone numbers as keys and a list of
                    inbound messages as the values
    """
    scores = []
    for msg_array in msgs.values():
        for m in msg_array:
            score = re.match("\d+(\.\d{1,2})?", m)
            if score:
                scores.append(round(float(score.group())))
                # break to prevent counting duplicate scores from same number
                break
    return scores


def calculate_nps(scores):
    """
        Takes in a list of floats and returns the Net Promoter Score based
        on those scores.

        Keyword arguments:
            scores -- list of floats representing scores
    """
    detractors, promoters = 0, 0
    for s in scores:
        if s <= 6:
            detractors += 1
        if s >= 9:
            promoters += 1
    return (float(promoters) / len(scores) - \
            float(detractors) / len(scores)) * 100


def output_scores(scores):
    """
        Takes in a list of integers from 0-10 and outputs results about
        Net Promoter Score.

        Keyword arguments:
            scores -- list of floats representing scores
    """
    nps = calculate_nps(scores)
    print("{} responses received".format(len(scores)))
    print("Net Promoter Score: {0:.1f}".format(nps))
    for i in range(0, 11):
        print("{0} responses with a score of {1}".format(scores.count(i), i))


if __name__ == '__main__':
    description = "Process a Twilio phone number and event date."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('phone_number', type=str,
                        help='Twilio phone number that people send ' + \
                             'scores to, for example, +12025551234')
    parser.add_argument('--date', dest='event_date', type=str,
                        default=datetime.today().strftime("%Y-%m-%d"),
                        help='Date of the event to filter messages on. ' + \
                             'YYYY-MM-DD format. (default: today)')
    args = parser.parse_args()
    try:
        client = TwilioRestClient()
    except:
        # input Twilio credentials if not set in environment variables
        account = "ACXXXXXXXXXXXXXXXXX"
        token = "YYYYYYYYYYYYYYYYYY"
        client = TwilioRestClient(account, token)
    msgs = get_messages(args.phone_number, args.event_date)
    scores = filter_scores(msgs)
    if len(scores) > 0:
        output_scores(scores)
    else:
        print("No scores found for an event on {}.".format(args.event_date))

