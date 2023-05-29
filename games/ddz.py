# -*- coding: utf-8 -*-


"""
斗地主

hx: 红心♥️
ht: 黑桃♠️
fp: 方片♦️
mh: 梅花♣️
xw: 小王🃏
dw: 大王🃏
"""


import collections
import random


Card = collections.namedtuple('Card', ['rank', 'suit'])


class FrenchDeck:
    ranks = [str(n) for n in range(3, 11)] + list('JQKA2')
    ranks_sort = [str(n) for n in range(3, 11)] + list('JQKA2-=')
    suits = 'hx ht fp mh'.split()

    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits
                       for rank in self.ranks]
        self._cards += [Card("=", "dw"), Card("-", "xw")]

    def __len__(self):
        return len(self._cards)

    def __getitem__(self, position):
        return self._cards[position]


suit_values = dict(hx=3, ht=2, fp=1, mh=0, dw=5, xw=4)


def spades_high(card):
    rank_value = FrenchDeck.ranks_sort.index(card.rank)
    return rank_value * len(suit_values) + suit_values[card.suit]


class Main:
    def __init__(self):
        f = list(FrenchDeck())
        random.shuffle(f)
        self.leader = None

        for i in ["user1", "user2", "user3"]:
            _tmp: list = f[:17]
            f = list(set(f) - set(_tmp))
            setattr(self, i, sorted(_tmp, key=spades_high))
        self.tmp = f

    def deal_cards(self):
        """发牌"""
        print(self.user1)
        print(self.user2)
        print(self.user3)
        print(self.tmp)

    def set_leader(self, username): ...

    def push(self): ...


if __name__ == '__main__':
    # Main().push()
    Main().deal_cards()
