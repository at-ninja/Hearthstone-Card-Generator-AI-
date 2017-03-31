import json

filename = "scored-cards.json"

def main():
	with open(filename) as fp:
	
		cards = json.load(fp)
	
	#scored-cards.json_formatted.txt      lol
	with open(filename + "_formatted.txt", "w") as fp:
		for card in cards["Cards"]:
			name = card["Name"]
			scores = card["Scores"]
			
			numScores = 0
			avgScore = 0
			for score in scores:
				avgScore += score["Score"]
				numScores += 1
			score = int(avgScore / numScores)
			fp.write("{0}\t{1}\n".format(name,score))
	
main()