This is an RFC document that explains the commands this app has to offer, what input they expect and what will the output be:
QUIT- closes the server if the password is correct. input- QUIT: {password}, output- server shut down
TIME- returns the current time. no need of input
ADM- returns the quit password if the admin password is correct. input- ADM: {admin password}, output- quit password
CONN- returns how many people are online. no need of input
BR- sends brodcast message to the people online. input- BR {message}
SEND TO- sends a message to a spesific person. input- SEND TO {name}:{message}, output- message send to name
KICK- kicking someone out of the chat room. input- KICK {name}, output- name being kicked
CALC- calculating an equation and returning the result. input- CALC: {equation}, output- reault for the equation
COM- returns a compliment. no need of input
QOTD- returns qoute of the day. no need of input
JOKE- returns a joke. no need of input
EXIT- disconnecting from the chat room
