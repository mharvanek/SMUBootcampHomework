## PyPoll

#[Vote-Counting](Images/Vote_counting.png)

# In this challenge, you are tasked with helping a small, rural town modernize its vote-counting process. (Up until now, Uncle Cleetus had been trustfully tallying them one-by-one, but unfortunately, his concentration isn't what it used to be.)

# You will be give a set of poll data called [election_data.csv](PyPoll/Resources/election_data.csv). 
# The dataset is composed of three columns: `Voter ID`, `County`, and `Candidate`. 
# Your task is to create a Python script that analyzes the votes and calculates each of the following:

  # The total number of votes cast

  # A complete list of candidates who received votes

  # The percentage of votes each candidate won

  # The total number of votes each candidate won

  # The winner of the election based on popular vote.

# As an example, your analysis should look similar to the one below:

#  Election Results
#  -------------------------
#  Total Votes: 3521001
#  -------------------------
#  Khan: 63.000% (2218231)
#  Correy: 20.000% (704200)
#  Li: 14.000% (492940)
#  O'Tooley: 3.000% (105630)
#  -------------------------
#  Winner: Khan
#  -------------------------

# Module for reading CSV files
import csv, os

#absolute path
#csvpath = 'D:/Workspace/Bootcamp/python-challenge/PyPoll/Resources/election_data.csv'
#output = open('D:/Workspace/Bootcamp/python-challenge/PyPoll/Resources/election_data_output.txt', "w")

#relative path
csvpath = os.path.join('..', 'Resources', 'election_data.csv')
outputpath = os.path.join('..', 'Resources', 'election_data_output.txt')

header = "Election Results"
section_sep ="-------------------------"

#Variables
votes_for_candidate = 0 #for incrementing the vote count for each candidate
total_votes = 0 #total votes cast in the election
election_results = {} #dictionary for candidate / votes
winner = "" #candidate with the most votes

#process file and put it in a list
with open(csvpath, newline="") as csvfile:

    # CSV reader
    csvreader = csv.reader(csvfile)

    # Read the header row first (skip this step if there is no header)
    csv_header = next(csvreader)
    
    # Convert to a list
    votes_list = list(csvreader)

    #just playing around with sorting a list
    #csv_list.sort(key=lambda x: x[2])
    
    #print(csv_list[:10])

#total votes
total_votes = len(votes_list) #Set the total votes to the length of the list. One row for each vote

#loop through to find unique candidates and count votes
for candidates in votes_list:
    if candidates[2] not in election_results.keys(): #check if the candidate is already in the dictionary
        election_results[candidates[2]] = 1 #add to dictionary as key with first vote
    else:
        election_results[candidates[2]] = election_results[candidates[2]] + 1 #if the candidate is in the dict then add 1 to their vote total
        
#Who is the Winner?
winner = max(election_results, key=election_results.get)

#print(winner)
#print(election_results)

#print to terminal
print(header)
print(section_sep)
print(f'Total Votes: {total_votes}')
print(section_sep)
for key, value in election_results.items() :
        print(f'{key} : {"{:.2%}".format(value/total_votes)} ({value})' )
print(section_sep)
print(f'Winner: {winner} ')
print(section_sep)

#output to file
output = open(outputpath, "w")
output.writelines(f'{header}\n')
output.writelines(f'{section_sep}\n')
output.writelines(f'Total Votes: {total_votes}\n')
output.writelines(f'{section_sep}\n')
for key, value in election_results.items() :
    output.writelines(f'{key} : {"{:.2%}".format(value/total_votes)} ({value})\n' )
output.writelines(f'{section_sep}\n')
output.writelines(f'Winner: {winner}\n')
output.writelines(f'{section_sep}\n')
output.close()





