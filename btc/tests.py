import pytest

from .poker import Poker


@pytest.fixture(scope='module', name='poker')
def poker_fixture():
    return Poker()


def test_highest_card(poker):
    output = poker.play('3D 5S 2H QD TD 6S KH 9H AD QH')
    assert output == 'Hand: 3D 5S 2H QD TD Deck: 6S KH 9H AD QH Best hand: highest-card'


def test_one_pair(poker):
    output = poker.play('6C 9C 8C 2D 7C 2H TC 4C 9S AH')
    assert output == 'Hand: 6C 9C 8C 2D 7C Deck: 2H TC 4C 9S AH Best hand: one-pair'


def test_two_pair(poker):
    output = poker.play('AH 2C 9S AD 3C QH KS JS JD KD')
    assert output == 'Hand: AH 2C 9S AD 3C Deck: QH KS JS JD KD Best hand: two-pairs'


def test_three_of_a_kind(poker):
    output = poker.play('KS AH 2H 3C 4H KC 2C TC 2D AS')
    assert output == 'Hand: KS AH 2H 3C 4H Deck: KC 2C TC 2D AS Best hand: three-of-a-kind'


def test_straight(poker):
    output = poker.play('AC 2D 9C 3S KD 5S 4D KS AS 4C')
    assert output == 'Hand: AC 2D 9C 3S KD Deck: 5S 4D KS AS 4C Best hand: straight'


def test_flush(poker):
    output = poker.play('2H AD 5H AC 7H AH 6H 9H 4H 3C')
    assert output == 'Hand: 2H AD 5H AC 7H Deck: AH 6H 9H 4H 3C Best hand: flush'


def test_full_house(poker):
    output = poker.play('2H 2S 3H 3S 3C 2D 9C 3D 6C TH')
    assert output == 'Hand: 2H 2S 3H 3S 3C Deck: 2D 9C 3D 6C TH Best hand: full-house'


def test_four_of_a_kind(poker):
    output = poker.play('2H 2S 3H 3S 3C 2D 3D 6C 9C TH')
    assert output == 'Hand: 2H 2S 3H 3S 3C Deck: 2D 3D 6C 9C TH Best hand: four-of-a-kind'


def test_straight_flush(poker):
    output = poker.play(['TH', 'JH', 'QC', 'QD', 'QS', 'QH', 'KH', 'AH', '2S', '6S'])
    assert output == 'Hand: TH JH QC QD QS Deck: QH KH AH 2S 6S Best hand: straight-flush'

