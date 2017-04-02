# A file to open Hearthstone cards from the command line, then export them in a file format readable to the neural network
# Andrew Thomas 3/31/2017

import json

def main(filename : str, ratingsFilename: str) -> None:

    with open(filename) as fp:

        cards = json.load(fp)

    with open(ratingsFilename) as fp:

        scores = json.load(fp)['Cards']
    
    scores = list(map(lambda card: card['Name'].lower(), scores))

    cards.sort(key=lambda card: card['name'].lower())
    
    with open(filename + '_formatted.txt', 'w') as fp:
        for card in cards:
            if card['name'].lower() in scores:
                name = card.get('name', '')
                attack = card.get('attack', '')
                cardClass = card.get('cardClass', '')
                cost = card.get('cost', '')
                health = card.get('health', '')
                text = card.get('text', '').replace('\n', ' ').replace('<b>', '').replace('</b>', '').replace('[x]', '')
                cardType = card.get('type', '')
                rarity = card.get('rarity', '')
                tribe = card.get('race', '')

                fp.write('|0{0}|1{1}|2{2}|3{3}|4{4}|5{5}|6{6}|7{7}|8{8}\n'.format(attack, cardClass, cost, health, text, cardType, name, rarity, tribe))

if __name__=='__main__':
    import sys
    sys.exit(main(sys.argv[1], sys.argv[2]))