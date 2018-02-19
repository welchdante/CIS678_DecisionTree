from csv import reader
from math import log
from pprint import pprint
from anytree import Node, RenderTree
from anytree.exporter import DotExporter

class DecisionTree:

	def __init__(self):
		self.total_positive = 0
		self.total_negative = 0
		self.total_entropy = 0
		self.playoffs_by_stat = {}
		self.entropy_list = []
		self.gain_dict = {}
		self.remaining_data = []
		self.data_labels = ['norm_rs', 'norm_ra', 'norm_w', 'norm_obp',	'norm_slg',	'norm_ba', 'id', 'playoffs']
		self.recursion_count = 0
		self.root_node = 0
		self.current_parent = 0
		self.children = []
		self.depth = 0

	def set_binary_metrics(self, dataset):
		for row in dataset:
			if int(row[-1]) == 1:
				self.total_positive += 1
			else:
				self.total_negative += 1

	def calc_total_entropy(self):
		positive = self.total_positive
		negative = self.total_negative
		total = positive + negative
		self.total_entropy = (-positive / total) * log(positive / total, 2) - (negative / total) * log(negative / total, 2)

	def calc_each_entropy_for_feature(self, data, column):
		self.playoffs_by_stat = self.create_dictionary(data, column)
		for key in self.playoffs_by_stat:
			positive = self.playoffs_by_stat[key][0]
			negative = self.playoffs_by_stat[key][1]
			entropy = self.entropy_function(positive, negative)
			self.playoffs_by_stat[key][2] = entropy
		
	def entropy_function(self, positive, negative):
		total = positive + negative
		if positive == 0:
			entropy = -1 * (negative / total) * log(negative / total, 2)
		elif negative == 0:
			entropy = -1 * (positive / total) * log(positive / total, 2)
		else:
			entropy = -1 * (positive / total) * log(positive / total, 2) - (negative / total) * log(negative / total, 2)
		return entropy

	def create_dictionary(self, data, column):
		#first element is wins, second is losses
		collection = {}
		for row in data:
			collection[row[column]] = [0,0,0]
		for row in data:
			if row[-1] == '1':
				collection[row[column]][0] += 1
			else:
				collection[row[column]][1] += 1
		return collection

	def calc_gain(self):
		sum_weighted_entropy = self.get_sum_weighted_entropy()
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
			entropy = self.playoffs_by_stat[key][2]
			total_for_feature = positive + negative
			weighted_entropy = total_for_feature / total * entropy
			sum_weighted_entropy += weighted_entropy
		return sum_weighted_entropy

	def get_max_key_value_pair(self):
		max_value = max(self.gain_dict.values())
		max_key = [i for i, j in self.gain_dict.items() if j == max_value]
		return (max_key, max_value)

	def build_tree(self, remaining_data):

		###################################
		# DO MATH
		###################################

		self.set_binary_metrics(remaining_data)
		self.calc_total_entropy()
		# print("Data to do the stuff to")
		# print(len(remaining_data))
		# pprint(remaining_data)

		for i in range(0,5):
			self.calc_each_entropy_for_feature(remaining_data, i)
			#pprint(self.playoffs_by_stat)
			pprint(self.playoffs_by_stat)
			self.entropy_list.append(self.playoffs_by_stat)
			gain = self.calc_gain()
			self.gain_dict[i] = gain
		
		max_gain = self.get_max_key_value_pair()
		max_index = max_gain[0][0]

		if self.root_node == 0:
			self.root_node = Node(self.data_labels[max_index])
			self.current_parent = self.root_node
		#else:
		#	self.current_parent = Node(self.data_labels[max_index])

		positive_labels_to_remove = []
		negative_labels_to_remove = []
		labels_to_keep = []
		for key in self.entropy_list[max_index]:
			if self.entropy_list[max_index][key][2] == 0:
				if self.entropy_list[max_index][key][0] == 0:
					negative_labels_to_remove = [i for i, j in self.entropy_list[max_index].items() if 0 == j[0]]
					negative_labels_to_remove.append(0)
					# print()
					# print("We want to predict a 0 for this classification")
					# print("This is also a leaf node with parent ", self.data_labels[max_index])
					# print(labels_to_remove)
					# print()
					#child = Node(labels_to_remove[0], parent = self.root_node)
					#print(labels_to_remove)

				elif self.entropy_list[max_index][key][1] == 0:
					positive_labels_to_remove = [i for i, j in self.entropy_list[max_index].items() if 0 == j[1]]	
					positive_labels_to_remove.append(1)
				# 	print() 
				# 	print("We want to predict a 1 for this classification")
				# 	print("This is also a leaf node with parent ", self.data_labels[max_index])
				# 	pprint(labels_to_remove)
				# 	print()
				# print("If statement")
				# pprint(labels_to_remove)
				# print()

			else:
				labels_to_keep = [i for i, j in self.entropy_list[max_index].items() if 0 != j[-1]]	
				# print("Else statement")
				# pprint(labels_to_keep)
				# print()
				#for i in range(len(labels_to_keep)):
				#		child = Node(labels_to_keep[i], parent = self.root_node)
			# pprint("Labels to remove")
			# pprint(labels_to_remove)
			# pprint("Labels to keep")
			# pprint(labels_to_keep)

		#########################################
		# this is where classification happens
		#########################################

		
		for i in range(len(positive_labels_to_remove) - 1):
			label = Node(positive_labels_to_remove[i], parent = self.root_node)
			child = Node(positive_labels_to_remove[-1], parent = label)
		for i in range(len(negative_labels_to_remove) - 1):
			label = Node(negative_labels_to_remove[i], parent = self.root_node)
			child = Node(negative_labels_to_remove[-1], parent = label)
		
		new_data = [[] for i in range(len(labels_to_keep))]

		for i in range(len(labels_to_keep)):
			for row in remaining_data:
				if row[max_index] == labels_to_keep[i]:				
					new_data[i].append(row)
		
		for i in range(len(new_data)):
			label = Node(labels_to_keep[i], parent = self.current_parent)
			child = Node(self.data_labels[i], parent = label)
			#grandchild = Node(len(new_data[i]), parent = child)
			self.the_other_build(new_data[i], child)
		
		#self.current_parent = child
		# if self.recursion_count <= 1:
		# 	self.recursion_count += 1
		# 	#print(len(new_data[i]))
		# 	self.build_tree(new_data[i])

		for pre, fill, node in RenderTree(self.root_node):
			print("%s%s" % (pre, node.name))

		DotExporter(self.root_node).to_picture("demo.png")

		pprint(self.playoffs_by_stat)

	def the_other_build(self, dataset, parent):
		self.set_binary_metrics(dataset)
		self.calc_total_entropy()

		for i in range(0,5):
			self.calc_each_entropy_for_feature(dataset, i)
			#pprint(self.playoffs_by_stat)
			self.entropy_list.append(self.playoffs_by_stat)
			gain = self.calc_gain()
			self.gain_dict[i] = gain
		
		max_gain = self.get_max_key_value_pair()
		max_index = max_gain[0][0]

		positive_labels_to_remove = []
		negative_labels_to_remove = []
		labels_to_keep = []

		for key in self.entropy_list[max_index]:
			if self.entropy_list[max_index][key][2] == 0:
				if self.entropy_list[max_index][key][0] == 0:
					negative_labels_to_remove = [i for i, j in self.entropy_list[max_index].items() if 0 == j[0]]
					negative_labels_to_remove.append(0)

				elif self.entropy_list[max_index][key][1] == 0:
					positive_labels_to_remove = [i for i, j in self.entropy_list[max_index].items() if 0 == j[1]]	
					positive_labels_to_remove.append(1)
			else:
				labels_to_keep = [i for i, j in self.entropy_list[max_index].items() if 0 != j[-1]]	
		
		for i in range(len(positive_labels_to_remove) - 1):
			label = Node(positive_labels_to_remove[i], parent = parent)
			child = Node(positive_labels_to_remove[-1], parent = label)
		for i in range(len(negative_labels_to_remove) - 1):
			label = Node(negative_labels_to_remove[i], parent = parent)
			child = Node(negative_labels_to_remove[-1], parent = label)							

		new_data = [[] for i in range(len(labels_to_keep))]

		for i in range(len(labels_to_keep)):
			for row in dataset:
				if row[max_index] == labels_to_keep[i]:				
					new_data[i].append(row)
		for i in range(len(new_data)):
			label = Node(labels_to_keep[i], parent = parent)
			child = Node(self.data_labels[i], parent = label)
			if self.recursion_count <= 0:
				self.recursion_count += 1
				pprint(self.playoffs_by_stat)
				self.the_other_build(new_data[i], child)
			#self.the_other_build(new_data[i], child)

def read_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

filename = 'discrete_baseball_no_teams.csv'
dataset = read_csv(filename)
decision_tree = DecisionTree()
decision_tree.build_tree(dataset)





