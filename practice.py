import argparse
import random
from collections import Counter

class Card:
  def __init__(self, value, color, str_value):
    self.value = value
    self.color = color
    self.str_value = str_value
  def __str__(self):
    return self.str_value + self.color
  def __repr__(self):
    return self.str_value + self.color


class HandRank:
  ranks = ["StraightFlush", "FourOfAKind", "FullHouse", "Flush", "Straight", "ThreeOfAKind", "TwoPair", "Pair", "HighCard"]
  def __init__(self, max_value, type):
    self.max_value = max_value
    self.type = type
  def __eq__(self, other):
    return (self.max_value == other.max_value) and (self.type == other.type)
  def __lt__(self, other):
    ranks = ["StraightFlush", "FourOfAKind", "FullHouse", "Flush", "Straight", "ThreeOfAKind", "TwoPair", "Pair", "HighCard"]
    return (ranks.index(self.type) > ranks.index(other.type)) or self.max_value < other.max_value
  def __str__(self):
    return str(self.max_value) + " " + self.type
  def __repr__(self):
    return str(self.max_value) + " " + self.type


def shuffle():
  colors = ['H', 'D', 'S', 'C']
  str_values = [str(i) for i in range(2,11)] + ["J", "Q", "K", "A"]
  values = range(2, 15)
  zip_values = zip(values, str_values)

  deck = [Card(value[0], color, value[1]) for value in zip_values for color in colors]
  random.shuffle(deck)
  return deck


#Hacky way to deal because itertools.batched is only available in python 3.12
def deal(deck, num_players, num_cards=2):
  hands =[[deck[num_cards*j + i] for i in range(num_cards)] for j in range(num_players)]
  return deck[num_players*num_cards:], hands


# selects the value and type of the given 5 card hand
def best_hand(hand):
  colors = [card.color for card in hand]
  values = [card.value for card in hand]
  flush = (colors.count(colors[0]) == len(hand))
  straight = (set(values) == set(range(sorted(values)[0], sorted(values)[-1]+1))) and len(set(values))==5
  if flush and straight:
    return HandRank(max(values), "StraightFlush")

  counts = dict()
  for i in values:
    counts[i] = counts.get(i, 0) + 1
  for i in counts:
    if counts[i] == 4:
      return HandRank(i, "FourOfAKind")

  if set(counts.values()) == set([2, 3]):
    return HandRank(list(counts.keys())[list(counts.values()).index(3)], "FullHouse")

  if flush:
    return HandRank(max(values), "Flush")

  if straight:
    return HandRank(max(values), "Straight")

  for i in counts:
    if counts[i] == 3:
      return HandRank(i, "ThreeOfAKind")

  if sorted(counts.values()) == [1, 2, 2]:
    del(counts[list(counts.keys())[list(counts.values()).index(1)]])
    return HandRank(max(counts.keys()), "TwoPair")

  for i in counts:
    if counts[i] == 2:
      return HandRank(i, "Pair")

  return HandRank(max(values), "HighCard")


#compares two 5 card hands
def compare(hand1, hand2):
  return None


def calculate_rates(deck, hands):
  return None

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description = "Simulate Holdem hands at various stages and calculate hand equity for betting practice")
  parser.add_argument('-r', '--round', help='Round of betting to simulate. Choices: preflop', choices=['preflop'], default='preflop')
  parser.add_argument('-p','--num_players', help='Number of players at the table. [2..9]', type=int, default=2)
  args = parser.parse_args()

  print("Round:", args.round)
  print("Number of players:", args.num_players)

  deck = shuffle()
  dealt = deal(deck, args.num_players)
  print(dealt[0], dealt[1])
  #print(best_hand([Card(1, "H", "1"), Card(2, "C", "2"), Card(3, "H", "3"), Card(4, "H", "4"), Card(5, "H", "5")]))
  #print(best_hand([Card(10, "H", "10"), Card(2, "H", "2"), Card(3, "H", "3"), Card(4, "H", "4"), Card(5, "H", "5")]))
  #print(best_hand([Card(10, "H", "10"), Card(9, "H", "9"), Card(8, "H", "8"), Card(7, "H", "7"), Card(6, "H", "6")]))
  #print(HandRank(10,"FourOfAKind") < HandRank(9, "FourOfAKind"))
  #print(HandRank(10,"FourOfAKind") > HandRank(9, "FourOfAKind"))
  #print(HandRank(10,"FourOfAKind") == HandRank(10, "FourOfAKind"))
  #print(HandRank(10,"FourOfAKind") < HandRank(9, "StraightFlush"))

  print(best_hand([Card(10, "H", "10"), Card(9, "H", "9"), Card(8, "H", "8"), Card(7, "H", "7"), Card(6, "H", "6")]))
  print(best_hand([Card(10, "H", "10"), Card(10, "C", "10"), Card(10, "S", "10"), Card(10, "D", "10"), Card(6, "H", "6")]))
  print(best_hand([Card(10, "H", "10"), Card(10, "C", "10"), Card(10, "S", "10"), Card(11, "D", "J"), Card(11, "H", "J")]))
  print(best_hand([Card(10, "H", "10"), Card(9, "H", "9"), Card(3, "H", "8"), Card(7, "H", "7"), Card(6, "H", "6")]))
  print(best_hand([Card(10, "H", "10"), Card(9, "C", "9"), Card(8, "H", "8"), Card(7, "H", "7"), Card(6, "H", "6")]))
  print(best_hand([Card(10, "H", "10"), Card(10, "C", "10"), Card(10, "S", "10"), Card(11, "D", "J"), Card(12, "H", "Q")]))
  print(best_hand([Card(10, "H", "10"), Card(10, "C", "10"), Card(11, "S", "J"), Card(11, "D", "J"), Card(12, "H", "Q")]))
  print(best_hand([Card(10, "H", "10"), Card(10, "C", "10"), Card(9, "S", "9"), Card(11, "D", "J"), Card(12, "H", "Q")]))
  print(best_hand([Card(10, "H", "10"), Card(9, "H", "9"), Card(8, "H", "8"), Card(7, "H", "7"), Card(5, "C", "5")]))
