###############################################################################
#Computer Project #7
#   function to open file
#       use try and except
#   function to read file entered
#       for loop to read lines and analyze file
#   function to process data
#       two for loops to calclate data and return a tuple
#   function to display data
#   function to plot data
#   function for main
#       call for functions
#       ask to plot data
###############################################################################
'''
This code analyzes claims made to the TSA.
We look at data that includes the date received, Airport name, claim amount, 
    status and close amount.
We will display the approved, denied, and settled claims against the TSA
'''
import pylab   # needed for plotting

STATUS = ['Approved','Denied','Settled'] #three different status elements

def open_file(): #open file function
    '''
    Prompts user to insert a file
    Checks for an error
    '''
    excel_file = input("Please enter a file name: ") #prompt to input a file name
    while True:
        try:
            return_file = open(excel_file, 'r') #reads file
            return return_file #returns file
        except FileNotFoundError: #exception for when file is not found
            excel_file = input("File not found. Please enter a valid file name: ") #print error and prompt to input a file again
            
def read_file(fp): #read file function
    '''
    Take file pointer as an argument
    Creates Tuples for colums 1,4,9,10, and 11
    Only uses data from 2002-2009
    Returns list of tuples
    '''
    excel_list = [] #empty list
    fp.readline() #read a line to skip over headers
    for line in fp: 
        line = line.strip().split(',') #strips and splits line
        date_recieved = line[1] #set date received to index one 
        airport_name = line[4] #set airport name to index four
        airport_claim_amount = line[9].strip('$').replace(';','') #replace odd characters in amount with empty string
        status = line[10] #set status to index ten
        close_amount = line[11].strip('$').replace(';','') #replace odd characters in amount with empty string
        if date_recieved == '' or airport_name == '' or airport_claim_amount == '' or status == '' or close_amount == '':
            continue
        year = int(date_recieved[-2:]) #convert year to integer and use last two numbers
        if year < 2 or year > 9: #check for valid year
            continue
        airport_claim_amount = float(airport_claim_amount) #change to floating point
        close_amount = float(close_amount)#change to floating point
        data_tuple = (date_recieved, airport_name, airport_claim_amount, status, close_amount) #create tuple
        excel_list.append(data_tuple) #add tuple to list
    return excel_list #print list of tuples

def process(data): #process data function
    '''
    Uses read_data function
    Calculates total, average, max claim, and airport max claim
    Uses for loop to run through data
    Creates three lists that calculates apporved+settled+denied, settled+denied, and denied
    Returns a tuple of calculations
    '''
    absolute_close = 0 #initialize close amount to 0 
    average_amount = 0 #initialize average to 0
    max_claim_amount = 0 #initialize max claim amount to 0
    amount = 0 #initialize amount to o
    max_claim_airport = '' #initialize airport string to 0
    list1 = [0,0,0,0,0,0,0,0] #initialize list 1 to 0
    list2 = [0,0,0,0,0,0,0,0] #initialize list 2 to 0
    list3 = [0,0,0,0,0,0,0,0] #initialize list 3 to 0
    #all lists have 8 zeros for the 8 years we are looking at
    for line in data: #for loop to analyze lines in data
        airport_name = line[1] #set airport name to index one
        airport_claim_amount = line[2] #set claim amount to index twp
        status_str = line[3] #set status to index three
        close_amount = line[4] #set close amount to index 4
        if status_str in STATUS: #if status is approved, denied, or settled
            amount += 1 #add one to amount
            if (status_str == 'Approved' or status_str == 'Settled') and close_amount > 0:
                average_amount += close_amount #add close amount to average
                absolute_close += 1 #add one to total close amount
        if airport_claim_amount > max_claim_amount:
            max_claim_amount = airport_claim_amount #create new max claim amount
            max_claim_airport = airport_name #create new max airport name
        total_average = (average_amount / absolute_close) #calculate average
    for line in data: #for loop to analyze lines in data
        date_received = line[0] #set date received to index 0
        year_int = int(date_received[-2:]) #convert year to an integer
        year_position = year_int - 2 #subtract two from year
        status_str =line[3] #set status to index 3
        if status_str in STATUS: #if status is approved, denied, or settled
            list1[year_position] += 1 #add one to list one for specidfic year
            if status_str == 'Approved' or status_str == 'Settled': #status is only approved or settled
                list2[year_position] += 1 #add one to list 2 for specific year
            else: #if status is only denied
                list3[year_position] += 1 #add one to list three for specific year
    tuple_1= (list1, list2, list3, amount, total_average, max_claim_amount, max_claim_airport)
    #create tuple for list 1, list 2, list 3, total, avergae, max claim, max airport name) 
    return tuple_1 #return tuple

def display_data(tup): #display data function
    '''
    Prints Header
    Prints total cases
    Prints total, settled and denied cases from 2002-2009
    Prints average settlement and maximum claim amount and airport
    '''
    print("TSA Claims Data: 2002 - 2009")
    print("") #empty line
    total_cases = tup[0][0] + tup[0][1] + tup[0][2] + tup[0][3] + tup[0][4] + tup[0][5] + tup[0][6] +  tup[0][7] #add up total cases
    print("N =", '{:,d}'.format(total_cases),'  ') #print toal number of cases
    print("") #empty line
    print("{:<8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}{:>8s}".format(" ",'2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009'))
    print("{:<8s}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}".format('Total', tup[0][0], (tup[0][1]), tup[0][2], tup[0][3], tup[0][4], tup[0][5], tup[0][6], tup[0][7]))
    #print total number of cases per year
    print("{:<8s}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}".format('Settled', tup[1][0], tup[1][1], tup[1][2], tup[1][3], tup[1][4], tup[1][5], tup[1][6], tup[1][7])) 
    #print total number of settled cases per year
    print("{:<8s}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}{:>8,d}".format('Denied', tup[2][0], tup[2][1], tup[2][2], tup[2][3], tup[2][4], tup[2][5], tup[2][6], tup[2][7]))
    #print total number of denied cases per year
    print('') #empty line
    print('Average settlement:','${}'.format(format((tup[4]), ',.2f')),'   ') #print average settlement
    print('The maximum claim was','${}'.format(format((tup[5]), ',.2f')),'at',tup[6], 'Airport') #print maxmum claim amount and aiport
    
def plot_data(accepted_data, settled_data, denied_data): #plot data function
    '''Plot the three lists as bar graphs.'''

    X = pylab.arange(8)   # create 8 items to hold the data for graphing
    # assign each list's values to the 8 items to be graphed, include a color and a label
    pylab.bar(X, accepted_data, color = 'b', width = 0.25, label="total")
    pylab.bar(X + 0.25, settled_data, color = 'g', width = 0.25, label="settled")
    pylab.bar(X + 0.50, denied_data, color = 'r', width = 0.25,label="denied")
    # label the y axis
    pylab.ylabel('Number of cases')
    # label each bar of the x axis
    pylab.xticks(X + 0.25 / 2, ("2002","2003","2004","2005","2006","2007","2008","2009"))
    # create a legend
    pylab.legend(loc='best')
    # draw the plot
    pylab.show()
    # optionally save the plot to a file; file extension determines file type
    # pylab.savefig("plot.png")
    
def main(): #main function
    '''
    Calls for each function to run test on inputed file
    Gives user option to plot data
    '''
    fp = open_file() #call for open file function
    data = read_file(fp) #call for read file function
    tup = process(data) #call for process function
    display_data(tup) #call for display data function
    
    ask_plot_data = input('Plot data (yes/no): ') #asks user to plot data
    if ask_plot_data == 'yes': #if user wants to plot data
        accepted_data = tup[0]
        settled_data = tup[1]
        denied_data = tup[2]
    plot_data(accepted_data, settled_data, denied_data) #calll for plot data function using index 0, 1 and 2 on tuple created above
    
if __name__ == "__main__":
    main()


