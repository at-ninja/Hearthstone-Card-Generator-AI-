import json

filename = "data/scored-cards.json"

def main():
	with open(filename) as fp:
	
		cards = json.load(fp)
		
	cards = cards["Cards"]
	cards.sort(key=lambda card: card["Name"])
	
	names = []
	
	#scored-cards.json_formatted.txt      lol
	i = 0
	with open(filename + "_formatted.txt", "w") as fp:
		for card in cards:
			name = card["Name"]
			scores = card["Scores"]
			if (name in names):
				continue
			else:
				names.append(name)
			
			numScores = 0
			avgScore = 0
			for score in scores:
				avgScore += score["Score"]
				numScores += 1
			score = int(avgScore / numScores)
			fp.write("{0}\t{1}\n".format(name,score))
			i += 1
			
main()