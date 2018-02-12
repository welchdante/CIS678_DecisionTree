from csv import reader
from math import log
from pprint import pprint

class DecisionTree:

	def __init__(self):
		self.total_positive = 0
		self.total_negative = 0
		self.total_entropy = 0
		self.playoffs_by_stat = {}
		self.entropy_list = []
		self.gain_dict = {}

	def set_binary_metrics(self, dataset):
		for row in dataset:
			if int(row[-1]) == 1:
				self.total_positive += 1
			else:
				self.total_negative += 1

	def calc_total_entropy(self):
		positive = self.total_positive
		negative = self.total_negative
		total = self.total_positive + self.total_negative
		self.total_entropy = (-positive / total) * log(positive / total, 2) - (negative / total) * log(negative / total, 2)

	def calc_each_entropy_for_feature(self, dataset, column):
		self.playoffs_by_stat = self.create_dictionary(dataset, column)
		for key in self.playoffs_by_stat:
			positive = self.playoffs_by_stat[key][0]
			negative = self.playoffs_by_stat[key][1]
			entropy = self.entropy_function(positive, negative)
			self.playoffs_by_stat[key][2] = entropy
		
	def entropy_function(self, positive, negative):
		total = positive + negative
		if positive == 0:
			entropy = - (negative / total) * log(negative / total, 2)
		elif negative == 0:
			entropy = -(positive / total) * log(positive / total, 2)
		else:
			entropy = -(positive / total) * log(positive / total, 2) - (negative / total) * log(negative / total, 2)
		return entropy

	def create_dictionary(self, dataset, column):
		#first element is wins, second is losses
		collection = {}
		for row in dataset:
			collection[row[column]] = [0,0,0]
		for row in dataset:
			if row[-1] == '1':
				collection[row[column]][0] += 1
			else:
				collection[row[column]][1] += 1
		return collection

	def calc_gain(self):
		gain = self.total_entropy - self.get_sum_weighted_entropy()
		return gain

	def get_sum_weighted_entropy(self):
		sum_weighted_entropy = 0
		total = 0
		for key in self.playoffs_by_stat:
			total += self.playoffs_by_stat[key][0]
			total += self.playoffs_by_stat[key][1]

		for key in self.playoffs_by_stat:
			positive = self.playoffs_by_stat[key][0]
			negative = self.playoffs_by_stat[key][1]
			total_for_feature = positive + negative
			entropy = self.playoffs_by_stat[key][2]
			sum_weighted_entropy += total_for_feature / total * entropy
		return sum_weighted_entropy

	def get_max_key_value_pair(self):
		max_value = max(self.gain_dict.values())
		max_key = [i for i, j in self.gain_dict.items() if j == max_value]
		return (max_key, max_value)

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
decision_tree.calc_total_entropy()

for i in range(0,7):
	decision_tree.calc_each_entropy_for_feature(dataset, i)
	decision_tree.entropy_list.append(decision_tree.playoffs_by_stat)
	gain = decision_tree.calc_gain()
	decision_tree.gain_dict[i] = gain

max_gain = decision_tree.get_max_key_value_pair()
max_index = max_gain[0][0]
# pprint(decision_tree.entropy_list)
# pprint(decision_tree.gain_dict)
# print(max_index)
pprint(decision_tree.entropy_list[max_index])


for key in decision_tree.entropy_list[max_index]:
	if decision_tree.entropy_list[max_index][key][2] == 0:
		if decision_tree.entropy_list[max_index][key][1] == 0:
			print("We want to predict a 0 for this classification")
		else: 
			print("We want to predict a 1 for this classification")


