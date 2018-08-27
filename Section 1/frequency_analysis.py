import string
import collections
import matplotlib.pyplot as plot

class TextAnalyzer:

	def __init__(self):
		self.alphabet = list(
			letter for letter in string.ascii_uppercase + " "
		)

	def histogram(self, text):
		text = "".join(
			letter for letter in text if letter in self.alphabet
		)
		hist = dict(collections.Counter(text))
		# transform to probability
		return {x: float(hist[x]) / len(text) for x in hist}


class Plotter:

	def __init__(self, *plots):
		# add more for comparing more than three dicts
		colors = ("r", "g", "b")
		# append histogram to plot
		for idx, dictionaries in enumerate(plots):
			plot.subplot(len(plots), 1, idx + 1)
			for dictionary, color in zip(dictionaries, colors):
				sorted_by_probability = sorted(
					dictionary.items(), 
					key=lambda kv: kv[1]
				)
				plot.bar(
					[x[0] for x in sorted_by_probability],
					[x[1] for x in sorted_by_probability],
					color=color, alpha=0.6
				)
				plot.title("Probability of letters")
		plot.show()

if __name__ == '__main__':
	# reference data
	with open("confucius.txt", "r") as f:
		data = f.read().upper()
	with open("confucius2.txt", "r") as f:
		data2 = f.read().upper()

	t = TextAnalyzer()
	histogram = t.histogram(data)
	histogram2 = t.histogram(data2)

	Plotter([histogram, histogram2])
