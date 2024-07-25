import random

def sum_hand(hand: list[tuple[str, str]]):
    total = 0
    aces = 0

    for card in hand: 
        if card[0] in ["Jack", "Queen", "King"]: 
            total += 10

        elif card[0] == "Ace":
            total += 11
            aces += 1
        else:
            total += int(card[0])

    while aces > 0 and total > 21: 
        total -= 10 
        aces -= 1 

    return total

def compare_hands(dealer_hand: list[tuple[str, str]], player_hand: list[tuple[str, str]]):
    dealer_total = sum_hand(dealer_hand)
    player_total = sum_hand(player_hand)
    if dealer_total > player_total: 
        return "loss"
    elif dealer_total < player_total: 
        return "win"
    else: 
        return "push"

class Dealer():
    def __init__(self):
        self.hand = []

    def deal_card(self, deck: list[tuple[str, str]]): 
        return deck.pop(random.randint(0, len(deck)-1))

    def get_hand(self, deck: list[tuple[str, str]]):
        total = 0
        aces = 0
        while total < 17 or total > 21:
            if total > 21: 
                if aces > 0:
                    # case where Ace changes from 11 -> 1, above 16
                    if total - 10 > 16: 
                        return self.hand, total - 10
                else: 
                    # no aces hand busts 
                    return self.hand, total
            # dealer deals if total < 21
            # if there exists an ace that changes from 11 -> 1, is less than 17, and total < 21
            card = self.deal_card(deck)
            self.hand.append(card)
            print(card)
            if card[0] in ["2","3", "4", "5", "6", "7", "8", "9", "10"]:
                total += int(card[0])
            elif card[0] in ["Jack", "Queen", "King"]:
                total += 10
            else:
                aces += 1
                # catches cases where there are multiple aces or ace is first card dealt
                if aces > 0: 
                    # Ace is 11, above 16, less 22
                    if total + 11 >= 17 and total + 11 <= 21: 
                        return self.hand, total + 11
                    
                    # Ace is 1, more than 17 
                    if total + 1 > 17:
                        return self.hand, total + 1
                    
            # Ace is 1, less 17
            total += 1
        return self.hand, total 

    def new_hand(self): 
        self.hand = []
        self.total = 0