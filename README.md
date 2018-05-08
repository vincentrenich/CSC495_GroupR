# CSC495 Group R

Renich,Vincent

Project3 transcripts are under the proj3 directory, with the code in the CardGames directory under that.

Instructions to Play

1. Clone this repository on every machine you want to use
2. Navigate to CardGames on every terminal you want to use
3. On one machine/terminal, run 'python3 server.py' or 'python3 server.py -p <PORT>'
For this, <PORT> is the port number to use for connections.
If you don't specify this, the port will be 2222.
4. On a number of other machines/terminals (players), run 'python3 client.py <HOST> <PORT>'
For this, <HOST> is the hostname of the server machine, and <PORT> is the port number that the
server is listening on. Both of these are printed by the server when it starts.
5. On each client terminal, enter the player name for that client.

For Egyptian Rat Screw

6. Using the first terminal connected (the Game Master), enter '/start ers'
This will start the game.
7. Using the current player's terminal, type 'play' to play the next card or 'slap' to slap the deck
8. To exit, type 'exit' on each client terminal, and type CTRL+C on the server terminal until
   the program exits.

For The Last One

6. Using the first terminal connected (the Game Master), enter '/start lo'
This will start the game.
7. Using the current player's terminal, type 'play <rank> of <suit>' for a card in your hand to play that card (special cases for 8s and Jokers below) or 'hand' to view the cards in your hand or 'others' to see how many cards are in each of your competitors' hands. Press ENTER to send the messages.
8. To exit, type 'exit' on each client terminal, and type CTRL+C on the server terminal until
   the program exits.

The Last One Special Cases:

When playing 8's, you must follow the card with another suit to set the current suit to, in the same line.
When playing Jokers, you must declare the card to play them as afterwards (with extra suit as above for 8s) in the same line.

For Sequence

6. Using the first terminal connected (the Game Master), enter '/start sqnc'
This will start the game.
7. Using the second player's terminal (the player who joined after the game master), play your lowest card of any suit, where 2 is lowest and A is highest.
8. Using a player's terminal, type 'play <rank> of <suit>' for a card in your hand to play that card (next rank of the current suit) (player depends on who has the card, which is not stated; you have to check your hand to figure out if you have it) or 'hand' to view the cards in your hand or 'others' to see how many cards are in each of your competitors' hands. Press ENTER to send the messages.
9. To exit, type 'exit' on each client terminal, and type CTRL+C on the server terminal until
   the program exits.
   
Sequence Special Case:

When the A of a suit is played, the player who played it has to play the next card, which should be their lowest card of a different suit, preferrably one that hasn't already been played if possible.
