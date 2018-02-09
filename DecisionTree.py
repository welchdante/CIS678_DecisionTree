from csv import reader
from math import log

class DecisionTree:

	def __init__(self):
		self.total_positive = 0
		self.total_negative = 0
		self.total_entropy = 0

	def set_binary_metrics(self, dataset):
		for row in dataset:
			if int(row[-1]) == 1:
				self.total_positive += 1
			else:
				self.total_negative += 1

	def calculate_total_entropy(self):
		positive = self.total_positive
		negative = self.total_negative
		total = self.total_positive + self.total_negative
		self.total_entropy = (-positive / total) * log(positive / total, 2) - (negative / total) * log(negative / total, 2)
		#print(log(5, 2))

	def calculate_individual_entropy(self, dataset, column_num):
		collection = {}
		for row in dataset:
			collection[row[column_num]] = []

	def calculate_gain(self, column):
		print("calc gains")

def read_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

filename = 'discrete_baseball.csv'
dataset = read_csv(filename)

decision_tree = DecisionTree()
decision_tree.set_binary_metrics(dataset)
decision_tree.calculate_total_entropy()
decision_tree.calculate_individual_entropy(dataset, 0)