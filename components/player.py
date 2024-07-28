import sqlite3
from components.dealer import Dealer
import os
def sql_command(sql, db, val = None) -> None:
    """
    Executes sql commands

    Parameters: 
    
    sql (str): an sql command that is represented by a string 

    db (str): the name of a database's path 

    val (tuple): a tuple that holds all values that are used in specific sql commands, such as INSERT

    """
    
    connection = sqlite3.connect(db)
    cursor = connection.cursor()

    if val: 
        cursor.execute(sql, val)
    else:
        cursor.execute(sql)
    connection.commit()
        
# holds the stats for a particular simulation 
class Player:
    """
    This is a class that represents a BlackJack player. 

    Attributes: 
    -----------

    """
    def __init__(self, name, balance):
        self.name = name 
        self.balance = balance 
        self.hands = [[]]
        self.wlp = 0
        self.prev_hands = []
        self.curr_bet = 0 

        directory = os.path.join('data')
        os.makedirs(directory, exist_ok=True)
        self.db_path = os.path.join(directory, self.name + ".db") # name of player is the name of the database

        sql_command(f'CREATE TABLE IF NOT EXISTS {self.name} (balance INTEGER, entry INTEGER, WLP TEXT)', self.db_path)
        sql_command(f'INSERT INTO {self.name} (balance, entry, WLP) VALUES (?, ?, ?)', self.db_path, (self.balance, self.curr_bet, self.wlp)) 
        sqlite3.connect(self.db_path).close()

    def add(self, amount: int) -> None:
        """ 
        This method adds to the balance of a player.

        Parameters: 

        amount (int): amount of simulation money being added to a player's balance

        """
        self.balance += amount
    
    def get_balance(self):
        """ This method returns the current balance of a player """
        return self.balance 
        
    def split(self, hand_num: int) -> None: 
        """ 
        This method represents a split in BlackJack. 

        Parameters: 

        hand_num (int): the number of the hand in a player's game that needs to be split. 
        """

        if len(self.hands) == 2 and self.hands[0][0] == self.hands[1][0]: 
            self.hands.append(self.hands[0].remove(self.hands[hand_num][1]))
        

    def stand():
        pass

        # problem referencing index that hasnt been instantiated 
    
    def hit(self, hand_num, deck: list[tuple[str, str]], dealer: Dealer) -> None:
        if hand_num > 1 and len(self.hands) != hand_num:
            self.hands.append([]) 
        if hand_num >= 1: 
            self.hands[hand_num - 1].append(dealer.deal_card(deck))
        else:
            print("invalid index")

    def get_hand(self) -> list[tuple[str, str]]:
        """ returns a list of tuples for a Player object's current hand of cards in the format list[tuple[str, str]] """
        return self.hands
    
    def new_hand(self) -> None:
        """ resets a Player object's current hand by setting self.hands to an empty list with an empty list """
        self.hands = [[]]
        sqlite3.connect(self.db_path).close()
    
    def previous_hands(self) -> list[str]:
        """
        This method returns a list of strings, which show if a previous had was a loss, push, or win, which is used in strategies 
        """
        return self.prev_hands
    
    def sum_player_hand(self, num_hand: int) -> int:
        """
        This is a private helper method that adds a hand's card value, which is represented by the first string in the list of tuples. 

        Parameters: 

        hand (list[tuple[str, str]]): list of tuples, which represent a card's value and suit 

        Returns: 

        int: the total value of a player's hand 
        """
        total = 0
        aces = 0
        for card in self.hands[num_hand - 1]:
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

    def compare_hands(self, dealer_total: int, player_total: int) -> None:
        """
        This is a private helper method that compares a player's hand and the total value of a dealer's hand to determine outcome of a BlackJack game. 

        Parameters: 

        dealer_total (int): the total value of a dealer's hand

        player_hand (list[tuple[str, str]]): list of tuples, which represent a card's value and suit

        Returns: 

        str: this method returns loss, win, or push based on if player_hand total is smaller, the same, or larger than the dealer_total
        """ 
        if dealer_total > player_total:
            return "loss"
        elif dealer_total < player_total: 
            return "win"
        else: 
            return "push"
    
    def bet(self, amount: int): 
        """
        This method sets a player's current bet. 

        Parameters: 

        amount (int): amount of the current bet. 
        """
        self.curr_bet = amount
        
    def check_bet(self, dealer_total: int) -> None:
        
        if len(self.hands) == 0 or dealer_total == 0:
            print("dealer hasn't dealt")

        outcome = ""
        for i in range(len(self.hands)):
            player_total = self.sum_player_hand(i)
            if self.balance < self.curr_bet:
                print("insufficient funds")
                quit()
            if self.compare_hands(dealer_total, player_total) == "win": 
                self.balance += self.curr_bet*1.5 
                outcome = "win"
                self.curr_bet = 0
            elif self.compare_hands(dealer_total, player_total) == "loss":
                self.balance -= self.curr_bet
                outcome = "loss"
                self.curr_bet = 0
            else:
                outcome = "push"
                self.curr_bet = 0

            self.prev_hands.append(outcome)
            sql_command(f'INSERT INTO {self.name} (balance, entry, WLP) VALUES (?, ?, ?)', self.db_path, (self.balance, self.curr_bet, outcome))
