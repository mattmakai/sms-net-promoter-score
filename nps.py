#!/usr/bin/python

import argparse
import sys
from twilio.rest import TwilioRestClient


def get_unfiltered_messages(number):
    """
        Uses the Twilio Python helper library to iterate through all
        messages sent to a single phone number. Saves the results in
        a dict with the inbound phone number as a key and an array of all
        responses from that phone number as the value.

        For example the return value could look something like the following:
            {'+12025551234': ['10', 'great job!'],
             '+13035555678': ['5'],
             '+19735553456': ['abcdefgh']
            }
    """
    unfiltered_msgs = {}
    for m in client.messages.iter(to=number):
        if m.from_ in unfiltered_msgs.keys():
            unfiltered_msgs[m.from_].append(m.body)
        else:
            unfiltered_msgs[m.from_] = [m.body]
    return unfiltered_msgs


def extract_score(msg):
    """
        Attempts to extract a score of 0-10 from a message. If a vote
        cannot be extracted the function returns False and None.
        If a vote is successfully extracted the function returns True
        and the score as an int between 0-10.
    """
    try:
        score = int(msg[:2])
        if score > 10:
            score = 10
        return True, score
    except ValueError:
        return False, None


def filter_scores(msgs):
    """
        Converts a dict with phone numbers as keys and inbound messages
        as arrays for values into an array with just scores from 1-10.
        Any score ranked as 11 or higher will be converted to 10.
    """
    scores = []
    for number, msg_array in msgs.iteritems():
        for m in msg_array:
            success, score = extract_score(m)
            if success:
                scores.append(score)
                break
    return scores


def calculate_nps(scores):
    """
        Takes in a list of integers from 0-10 and returns the Net Promoter
        Score based on those scores.
    """
    responses_count = len(scores)
    promoters = scores.count(10) + scores.count(9)
    detractors = 0
    for i in range (0, 7):
        detractors += scores.count(i)
    proportion_promoters = promoters / (responses_count + 0.0)
    proportion_detractors = detractors / (responses_count + 0.0)
    return (proportion_promoters - proportion_detractors) * 100


def output_scores(scores):
    """
        Takes in a list of integers from 0-10 and outputs results about
        Net Promoter Score.
    """
    nps = calculate_nps(scores)
    print("%.0f responses received" % len(scores))
    print("Net Promoter Score: %0.1f" % nps)
    for i in range(0, 11):
        print("%.0f responses with the score of %.0f" % (scores.count(i), i))


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("usage: python nps.py [number with inbound SMS NPS scores]")
        print("example: python nps.py +12025551234")
    else:
        client = TwilioRestClient()
        number = sys.argv[1]
        unfiltered_msgs = get_unfiltered_messages(number)
        scores = filter_scores(unfiltered_msgs)
        output_scores(scores)

