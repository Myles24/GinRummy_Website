"""
2-Player card game Gin Rummy. Not the official rules, but essentially the way I've
played. This project certainly took a lot of effort, but I am glad to have made
something more unique and replayable. I want to add more features in the future that
are left out for now, such as the ability to play off of the other player's sets and
the ability to add to your existing sets, but it is definitely playable in its
current state.  As for the code, I've tried to use as many functions as necessary
to make it more understandable. Almost all functions can be unit tested, but most
of the routes cannot since they all rely on the deck being shuffled. 
"""    
from drafter import *
from bakery import assert_equal
from dataclasses import dataclass
import random

# The unshuffled deck below follows this format for reference 
"""
deck = [    ["AH","AD","AC","AS"],
            ["2H","2D","2C","2S"],
            ["3H","3D","3C","3S"],
            ["4H","4D","4C","4S"],
            ["5H","5D","5C","5S"],
            ["6H","6D","6C","6S"],
            ["7H","7D","7C","7S"],
            ["8H","8D","8C","8S"],
            ["9H","9D","9C","9S"],
            ["TH","TD","TC","TS"],
            ["JH","JD","JC","JS"],
            ["QH","QD","QC","QS"],
            ["KH","KD","KC","KS"]];
"""

# NOT GLOBAL VARIABLES; their values never change and are purely for reference purposes for the order of the deck
# Long lines since the URLs are long and to keep the deck in the right format

card_backing = "https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg"
deck = [  ['https://tinyurl.com/26navyx5',
          'https://tinyurl.com/25ok22e9',
          'https://tinyurl.com/234sluca',
          'https://tinyurl.com/2b8ccqbs'],
         ['https://tinyurl.com/2d2cvtto',
          'https://tinyurl.com/29vgmnrc',
          'https://tinyurl.com/23dejutx',
          'https://tinyurl.com/298ptkrm'],
         ['https://tinyurl.com/279kzacw',
          'https://tinyurl.com/272p6n67',
          'https://tinyurl.com/27epah9q',
          'https://tinyurl.com/22ye5jw3'],
         ['https://tinyurl.com/27vu6za6',
          'https://tinyurl.com/26ck8p4y',
          'https://tinyurl.com/27duxr4r',
          'https://tinyurl.com/23wo778r'],
         ['https://tinyurl.com/2a7gpjdz',
          'https://tinyurl.com/23vxkqvt',
          'https://tinyurl.com/2565og6e',
          'https://tinyurl.com/27c6edrt'],
         ['https://tinyurl.com/2yvs9gh6',
          'https://tinyurl.com/29lla537',
          'https://tinyurl.com/25gkzw98',
          'https://tinyurl.com/2xnsftzr'],
         ['https://tinyurl.com/24faqu8f',
          'https://tinyurl.com/2d2wdr8d',
          'https://tinyurl.com/22tt5r79',
          'https://tinyurl.com/28t2q5sa'],
         ['https://tinyurl.com/2aoqvmn4',
          'https://tinyurl.com/25lpb662',
          'https://tinyurl.com/25y69bzq',
          'https://tinyurl.com/28s7gfnb'],
         ['https://tinyurl.com/2bp8eyzv',
          'https://tinyurl.com/27quodmz',
          'https://tinyurl.com/2cn4x9ws',
          'https://tinyurl.com/25eymsrb'],
         ['https://tinyurl.com/28g7cljp',
          'https://tinyurl.com/28n2o8qh',
          'https://tinyurl.com/247k5jto',
          'https://tinyurl.com/2dq4bpaj'],
         ['https://tinyurl.com/23ef6na5',
          'https://tinyurl.com/24capvo2',
          'https://tinyurl.com/22uaam9p',
          'https://tinyurl.com/29a7l8ba'],
         ['https://tinyurl.com/24v68dyd',
          'https://tinyurl.com/258fpqsy',
          'https://tinyurl.com/28q2p7au',
          'https://tinyurl.com/249ots95'],
         ['https://tinyurl.com/2b53h2y5',
          'https://tinyurl.com/28zc3tw6',
          'https://tinyurl.com/223o6ukn',
          'https://tinyurl.com/27m74ys7']]


def shuffle_deck(deck: list[list[str]]) -> list[str]:
    """ Shuffles the deck of cards.
        Cannot make unit test since the deck will be randomized.
    Args:
        deck (list[list[str]]): The 2D list of cards
    Returns:
        list[str]: A single list of all cards shuffled
    """
    new_deck = []
    for row in deck:
        for card in row:
            new_deck.append(card)
    random.shuffle(new_deck)
    return new_deck

def display_sets(sets: list[list[str]]) -> Table:
    """ Converts a 2D list of cards (sets) to be displayed as a 1-row table
    Args:
        sets (list[list[str]]): The 2D list of sets of cards
    Returns:
        Table: The 1-row table to be displayed on screen
    """
    set_images = []
    for y, set in enumerate(sets):
        set_images.append([])
        for url in set:
            set_images[y].append(Image(url, 82, 140))
    return Table(set_images)
    
def format_cards(urls: list[str]) -> list[list[str]]:
    """ Gets a list of cards ready to be displayed with their respective buttons
        by converting a list of cards into a 2D list with the first row being
        the Images of the card's urls.
    Args:
        urls (list[str]): The list of cards as urls of their PNGs
    Returns:
        list[list[str]]: The 2D list of Images be returned
    """
    cards = [[],[]]
    for url in urls:
        cards[0].append(Image(url, 82, 140))
    return cards
def display_cards(urls: list[str]) -> Table:
    """ Displays all cards in a list in Drafter
    Args:
        urls (list[str]): The list of URLs of the images of the cards
    Returns:
        Table: A 1-row Table of cards to be displayed in drafter
    """
    cards = format_cards(urls)
    return Table(cards)

@dataclass
class Player:
    """ Dataclass to store information about a player """
    name : str
    hand : list[str]
    sets : list[list[str]]
    points : int
  

@dataclass
class State:
    """ The State which stores data while the game is in play """
    deck: list[str]            # The randomized deck
    players : list[Player]     # List of two players. Index 0 is Player 1 and index 1 is Player 2
    current_player : bool      # True and False will represent indexes 1 and 0 of the Player list
    discard_pile : list[str] 
    current_phase : str        # Either 'Pick' Phase and 'Discard' Phase as explained in the instructions
    selected_cards : list[int] # The indexes of cards the user currently has selected to make a set

def get_hand(state : State) -> list[str]:
    """ Just a function to shorten the way to get the current player's hand
    Args:
        state (State): The state
    Returns:
        list[str] : The current player's hand of cards
    """
    return state.players[state.current_player].hand
    
def display_pick_buttons(urls : list[str], route : str) -> Table:
    """ Displays a list of cards and the same number of buttons to pick one of the cards up
    Args:
        urls (list[str]): The list of card PNGs as URLs
        route (str): The route that is attached to the button that signifies which
        pile the selected card is added to
    Returns:
        Table: A 2-row table to be displayed in Drafter where the first row are the
               cards and the second row are the buttons
    """
    cards_and_buttons = format_cards(urls)      
    for card_index in range(len(urls)):
        cards_and_buttons[1].append(Button("Pick"+str(card_index), route,
                                          [Argument("card_index", card_index)]))
    return Table(cards_and_buttons)

def display_select_buttons(state : State) -> Table:
    """ Displays a list of cards and the same number of buttons to select multiple cards
    Args:
        state: The State
    Returns:
        Table: A 2-row table to be displayed in Drafter where the first row are the cards
               from the player's hand and the second row are the buttons to select multiple
               cards from the hand.
    """
    cards_and_buttons = format_cards(get_hand(state))      
    for card_index in range(len(get_hand(state))):
        cards_and_buttons[1].append(Button("Select"+str(card_index), "/select_sets",
                            [Argument("card_index", card_index), Argument("selected", True)]))
    
    for i in range(len(get_hand(state))):
        if i in state.selected_cards:
            cards_and_buttons[1][i] = Button("Unselect"+str(i), "/select_sets",
                                [Argument("card_index", i), Argument("selected", False)])
    return Table(cards_and_buttons)

@route
def index(state: State) -> Page:
    """ The main page where the user can start the game or view instructions
    Args:
        state (State): The State
    Returns:
        Page: The main page of the site
    """
    return Page(state, [
        "Welcome to Gin Rummy!",
        "To view instructions, use the dropdown below.",
        Span(SelectBox("instructions", ["Game Setup", "Rules of Play", "Winning"]),
             Button("View Instructions", "/view_instructions",
                    [Argument("p1_name", "Player 1"), Argument("p2_name", "Player 2")])),
        "To get started, enter your names",
        Span("Player 1's Name: ", TextBox("p1_name", "Player 1")),
        Span("Player 2's Name: ", TextBox("p2_name", "Player 2")),
        Button("START GAME", "/deal_cards")
    ])
@route
def view_instructions(state : State, instructions : str, p1_name : str, p2_name :str) -> Page:
    """ The instructions page where the user can learn how the game is played.
    Args:
        state (State): The state
        instructions (str): Which category of instructions to show to the user
    Returns:
        Page: The page with the desired instruction category
    """
    if instructions == "Game Setup":
        return Page(state, [
            "Gin Rummy is a two-player game with alternating turns",
            "Each player is first dealt 7 random cards",
            "The remaining cards in the deck shall be available face down in a stack",
            "The top card from the deck is placed face up next to the deck; this is the start of the discard pile.",
            "At the end of each turn, a player MUST discard a card from their hand which gets placed face-up"
            " next to the previously discarded card.",
            Span(Button("Back", "/index"),
                Button("Next", "/view_instructions",
                       [Argument("instructions", "Rules of Play"),
                        Argument("p1_name", "Player 1"), Argument("p2_name", "Player 2")]))   
        ])
    elif instructions == "Rules of Play":
        return Page(state, [
            "The goal of Gin Rummy is to build 'sets' of cards, of which there are two types.",
            "A 'Rank Set' is three or more cards which share the same rank. For example:",
            display_cards([deck[0][0], deck[0][1], deck[0][2]]),
            "A 'Suit Set' is three or more cards which share the same suit,"+
            "but must be in direct increasing rank order. For example,",
            display_cards([deck[3][1], deck[4][1], deck[5][1]]),
            "Each turn, a player may either pick up from the deck or pick up from the discard pile",
            "If a player picks up from the deck, then they have two options: Make a set or Discard",
            "If they are unable to make a valid set or do not wish to do so, they must discard a card from their hand",
            "If a player wants to pick up a card from the discard pile instead, they will only be allowed to if "
            "they can form a valid set with their desired card. It is also worth noting that every other card to the "
            "right of the desired card in the discard pile will be picked up as well.",
            Span(Button("Back", "/view_instructions",
                [Argument("instructions", "Game Setup"),
                Argument("p1_name", "Player 1"), Argument("p2_name", "Player 2")]),
                Button("Next", "/view_instructions",
                       [Argument("instructions", "Winning"),
                        Argument("p1_name", "Player 1"), Argument("p2_name", "Player 2")]))
        ])
    elif instructions == "Winning":
        return Page(state, [
            "Play continues until either a player's hand is empty or the deck is depleted",
            "Scoring will commence in this format:",
            "Ranks A - 9 will be worth 5 points.",
            "Ranks 10 - K will be worth 10 points.",
            "The score is compiled for each player by calculating the "+
            "total number of points from each card in the player's sets "
            "minus the total number of points in the player's hand.",
            "The player with the most points at the end wins!",
            Span(Button("Back", "/view_instructions", [Argument("instructions", "Rules of Play"),
                                        Argument("p1_name", "Player 1"), Argument("p2_name", "Player 2")]),
                Button("Next", "/index")) 
        ])

@route
def play_turn(state: State) -> Page:
    """ The route that deals with the basic play of the game and what to display as it progresses.
        Cannot make consistent unit tests since the deck is randomized and the discard pile is based
        on user choice.
    Args:
        state (State): The state
    Returns:
        Page: The page that displays what's currently happening in the game
    """
    if len(state.deck) <= 0 or len(get_hand(state)) <= 0: # Triggers win conditions if either the deck
        return win_conditions(state)                      # or the current player's hand is empty
    
    # Pick Phase
    elif state.current_phase == "pick":
        return Page(state, [
            "Discard Pile (" + str(len(state.deck)) + " cards left in deck)",
            display_pick_buttons(state.discard_pile, "/pick_up_card"),
            state.players[state.current_player].name + "'s Hand",
            display_cards(get_hand(state)),
            "Sets",
            display_sets(state.players[state.current_player].sets),
        ])
    
    # Discard Phase
    elif state.current_phase == "discard":
        return Page(state, [
            "Discard Pile (" + str(len(state.deck)) + " cards left in deck)",
            display_cards(state.discard_pile),
            state.players[state.current_player].name + "'s Hand",
            display_cards(get_hand(state)),
            Button("Make set", "/make_set"),
            Button("Discard", "/pick_discard_card"),
            "Sets",
            display_sets(state.players[state.current_player].sets) 
    ])
    

@route
def make_set(state : State) -> Page:
    """ The route that handles what to display when the user wants to make a set
        Cannot make unit test since the player's starting hand is random.
    Args:
        state (State): The state
    Returns:
        Page: Displays cards that can be picked up
    """
    return Page(state, [
            "Discard Pile (" + str(len(state.deck)) + " cards left in deck)",
            display_cards(state.discard_pile),
            state.players[state.current_player].name + "'s Hand",
            display_select_buttons(state),
            Button("Confirm Selection", "/confirm_sets"),
            "Sets",
            display_sets(state.players[state.current_player].sets) 
    ])

@route
def pick_discard_card(state: State) -> Page:
    """ The route that handles when the user is ready to pick a card from their hand to discard
        Cannot make unit test since 
    Args:
        state (State): The state
    Returns:
        Page: The page of 'pick' buttons so the user can pick a card to discard
    """
    return Page(state, [
            "Discard Pile (" + str(len(state.deck)) + " cards left in deck)",
            display_cards(state.discard_pile),
            state.players[state.current_player].name + "'s Hand",
            display_pick_buttons(get_hand(state), "/discard"),
            "Sets",
            display_sets(state.players[state.current_player].sets)   
    ])
@route
def discard(state: State, card_index : int) -> Page:
    """ The route that handles discarding a card. The card is added to the discard pile
        and removed from the player's hand and the current player is changed.
        Cannot be unit tested since the deck and discard pile are randomized
    Args:
        state (State): The state
        card_index (int): The index of the card from the player's hand to be discarded
    Returns:
        Page: Returns to the play_turn page for the next player's turn
    """
    state.discard_pile.append(state.players[state.current_player].hand.pop(card_index))
    state.current_player = not state.current_player # Changes current player
    state.current_phase = "pick"
    return play_turn(state)


@route
def deal_cards(state: State, instructions : str, p1_name : str, p2_name : str) -> Page:
    """ Deals 7 random cards to each player and removes them from the deck
        Cannot be unit tested since the dealt cards are random
    Args:
        state (State): The State
        instructions (str): Which category of instructions to show the user (not used here)
        p1_name (str): Player 1's name
        p2_name (str): Player 2's name
    Returns:
        Page: Will call the play_turn route for the game to begin
    """
    state.players[0].name = p1_name
    state.players[1].name = p2_name
    state.deck = shuffle_deck(deck)
    for i in range(7):
        state.players[0].hand.append(state.deck.pop(0))
        state.players[1].hand.append(state.deck.pop(0))
    state.discard_pile.append(state.deck.pop(0))
    return play_turn(state)


#  ---------------------- VALID SET FUNCTIONS --------------------------

def get_card_coordinates(urls : list[str]) -> list[list[int]]:
    """ Converts a list of urls of cards to their respective coordinates in the unshuffled
        deck of cards so we can extract their suit and rank. Coordinates will be in the
        format of [Rank, Suit].
    Args:
        urls (list[str]): The urls of the images of the cards
    Returns:
        list[list[int]]: A list of coordinates of each card's placement in the 2d list 
    """
    card_coordinates = []
    for url in urls:
        for row in range(13):
            for col in range(4):
                if url == deck[row][col]:
                    card_coordinates.append([row, col])
    return card_coordinates

def check_standard_rank_set(selecting:bool, card_coordinates:list[list[int]], rank:int) -> bool:
    """ Checks whether a user has a valid rank set. A rank set is 3 or more cards that
        share the same rank. For example {Ace of Spades, Ace of Hearts, Ace of Diamonds}
        would be a valid rank set.
        
    Args:
        selecting (bool): Whether or not the user is selecting cards (True) to make a set or if
                          the user is trying to pick up a card from the discard pile to make a set (False)
        card_coordinates (list[list[int]]): The coordinates of the cards to be tested to extract their
                                            suit and rank
        rank (int): The specific rank to test other cards' ranks against to ensure a valid rank set.
    Returns:
        bool: Whether or not a list of cards is a valid rank set.
    """
    
    # If the user is selecting cards for a rank set, we need to make sure that they aren't selecting invalid cards
    # Namely, if the user selects a card with a rank that does not match, this should return False.
    set_length = 0
    for coordinate in card_coordinates:
        if coordinate[0] == rank:
            set_length += 1
        elif selecting:
            return False
    
    return set_length >= 3

def check_standard_suit_set(selecting : bool, card_coordinates : list[list[int]],
                            rank : int, suit : int) -> bool:
    """ Checks whether a user has a valid suit set. A suit set is 3 or more cards that share the
        same suit, but must be in direct order with two other cards in terms of their ranks.
        For example: {Two of Clubs, Three of Clubs, and Four of Clubs} is a valid suit set.
        Since these cards are in the form of URLs of their images, this function takes advantage
        of their position in the ordered 2D list (deck) to determine their suit and rank.
        
        Args: The same arguments as the next function (valid_set)
        Returns:
            bool: Whether or not a list of cards is a valid suit set
    """
    
    # If the user is selecting cards for a suit set, we need to make sure that they aren't selecting invalid cards
    # Namely, if the user selects a card with a suit that does not match, this should return False.       
    ranks = []
    set_length = 1
    for coordinate in card_coordinates: 
        if coordinate[1] == suit:       # If a card in the player's hand has the same suit,
            ranks.append(coordinate[0]) # Then append the card's rank to a list for comparison
        elif selecting:
            return False
    ranks.sort()                        # Then, sort this list in increasing order
    
    target_rank_index = 0
    for i in range(len(ranks)):        
        if ranks[i] == rank:            # Then find the index of the target rank in the list.
            target_rank_index = i       # The reason for this is to ensure that any set that
                                        # is found includes the card that is picked up
    
    # This searches indexes to the LEFT of the target to see if the ranks are increasing by 1 exactly
    left_search_index = target_rank_index - 1
    while left_search_index >= 0:
        if ranks[left_search_index] == ranks[left_search_index + 1] - 1:
            set_length += 1
            left_search_index -= 1
        else:
            break
    
    # This searches indexes to the RIGHT of the target to see if the ranks are increasing by 1 exactly
    right_search_index = target_rank_index + 1
    while right_search_index < len(ranks):
        if ranks[right_search_index] == ranks[right_search_index - 1] + 1:
            set_length += 1
            right_search_index += 1
        else:
            break
    
    # If the user is selecting cards to make a set, we need to make sure that every card that is selected
    # is included in the set. We can do this by checking the length of the list and the length of the found set.
    # This step is not necessary if we're checking a player's entire hand to determine if they are ABLE to make a set.
    if selecting:  
        return len(card_coordinates) == set_length and set_length >= 3
    return set_length >= 3
                
    
def valid_set(selecting : bool, urls : list[str], rank : int, suit : int) -> bool:
    """
    Args:
        selecting (bool): Whether or not the user is selecting cards (True) to make a set or if the user
                          is trying to pick up a card from the discard pile to make a set (False)
        card_coordinates (list[list[int]]): The coordinates of the cards to be tested to extract their
                                        suit and rank
        rank (int): The specific rank to test other cards' ranks against to ensure that they are increasing
                    by exactly 1
        suit (int): The specific suit to test other cards' suits against to ensure that they are the same
    Returns:
        bool: Whether or not either a rank set or a suit set can be made from given cards
    """
    card_coordinates = get_card_coordinates(urls)
    return check_standard_rank_set(selecting, card_coordinates, rank) or \
           check_standard_suit_set(selecting, card_coordinates, rank, suit)

# --------------------- END OF VALID SET FUNCTIONS -----------------------

@route
def pick_up_card(state: State, card_index : int) -> Page:
    """ This route handles what to do when a player wants to pick up a
        card from either the deck or discard pile.
        Cannot be unit tested since the deck and discard pile are randomized
    Args:
        state (State): The state
        card_index (int): The index of the card from the discard pile (the first index designates the deck)
    Returns:
        Page: Returns to the play_turn route to display the changes that were made from picking up a card
    """
    if card_index > 0: # If picking up from the discard pile...
        # check if this card would make a valid set with other cards in the player's hand
        selected_card_coordinates = get_card_coordinates([state.discard_pile[card_index]])
        rank = selected_card_coordinates[0][0]
        suit = selected_card_coordinates[0][1]
 
        # Making copies of the hand and discard pile
        temporary_discard_pile = state.discard_pile.copy() 
        temporary_hand = get_hand(state).copy()
        # This will append every card in the discard pile from the selected card to the end to the player's hand
        for j in range(card_index, len(temporary_discard_pile)):
            temporary_hand.append(temporary_discard_pile.pop(card_index))
        # If a valid set can be made with the selected card,
        # then the hand with the cards from the discard pile becomes the new hand.
        if valid_set(False, temporary_hand, rank, suit):
            state.players[state.current_player].hand = temporary_hand.copy()
            state.discard_pile = temporary_discard_pile.copy()
            state.current_phase = "discard"
            return make_set(state)
        
        return play_turn(state)
        
    # If picking up from the deck then append the first card from the deck to the player's hand.
    state.current_phase = "discard"
    state.players[state.current_player].hand.append(state.deck.pop(0))
    return play_turn(state)


@route
def select_sets(state : State, card_index: int, selected : bool) -> Page:
    """ Determines what to do when the user 'Selects' or 'Unselects' cards to make a pair.
        The selected card indexes from the player's hand are put into the selected_cards
        variable in the state and are removed if they are unselected.
        Cannot be unit tested since the deck and hands are random
    Args:
        state (State): The state
        card_index (int): The index of the card in the player's hand to be selected/unselected
        selected (bool): Whether a card in the hand is selected (True) or unselected (False)
    Returns:
        Page: Returns to the make_set route to display changes to the text on the buttons
    """
    if selected:
        state.selected_cards.append(card_index)
    else:
        for index in state.selected_cards:
            if index == card_index:
                state.selected_cards.remove(index)
    return make_set(state)

    

@route
def confirm_sets(state : State) -> Page:
    """ Route that checks if the set selected by the player is valid or not so play can continue
        Cannot be unit tested since the deck is randomized
    Args:
        state (State): The state
    Returns:
        Page: Either returns the make_set page if the set isn't valid or returns the play_turn page if it is
    """
    if not state.selected_cards:
        return play_turn(state)
    # Converts indexes of selected cards from the hand back into URLs
    card_urls = []
    for card_index in state.selected_cards:
        card_urls.append(get_hand(state)[card_index])
    # The rank and suit designations for this set are to be compared to the first selected card  
    rank = get_card_coordinates(card_urls)[0][0]      
    suit = get_card_coordinates(card_urls)[0][1]
    
    if valid_set(True, card_urls, rank, suit):
        state.players[state.current_player].sets.append(card_urls)
        for url in card_urls:
            state.players[state.current_player].hand.remove(url)
        state.selected_cards = []
        return play_turn(state)
    else:
        state.selected_cards = []
        return make_set(state)
    
@route
def win_conditions(state : State) -> Page:
    """ Route that gets called when the game is over to display scoring information
        Cannot be unit tested since the scoring is based on what the user is dealt
        from the randomized deck.
    Args:
        state (State): The state
    Returns:
        Page: The page with scoring information
    """
    # Converts 5 and 10 point cards into 1D lists of their URLs
    five_point_cards = []
    ten_point_cards = []
    for rank in deck[:9]:               # Ace to 9
        for card in rank:
            five_point_cards.append(card)
    for rank in deck[9:]:               # 10 to King
        for card in rank:
            ten_point_cards.append(card)
    
    # Checks to see if a card in the player's hand or pairs is worth 5 or 10 points
    for player in state.players:
        for card_set in player.sets:
            for card in card_set:
                if card in five_point_cards:
                    player.points += 5
                if card in ten_point_cards:
                    player.points += 10
                    
        for card in player.hand:
            if card in five_point_cards:
                player.points -= 5
            if card in ten_point_cards:
                player.points -= 10
    
    
    return Page(state, [
        "Game OVER",
        state.players[0].name + " has " + str(state.players[0].points) + " points.",
        "Hand",
        display_cards(state.players[0].hand),
        "Sets",
        display_sets(state.players[0].sets),
        state.players[1].name + " has " + str(state.players[1].points) + " points.",
        "Hand",
        display_cards(state.players[1].hand),
        "Sets",
        display_sets(state.players[1].sets),
        "Thanks for playing!"
    ])
        

# ------------------------------------------------------------------------------------------------------


# I've tried to make these assert_equal lines as short as possible
# but some of them are inherently long and cannot be broken up.

assert_equal(display_sets([["url1","url2","url3"],["url4","url5","url6"]]),
    Table(rows=[["<img src='/__images/url1'  style='width: 82; height: 140'>", \
        "<img src='/__images/url2'  style='width: 82; height: 140'>", \
        "<img src='/__images/url3'  style='width: 82; height: 140'>"],
        ["<img src='/__images/url4'  style='width: 82; height: 140'>", \
        "<img src='/__images/url5'  style='width: 82; height: 140'>", \
        "<img src='/__images/url6'  style='width: 82; height: 140'>"]]))

assert_equal(format_cards(["url1", "url2", "url3"]),
    [[Image(url='url1', width=82, height=140), Image(url='url2', width=82, height=140),
      Image(url='url3', width=82, height=140)], []])

assert_equal(display_cards(["url1", "url2", "url3"]),
    Table(rows=[["<img src='/__images/url1'  style='width: 82; height: 140'>", \
                 "<img src='/__images/url2'  style='width: 82; height: 140'>", \
                 "<img src='/__images/url3'  style='width: 82; height: 140'>"], []]))

assert_equal(get_hand(State([],[Player("",["card1", "card2"],[],0),
    Player("",["card3", "card4"],[],0)],False,[card_backing],"pick",[])),
        ["card1", "card2"])

assert_equal(get_hand(State([],[Player("",["card1", "card2"],[],0),
    Player("",["card3", "card4"],[],0)],True,[card_backing],"pick",[])),
        ["card3", "card4"])

assert_equal(display_pick_buttons(["url1", "url2"], "/pick_up_card"),
    Table(rows=[["<img src='/__images/url1'  style='width: 82; height: 140'>",
                 "<img src='/__images/url2'  style='width: 82; height: 140'>"],
                ["<input type='hidden' name='&quot;Pick0&quot;$@~@$card_index'"+
                 " value='0' /><button type='submit' name='--submit-button' "+
                 "value='&quot;Pick0&quot;' formaction='/pick_up_card?--"+
                 "submit-button=Pick0' >Pick0</button>",
                 "<input type='hidden' name='&quot;Pick1&quot;$@~@$card_index'"+
                 " value='1' /><button type='submit' name='--submit-button' va"+
                 "lue='&quot;Pick1&quot;' formaction='/pick_up_card?--"+
                 "submit-button=Pick1' >Pick1</button>"]]))


assert_equal(display_pick_buttons(["url1"], "/discard"),
    Table(rows=[["<img src='/__images/url1'  style='width: 82; height: 140'>"],
                ["<input type='hidden' name='&quot;Pick0&quot;$@~@$card_index"+
                 "' value='0' /><button type='submit' name='--submit-button' "+
                 "value='&quot;Pick0&quot;' formaction='/discard?--submit-"+
                 "button=Pick0' >Pick0</button>"]]))

assert_equal(display_select_buttons(State([],[Player("",["card1", "card2"],[],0),
        Player("",[],[],0)],False,[card_backing],"pick",[])),
    Table(rows=[["<img src='/__images/card1'  style='width: 82; height: 140'>",
                 "<img src='/__images/card2'  style='width: 82; height: 140'>"],
                ["<input type='hidden' name='&quot;Select0&quot;$@~@$card_"+
                 "index' value='0' />\n<input type='hidden' name='&quot;"+
                 "Select0&quot;$@~@$selected' value='true' /><button type="+
                 "'submit' name='--submit-button' value='&quot;Select0&quo"+
                 "t;' formaction='/select_sets?--submit-button=Select0' >Select0</button>",
                 "<input type='hidden' name='&quot;Select1&quot;$@~@$card_"+
                 "index' value='1' />\n<input type='hidden' name='&quot;Se"+
                 "lect1&quot;$@~@$selected' value='true' /><button type="+
                 "'submit' name='--submit-button' value='&quot;Select1&q"+
                 "uot;' formaction='/select_sets?--submit-button=Select1' >Select1</button>"]]))

assert_equal(
 index(State(deck=[], players=[Player(name='', hand=[], sets=[], points=0), \
    Player(name='', hand=[], sets=[], points=0)], current_player=False, \
    discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'], \
    current_phase='pick', selected_cards=[])),
 Page(state=State(deck=[],
                 players=[Player(name='', hand=[], sets=[], points=0),
                Player(name='', hand=[], sets=[], points=0)],
                 current_player=False,
                 discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'],
                 current_phase='pick',
                 selected_cards=[]),
 content=['Welcome to Gin Rummy!',
          'To view instructions, use the dropdown below.',
          Span(SelectBox(name='instructions',
                         options=['Game Setup', 'Rules of Play', 'Winning'], default_value=''),
               Button(text='View Instructions', url='/view_instructions',
                      arguments=[Argument(name='p1_name', value='Player 1'),
                        Argument(name='p2_name', value='Player 2')])),
          'To get started, enter your names',
          Span("Player 1's Name: ", TextBox(name='p1_name', kind='text', default_value='Player 1')),
          Span("Player 2's Name: ", TextBox(name='p2_name', kind='text', default_value='Player 2')),
          Button(text='START GAME', url='/deal_cards')]))

assert_equal(
 view_instructions(State(deck=[], players=[Player(name='', hand=[], sets=[], points=0), \
        Player(name='', hand=[], sets=[], points=0)], 
        current_player=False,
                discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'], 
                current_phase='pick', selected_cards=[]), 'Game Setup', 'Player 1', 'Player 2'),
 Page(state=State(deck=[],
                 players=[Player(name='', hand=[], sets=[], points=0),
                    Player(name='', hand=[], sets=[], points=0)],
                 current_player=False,
                 discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'],
                 current_phase='pick',
                 selected_cards=[]),
 content=['Gin Rummy is a two-player game with alternating turns',
          'Each player is first dealt 7 random cards',
          'The remaining cards in the deck shall be available face down in a stack',
          'The top card from the deck is placed face up next to the deck; this is the start of the discard pile.',
          'At the end of each turn, a player MUST discard a card from their hand which gets placed face-up next to '
          'the previously discarded card.',
          Span(Button(text='Back', url='/'), Button(text='Next', url='/view_instructions', 
                    arguments=[Argument(name='instructions', value='Rules of Play'),
                        Argument(name='p1_name', value='Player 1'),
                            Argument(name='p2_name', value='Player 2')]))]))
assert_equal(
 index(State(deck=[], players=[Player(name='', hand=[], sets=[], points=0), \
    Player(name='', hand=[], sets=[], points=0)], current_player=False, \
    discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'], \
    current_phase='pick', selected_cards=[])),
 Page(state=State(deck=[],
             players=[Player(name='', hand=[], sets=[], points=0),
                      Player(name='', hand=[], sets=[], points=0)],
             current_player=False,
             discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'],
             current_phase='pick',
             selected_cards=[]),
     content=['Welcome to Gin Rummy!',
              'To view instructions, use the dropdown below.',
              Span(SelectBox(name='instructions',
                options=['Game Setup', 'Rules of Play', 'Winning'], default_value=''),
                Button(text='View Instructions', url='/view_instructions',
                       arguments=[Argument(name='p1_name', value='Player 1'),
                            Argument(name='p2_name', value='Player 2')])),
              'To get started, enter your names',
              Span("Player 1's Name: ", TextBox(name='p1_name',
                            kind='text', default_value='Player 1')),
              Span("Player 2's Name: ", TextBox(name='p2_name',
                            kind='text', default_value='Player 2')),
              Button(text='START GAME', url='/deal_cards')]))
assert_equal(
 view_instructions(State(deck=[], players=[Player(name='', hand=[], sets=[], points=0), \
    Player(name='', hand=[], sets=[], points=0)], current_player=False, \
    discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'], \
    current_phase='pick', selected_cards=[]), 'Game Setup', 'Player 1', 'Player 2'),
 Page(state=State(deck=[],
         players=[Player(name='', hand=[], sets=[], points=0),
                  Player(name='', hand=[], sets=[], points=0)],
         current_player=False,
         discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'],
         current_phase='pick',
         selected_cards=[]),
 content=['Gin Rummy is a two-player game with alternating turns',
      'Each player is first dealt 7 random cards',
      'The remaining cards in the deck shall be available face down in a stack',
      'The top card from the deck is placed face up next to the deck; this is the start of the discard pile.',
      'At the end of each turn, a player MUST discard a card from their hand which gets placed face-up next to '
      'the previously discarded card.',
      Span(Button(text='Back', url='/'), Button(text='Next', url='/view_instructions',
        arguments=[Argument(name='instructions', value='Rules of Play'),
                   Argument(name='p1_name', value='Player 1'),
                   Argument(name='p2_name', value='Player 2')]))]))

assert_equal(
 view_instructions(State(deck=[],
    players=[Player(name='', hand=[], sets=[], points=0),
    Player(name='', hand=[], sets=[], points=0)], current_player=False,
    discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'],
    current_phase='pick', selected_cards=[]), 'Winning', 'Player 1', 'Player 2'),
 Page(state=State(deck=[],
     players=[Player(name='', hand=[], sets=[], points=0),
        Player(name='', hand=[], sets=[], points=0)],
     current_player=False,
     discard_pile=['https://m.media-amazon.com/images/I/614IlbYs76L._AC_UF1000,1000_QL80_.jpg'],
     current_phase='pick',
     selected_cards=[]),
     content=["Play continues until either a player's hand is empty or the deck is depleted",
      'Scoring will commence in this format:',
      'Ranks A - 9 will be worth 5 points.',
      'Ranks 10 - K will be worth 10 points.',
      'The score is compiled for each player by calculating the total number of points from each card in the '
      "player's sets minus the total number of points in the player's hand.",
      'The player with the most points at the end wins!',
      Span(Button(text='Back', url='/view_instructions',
        arguments=[Argument(name='instructions', value='Rules of Play'),
            Argument(name='p1_name', value='Player 1'),
            Argument(name='p2_name', value='Player 2')]),
            Button(text='Next', url='/'))]))

assert_equal(get_card_coordinates(
    ['https://tinyurl.com/2d2cvtto',
     'https://tinyurl.com/29vgmnrc']),
     [[1, 0],[1,1]])

assert_equal(check_standard_rank_set(False, [[1, 0],[1,1],[1, 3],[2, 5]], 1), True)
assert_equal(check_standard_rank_set(True, [[5, 2],[5,1],[5, 3],[2, 5]], 5), False)
assert_equal(check_standard_rank_set(False, [[2, 0],[2,1],[2, 3],[2, 5]], 2), True)

assert_equal(check_standard_suit_set(False, [[1, 0],[2,0],[3, 0],[6, 3]], 1, 0), True)
assert_equal(check_standard_suit_set(True, [[5, 2],[4,2],[6, 2]], 1, 0), False)
assert_equal(check_standard_suit_set(True, [[1, 0],[2,0],[3, 0],[2, 5]], 1, 0), False)
assert_equal(check_standard_suit_set(True, [[7,0],[8,0],[9,0]], 7, 0), True)

assert_equal(valid_set(True,
    ['https://tinyurl.com/2d2cvtto',
     'https://tinyurl.com/279kzacw',
     'https://tinyurl.com/27vu6za6'],
        1, 0), True)
assert_equal(valid_set(False,
    ['https://tinyurl.com/2bp8eyzv',
     'https://tinyurl.com/27quodmz',
     'https://tinyurl.com/2cn4x9ws',
     'https://tinyurl.com/2yvs9gh6'],
        8, 1), True)


#hide_debug_information()
set_website_framed(False)
set_website_title("Gin Rummy")
start_server(State([],[Player("",[],[],0), Player("",[],[],0)],False,[card_backing],"pick",[]))
