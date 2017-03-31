# A file to open Hearthstone cards from the command line, then export them in a file format readable to the neural network
# Andrew Thomas 3/31/2017

import json

def main(filename : str) -> None:

    with open(filename) as fp:

        cards = json.load(fp)

    cards.sort(key=lambda card: card["name"].lower())
    
    with open(filename + '_formatted.txt', 'w') as fp:
        for card in cards:
            attack = card.get('attack', '')
            cardClass = card.get('cardClass', '')
            cost = card.get('cost', '')
            health = card.get('health', '')
            text = card.get('text', '').replace('\n', ' ')
            cardType = card.get('type', '')
            name = card.get('name', '')
            rarity = card.get('rarity', '')

            fp.write('|0{0}|1{1}|2{2}|3{3}|4{4}|5{5}|6{6}|7{7}\n'.format(attack, cardClass, cost, health, text, cardType, name, rarity))

if __name__=='__main__':
    import sys
    sys.exit(main(sys.argv[1]))