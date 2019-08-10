#Instructions
# In this challenge, you are tasked with creating a Python script for analyzing the financial records of your company. You will give a set of financial data called [budget_data.csv](PyBank/Resources/budget_data.csv). The dataset is composed of two columns: `Date` and `Profit/Losses`. (Thankfully, your company has rather lax standards for accounting so the records are simple.)

# Your task is to create a Python script that analyzes the records to calculate each of the following:

  ## The total number of months included in the dataset

  ## The net total amount of "Profit/Losses" over the entire period

  ## The average of the changes in "Profit/Losses" over the entire period

  ## The greatest increase in profits (date and amount) over the entire period

  ## The greatest decrease in losses (date and amount) over the entire period

# As an example, your analysis should look similar to the one below:

#  Financial Analysis
#  ----------------------------
#  Total Months: 86
#  Total: $38382578
#  Average  Change: $-2315.12
#  Greatest Increase in Profits: Feb-2012 ($1926159)
#  Greatest Decrease in Profits: Sep-2013 ($-2196167)

#* In addition, your final script should both print the analysis to the terminal and export a text file with the results.

import csv, os

#absolute path
#csvpath = 'D:/Workspace/Bootcamp/python-challenge/PyBank/Resources/budget_data.csv.csv'
#output = open('D:/Workspace/Bootcamp/python-challenge/PyBank/Resources/budget_data_output.txt', "w")

#relative path
csvpath = os.path.join('..', 'Resources', 'budget_data.csv')
outputpath = os.path.join('..', 'Resources', 'budget_data_output.txt')

#Initialize variables for loop
total_months = 0 #There's 1 month for each row (column 0)
total_profit = 0 #Sum Profit/Losses column (column 1)
average_change = 0
month_to_month_change = 0
greatest_increase_in_profits = 0
greatest_decrease_in_profits = 0
greatest_increase_month = ""
greatest_decrease_month = ""

with open(csvpath, newline="") as csvfile:

    # CSV reader
    csvreader = csv.reader(csvfile)

    # Read the header row first (skip this step if there is no header)
    csv_header = next(csvreader)
    
    # Convert to a list
    csv_list = list(csvreader)

    total_months = len(csv_list) # Set the number of months which is equal to number of rows in the file
    total_profit = sum(int(i[1]) for i in csv_list) #sum each month's profit/loss
    
    #print(TotalMonths)
    #print(TotalProfit)
    
    #loop to add month to month change to the list
    for index, eachmonth in enumerate(csv_list): #use enumerate so each list is counted
        if index > 0 and index <= len(csv_list): #start month to month changes after first row
            month_to_month_change = int(csv_list[index][1]) - int(csv_list[index-1][1])
            csv_list[index].append(month_to_month_change)
    
    average_change = float(sum(int(i[2]) / (len(csv_list)-1) for index, i in enumerate(csv_list) if index > 0))

    greatest_increase_in_profits = max(int(i[2]) for index, i in enumerate(csv_list) if index > 0)
    greatest_decrease_in_profits = min(int(i[2]) for index, i in enumerate(csv_list) if index > 0) 
    
    #playing around to see if the month be found in a comprehension
    #greatest_increase_month = (i[0] for index, i in enumerate(csv_list) if index > 0 and i[2] == greatest_increase_in_profits)
    
    #print(f'greatest increase: {greatest_increase_in_profits}')
    #print(f'greatest decrease: {greatest_decrease_in_profits}')
    #print(f'greatest increase month: {greatest_increase_month}')
    
    for index, eachmonth2 in enumerate(csv_list):
        if index > 0 and eachmonth2[2] == greatest_increase_in_profits:
            greatest_increase_month = eachmonth2[0]
        elif index > 0 and eachmonth2[2] == greatest_decrease_in_profits:
            greatest_decrease_month = eachmonth2[0]
    
    #print(greatest_increase_month)
    #print(greatest_decrease_month)
            
#print to terminal
print('Financial Analysis')
print('----------------------------')
print(f'Total Months: {total_months}')
print(f'Total: ${total_profit}')
print(f'Average Change: ${ round(average_change,2) }')
print(f'Greatest Increase in Profits:: {greatest_increase_month} (${greatest_increase_in_profits})')
print(f'Greatest Decrease in Profits:: {greatest_decrease_month} (${greatest_decrease_in_profits})')

#output to file
output = open(outputpath, "w")
output.writelines('Financial Analysis\n')
output.writelines('----------------------------\n')
output.writelines(f'Total Months: {total_months}\n')
output.writelines(f'Total: ${total_profit}\n')
output.writelines(f'Average Change: ${round(average_change,2)}\n')
output.writelines(f'Greatest Increase in Profits:: {greatest_increase_month} (${greatest_increase_in_profits})\n')
output.writelines(f'Greatest Decrease in Profits:: {greatest_decrease_month} (${greatest_decrease_in_profits})\n')
output.close()




