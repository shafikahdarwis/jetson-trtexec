#!/usr/bin/env bash

# Author : shafikah(nurshafikah.darwis@intel.com)
# -------------------------------------------------

import argparse
from itertools import groupby
import sys
import csv
import os
from datetime import datetime

os.system('clear')

ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required=True,
	help="path to input data")
args = vars(ap.parse_args())
		
def all_equal(iterable):
	g = groupby(iterable)
	return next(g, True) and not next(g, False)

def check_if_string_in_file(file_name, string_to_search):
	""" Check if any line in the file contains given string """
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			if string_to_search in line:
				return True
	return False

def search_string_in_file(file_name, string_to_search):
	"""Search for the given string in file and return lines number"""
	line_number = 0
	list_of_results = []
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			line_number += 1
			if string_to_search in line:
				list_of_results.append(line_number)
	return list_of_results

def search_multiple_strings_in_file(file_name, list_of_strings):
	"""Get line from the file along with line numbers, which contains any
	 string from the list"""
	line_number = 0
	list_of_results = []
	with open(file_name, 'r') as read_obj:
		for line in read_obj:
			line_number += 1
			for string_to_search in list_of_strings:
				if string_to_search in line:
					list_of_results.append(line_number)
	return list_of_results

def matched_lines(file_name, list_of_strings):
	"""Checks required "Header" Dimensions"""
	matched = search_multiple_strings_in_file(file_name, list_of_strings)
	
	if len(matched) % len(list_of_strings) == 0:
		return True
	else:
		return False
		
def find_line_of_interest(file_name, string_to_search, offset):
	""" """
	line_of_interest = []
	line_of_data = []
	interested = search_string_in_file(file_name, string_to_search)
	for i in interested:
		line_of_interest.append(i+offset)
		
	return line_of_interest
	
def list_of_interest(listing, N):
	""" """
	list_of_interest = []
	for i in listing:
		list_of_interest.append(CoList[i-1][N::])
	
	return list_of_interest
	
def clean_data(listing, stringName):
	""" """
	condition = all_equal(listing)
	if all_equal(listing):
		return listing[0]
	else:
		# exits the program 
		print("[ERROR] Required %s are abnormal..." % stringName)
		print("[ERROR] List of %s:" % stringName)
		print(listing)
		print("[ERROR] Please check the file!")
		sys.exit("[ERROR] Files may be corrupted...")


file = open(args["file"],"r")

Content = file.read() 
CoList = Content.split("\n")
listHeader = 	[
		"=== Model Options ===", 
		"=== Build Options ===", 
		"=== Inference Options ===", 
		"=== Reporting Options ==="
		]
boolHeader = matched_lines(args["file"], listHeader)
if boolHeader:
	pass
else:
	# exits the program 
	print("[ERROR] Required headers are missing or in-balance...")
	sys.exit("[ERROR] Files may be corrupted...")

line_of_format = find_line_of_interest(args["file"], 'Format:', 0)
line_of_prototxt = find_line_of_interest(args["file"], 'Prototxt:', 0)
line_of_precision = find_line_of_interest(args["file"], 'Precision:', 0)
line_of_iteration = find_line_of_interest(args["file"], 'Iterations:', 0)
line_of_batch = find_line_of_interest(args["file"], 'Batch:', 0)
line_of_throughput = find_line_of_interest(args["file"], 'throughput:', 0)
line_of_latency = find_line_of_interest(args["file"], 'Host Latency', 3)

list_of_format = list_of_interest(line_of_format, 34)
list_of_prototxt = list_of_interest(line_of_prototxt, 36)
list_of_precision = list_of_interest(line_of_precision, 37)
list_of_iteration = list_of_interest(line_of_iteration, 38)
list_of_batch = list_of_interest(line_of_batch, 26)
list_of_throughput = list_of_interest(line_of_throughput, 38)
list_of_latency = list_of_interest(line_of_latency, 32)

usedFormat = clean_data(list_of_format, "Format")
usedPrototxt = clean_data(list_of_prototxt, "Prototxt")
usedPrecision = clean_data(list_of_precision, "Precision")
usedIteration = clean_data(list_of_iteration, "Iterations")

# Summary
print("*" * 15 + " SUMMARY " + "*" * 15)
print("Format: %s" % usedFormat)
print("Prototxt: %s" % os.path.basename(usedPrototxt))
print("Precision: %s" % usedPrecision)
print("Iteration: %s" % usedIteration)
print("Throughput:")
print("Host Latency (Mean):")

for (i, j, k) in zip(list_of_batch, list_of_throughput, list_of_latency):
	print("%s: %s :%s" % (i, j, k))

print("*" * 40)

path, folder = os.path.split(args["file"])
base = os.path.basename(args["file"])
now = datetime.now()
dt_string = now.strftime("%B %d, %Y %H:%M:%S")
newFilename = "Summary" + base[3:-4] + '.csv'
dirPath = os.path.sep.join([path, newFilename])

with open(dirPath, mode='w') as extract_file:
	extract_writer = csv.writer(
					extract_file, 
					delimiter=',', 
					quotechar='"', 
					quoting=csv.QUOTE_MINIMAL
					)

	extract_writer.writerow(["Format", usedFormat])
	extract_writer.writerow(["Prototxt", usedPrototxt])
	extract_writer.writerow(["Precision", usedPrecision])
	extract_writer.writerow(["Iteration", usedIteration])
	extract_writer.writerow([" ", "Throughput", "Latency(Mean)"])
	
	for (i, j, k) in zip(list_of_batch, list_of_throughput, list_of_latency):
		extract_writer.writerow([i, j, k])
		
print("[INFO] Extracted files were save in: %s" % newFilename)
