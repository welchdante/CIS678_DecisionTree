import csv
from csv import reader

def read_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

def write_csv(dataset):
	with open("temp.csv", "w") as f:
		writer = csv.writer(f)
		writer.writerows(dataset)

def runs_scored(dataset):
	for i in range(len(dataset)):
		for j in range(len(dataset[i])):
			print(dataset[i][j])
			if float(dataset[i][j]) <= 0.15:
				dataset[i][j] = "PO"
				print(dataset[i][j])
			elif float(dataset[i][j]) > 0.15 and float(dataset[i][j]) <= 0.4:
				dataset[i][j] = "BA"
				print(dataset[i][j])
			elif float(dataset[i][j]) > 0.4 and float(dataset[i][j]) <= 0.6:
				dataset[i][j] = "AV"
				print(dataset[i][j])
			elif float(dataset[i][j]) > 0.6 and float(dataset[i][j]) <= 0.85:
				dataset[i][j] = "AA"
				print(dataset[i][j])
			else:
				dataset[i][j] = "EX"
		

def runs_against(dataset):
	print("Runs Against")

def wins(dataset):
	print("Wins")

def on_base_percentage(dataset):
	print("On Base Percentage")

def slugging(dataset):
	print("Slugging")

def batting_average(dataset):
	print("Batting Average")

dataset = read_csv("baseball_numbers.csv")
runs_scored(dataset)
write_csv(dataset)