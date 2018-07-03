from trello import TrelloClient
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import random

app = Flask(__name__)

client = TrelloClient(
    api_key='key-here',
    api_secret='key-here'
)

all_boards = client.list_boards()
my_board = all_boards[18] # specific to the board you want

# every single list you've ever made
my_lists = my_board.list_lists()

def get_todo_item():
	to_do = []
	for card in my_lists:
	    cards = card.list_cards()
	    if card.closed == False:
	        for i in cards:
	            to_do.append(i.name)
	return to_do[random.randint(0, len(to_do)-1)]

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():

	body = request.values.get('body', None)

	resp = MessagingResponse()
	
	resp.message("Why don't you try doing: " + get_todo_item())

	return str(resp)


if __name__ == "__main__":
	app.run(debug=True)
