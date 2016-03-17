#############
# equipment #
#############
# 5 Dice: 2 white and 3 red
dice = {1, 2, 3, 4, 5, 6}

# 56 risk cards
'''
The 56 RISK@ Cards: 42 marked with a territory and a picture of
Infantry, Cavalry, or Artillery l 2 “wild” cards marked with all three pictures,
but no territory
'''

'''
6 complete sets of armies, each containing 3
denominations of army pieces: Infantry (worth l), Cavalry (worth 5
Infantry), and Artillery (worth 10 Infantry, or 2 Cavalry). Start the game by
placing Infantry pieces; later in the game, you may trade in 5 Infantry for
1 Cavalry, or 2 Cavalry (or 1 Cavalry and 5 Infantry) for 1 Artillery.
'''
army_pieces_worth = {
	'Infantry': 1,
	'Cavalry': 5,
	'Artillery': 10
	}

territories_graph = {}
	
##########
# Stages #
##########

# Initial Army Placement
'''
Select a color and, depending on the number of players, count out the
“armies” you’ll need to start the game.

uses: starting_infantry_by_player_num
'''

'''
Roll one die. Whoever rolls the highest number takes one Infantry piece
from his or her pile and places it onto any territory on the board, thus
claiming that territory.

Starting to the left of the first player, everyone in turn places one army
onto any unoccupied territory. Continue until all 42 territories have
been claimed.

After all 42 territories are claimed, each player in turn places one
additional army onto any territory he or she already occupies. Continue
in this way until everyone has run out of armies. There is no limit to the
number of armies you may place onto a single territory.

uses: 1 dice, infantry, board
'''

'''
Shuffle the pack of RISK cards (remove the Mission cards) and place it,
face down, by the side of the board. This pack forms the draw pile.

uses: cards
'''

# Playing
'''
Whoever placed the first army takes the first turn
'''


'''
Trading In Cards for Armies. At the beginning of subsequent turns,
you may trade in matched sets of cards and take additional armies based on
the total number of sets anyone has traded in so far.
'''

'''
At any time during the game, you may trade in Infantry pieces for the
equivalent (see page 4) in Cavalry or Artillery if you need to, or wish to.
'''

'''
ATTACKING
After placing your armies at the beginning of your turn, decide if you wish
to attack at this time. The object of an attack is to capture a territory by
defeating all the opposing armies already on it. The battle is fought by a roll
of the dice. Study the board for a moment. Do you want to attack?

If you choose to attack, you must follow these rules:
You may only attack a territory that’s adjacent (touching) to one of your
own, or connected to it by a dashed line. 

Examples: Greenland may attack the Northwest Territory, Ontario, Quebec and Iceland.
North Africa may attack Egypt, Western Europe and Brazil. At the western and
eastern edges of the board, Alaska is considered adjacent to, and may attack, Kamchatka.

You must always have at least two armies in the territory you’re attacking from.

You may continue attacking one territory until you have eliminated all
armies on it, or you may shift your attack from one territory to another,
attacking each as often as you like and attacking as many territories as
you like during one turn.

To attack, first announce both the territory you’re attacking and the one
you’re attacking from. Then roll the dice against the opponent who
occupies the opposing territory.

Before rolling, both you and your opponent must announce the number
of dice you intend to roll, and you both must roll at the same time.

You, the attacker, will roll 1,2 or 3 red dice: You must have at least one
more army in your territory than the number of dice you roll. 

Hint: The more dice you roll, the greater your odds of winning. Yet the more
dice you roll, the more armies you may lose, or be required to move into a
captured territory.

The defender will roll either 1 or 2 white dice: To roll 2 dice, he or she
must have at least 2 armies on the territory under attack. Hint: The more
dice the defender rolls, the greater his or her odds of winning-but the
more armies he or she may lose.

To Decide a Battle. Compare the highest die each of you rolled. If yours
(the attacker’s) is higher, the defender loses one army from the territory
under attack. 

But if the defender’s die is higher or equal than yours, you lose one army
from the territory you attacked from; put it back in your clear plastic box.
If each of you rolled more than one die, now compare the two next-highest
dice and repeat the process.
'''

'''
Capturing territories.

As soon as you defeat the last opposing army on a territory, you capture
that territory and must occupy it immediately. To do so, move in at least
as many armies as the number of dice you rolled in your last battle.
Remember: In most cases, moving as many armies as you
can to the front is advantageous, because armies left behind can’t help
you when you are attacking. Also remember you must always leave at least
one army behind on the territory you attacked from. During the game,
every territory must always be occupied by at least one army.
'''

'''
Earning Cards. At the end of any turn in which you have captured at
least one territory, you will earn one (and only one) RISK card. You are
trying to collect sets of 3 cards in any of the following combinations:
- 3 cards of same design (Infantry, Cavalry, or Artillery)
- 1 each of 3 designs
- any 2 plus a “wild” card

If you have collected a set of 3 RISK cards, you may turn them in at the
beginning of your next turn, or you may wait. But if you have 5 or 6 cards at
the beginning of your turn, you must trade in at least one set, and may
trade in a second set if you have one.

If any of the 3 cards you trade in shows the picture of
a territory you occupy, you receive 2 extra armies. You must place both
those armies onto that particular territory.

Note: On a single turn, you may receive no more than 2 extra armies above
and beyond those you receive for the matched sets of cards you trade in.
'''

#########
# rules #
#########
MAX_PLAYERS = 6
NUM_OF_CARDS_TO_MATCH = 3
MIN_ARMIER_FOR_ATTACK = 2
MATCHED_LAND_ON_CARD_BONUS = 2
MAX_CARDS_AT_TURN_START = 4

# The player receives additional armies for occupying an entire continent, equal to the continent bonus shown on the game board
continent_bonus = {
	'Asian': 7,
	'North America': 5,
	'Europe': 5,
	'Africa': 3,
	'Australia': 2,
	'South America': 2
	}

'''
If 2 are playing, see instructions on page 11.
If 3 are playing, each player counts out 35 Infantry.
If 4 are playing, each player counts out 30 Infantry.
If 5 are playing, each player counts out 25 Infantry.
If 6 are playing, each player counts out 20 Infantry.
'''
starting_infantry_by_player_num = {
	2: ???,
	3: 35,
	4: 30,
	5: 25,
	6: 20
}

'''
The first set traded in - 4 armies
The second set traded in - 6 armies
The third set traded in - 8 armies
The fourth set traded in - 10 armies
The fifth set traded in - 12 armies
The sixth set traded in - 15 armies
'''
added_armies_by_traded_sets = {
	1: 4,
	2: 6,
	3: 8,
	4: 10,
	5: 12,
	6: 15,
	7: 20,
	8: 25,
	9: 30
}
