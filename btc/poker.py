from collections import Counter, namedtuple
from itertools import combinations
from typing import List, Union, ValuesView, Tuple, Iterator

from .const import *

Card = namedtuple('Card', ['rank', 'suit'])


class HandChecker:

    @staticmethod
    def _get_counts_per_rank(cards: List[Card]) -> ValuesView:
        """Return the values of a Count object with the amount of card of a rank in a hand

        Example:
            _get_counts_per_rank(2H 2S 3H 4S 8C) -> [2, 1, 1, 1]

            The rank '2' is 2 times in the hand and the others only once
        """
        return Counter(card.rank for card in cards).values()

    def _one_pair(self, cards: List[Card]) -> bool:
        """
        Return True if there are 2 cards of the same rank
        Return False otherwise
        """
        counts_per_rank = self._get_counts_per_rank(cards)
        return 2 in counts_per_rank

    def _two_pairs(self, cards: List[Card]) -> bool:
        """
        Return True if there are 2 cards of the one same rank and 2 of another
        Return False otherwise
        """
        counts_per_rank = self._get_counts_per_rank(cards)
        return list(counts_per_rank).count(2) == 2

    def _three_of_a_kind(self, cards: List[Card]) -> bool:
        """
        Return True if there are 3 cards of the same rank
        Return False otherwise
        """
        counts_per_rank = self._get_counts_per_rank(cards)
        return 3 in counts_per_rank

    @staticmethod
    def _straight(cards: List[Card]) -> bool:
        """
        Return True if there are 5 consecutive ranks including A 2 3 4 5
        Return False otherwise
        """
        values = sorted([card.rank for card in cards])
        if values == list(range(min(values), max(values) + 1)):
            return True

        # Check if the straight hand is A 2 3 4 5
        return values == list(range(2, CARDS_IN_HAND + 1)) + [CARD_MAPPED_VALUES['A']]

    @staticmethod
    def _flush(cards: List[Card]) -> bool:
        """
        Return True if there are 5 cards of the same suit
        Return False otherwise
        """
        return all(card.suit == cards[0].suit for card in cards)

    def _full_house(self, cards: List[Card]) -> bool:
        """
        Return True if there are 3 cards of one rank and 2 cards of another
        Return False otherwise
        """
        counts_per_rank = self._get_counts_per_rank(cards)
        return 3 in counts_per_rank and 2 in counts_per_rank

    def _four_of_a_kind(self, cards: List[Card]) -> bool:
        """
        Return True if there are 4 cards of the same rank
        Return False otherwise
        """
        counts_per_rank = self._get_counts_per_rank(cards)
        return 4 in counts_per_rank

    def _straight_flush(self, cards: List[Card]) -> bool:
        """
        Return True if there are 5 consecutive cards (straight) of the same suit (flush)
        Return False otherwise
        """
        return self._flush(cards) and self._straight(cards)

    def get_best_hand(self, cards: List[Card]) -> int:
        """
        Return the first best hand found
        """
        if self._straight_flush(cards):
            best_hand = STRAIGHT_FLUSH
        elif self._four_of_a_kind(cards):
            best_hand = FOUR_OF_A_KIND
        elif self._full_house(cards):
            best_hand = FULL_HOUSE
        elif self._flush(cards):
            best_hand = FLUSH
        elif self._straight(cards):
            best_hand = STRAIGHT
        elif self._three_of_a_kind(cards):
            best_hand = THREE_OF_A_KIND
        elif self._two_pairs(cards):
            best_hand = TWO_PAIRS
        elif self._one_pair(cards):
            best_hand = ONE_PAIR
        else:
            best_hand = HIGHEST_CARD

        return best_hand


class Poker:

    def __init__(self):
        self.hand_checker = HandChecker()

    @staticmethod
    def _get_card_value(rank: str, suit: str) -> Tuple[int, str]:
        """Return the value of the rank and the suit"""
        try:
            return int(rank), suit
        except ValueError:
            return CARD_MAPPED_VALUES.get(rank), suit

    @staticmethod
    def _format_output(original_cards: list, best_hand: int) -> str:
        """Return the result of the play in the required format"""
        return 'Hand: {0} Deck: {1} Best hand: {2}'.format(
            ' '.join(original_cards[:CARDS_IN_HAND]),
            ' '.join(original_cards[CARDS_IN_DECK:]),
            HANDS[best_hand])

    @staticmethod
    def _get_possible_hands(player_hand: List[Card], deck_cards: List[Card]) -> \
            Iterator[List[Card]]:
        """
        Generate all the possible hand combinations taking one card by one from the deck
        and replacing them on the player's hand

        Example:
             player_hand -> AC 2D 9C 3S KD
             deck_cards  -> 5S 4D KS AS 4C

             It will replace all the cards one by one with the first card on the deck

             _get_possible_hands -> 5S 2D 9C 3S KD
             _get_possible_hands -> AC 5S 9C 3S KD
             _get_possible_hands -> AC 2D 5S 3S KD
             _get_possible_hands -> AC 2D 9C 5S KD
             _get_possible_hands -> AC 2D 9C 3S 5S

             The it will take the the first two cards on the deck and it will replace every
             possible combination on the player's hand

             Then the first 3 from the deck and so on

             _get_possible_hands -> 5S 4D 9C 3S KD
             _get_possible_hands -> 5S 2D 4D 3S KD
             _get_possible_hands -> 5S 2D 9C 4D KD
             _get_possible_hands -> 5S 2D 9C 3S 4D
             _get_possible_hands -> AC 5S 4D 3S KD
        """
        for number_dealt_cards in range(1, len(player_hand) + 1):
            for replacements in combinations(range(len(player_hand)), number_dealt_cards):
                possible_hand = player_hand[:]
                for index_card_deck, replacement_index in enumerate(replacements):
                    possible_hand[replacement_index] = deck_cards[index_card_deck]
                    yield possible_hand

    def play(self, data: Union[str, list]) -> str:
        """
        Set the cards for the player and the deck
        Get the best hand from the initial player's hand
        Get the next possible move withdrawing cards from the deck
        Get the best hand in that move
        Return the original data and the best hand to be printed
        """
        if isinstance(data, str):
            data = data.strip().split(CARDS_SEPARATOR)

        player_hand = [Card(*self._get_card_value(*card)) for card in data[:CARDS_IN_HAND]]
        deck_cards = [Card(*self._get_card_value(*card)) for card in data[CARDS_IN_DECK:]]
        best_hands = [self.hand_checker.get_best_hand(player_hand)]

        for possible_hand in self._get_possible_hands(player_hand, deck_cards):
            best_hands.append(self.hand_checker.get_best_hand(possible_hand))

            if STRAIGHT_FLUSH in best_hands:
                # There is no need to continue iterating over the possible hands because
                # this is the best possible hand
                break

        return self._format_output(data, max(best_hands))
