from statistics import median

# @purpose: Returns a list of intervals gotten according to the input specifications defined in the homework document
# @param input_file: The input file we will be reading from to get these intervals
def get_intervals_from_input(input_file):
    intervals = list()

    with open(input_file) as input:
        list_of_values = input.read().split(',')

        for x in range(0, len(list_of_values), 2):
            intervals.append([int(list_of_values[x]), int(list_of_values[x + 1])])

    return intervals

# @purpose: Outputs the given intervals that make up an MIS for the problem
# @param answer_intervals: The answer to this problem
# @param output_file_name: The output file name, in this case we will utilize 'output-#.csv' where # is the number of intervals in sol'n
def output_intervals(answer_intervals):

    output_file_name = "output-" + str(len(answer_intervals)) + ".csv"

    with open(output_file_name, 'w') as output:
        # To maintain proper .csv file format we go only to the second to last interval and then do the last outside it
        for x in range(len(answer_intervals) - 1):
            answer_segment = answer_intervals[x]

            to_print = str(answer_segment[0]) + "," + str(answer_segment[1]) + ","
            output.write(to_print)

        last_print = str(answer_intervals[-1][0]) + "," + str(answer_intervals[-1][1])
        output.write(last_print)



# @param list_of_intervals: a list of lists of length 2, such as the following : [[1,3],[5,6],[2,3]] 
# @param solution: A list variable for us to store the intermediate results of this recursive algorithm
def get_median_of_intervals(list_of_intervals, solution):
    # We begin by flattening the list
    flattened_list_of_intervals = [item for sublist in list_of_intervals for item in sublist]
 
    # We now get the median of all the endpoints which are now stored in our flattened list
    median_of_flattened_lists = median(flattened_list_of_intervals)

    S_minus = list()
    S_crossing = list()
    S_plus = list()
    x = None

    # Iterate over the intervals and find their relations to the median of all endpoints
    for interval in list_of_intervals:
        if interval[0] < median_of_flattened_lists and interval[1] < median_of_flattened_lists:
            S_minus.append(interval)
        elif(interval[0] > median_of_flattened_lists and interval[1] > median_of_flattened_lists):
            S_plus.append(interval)
        else:
            S_crossing.append(interval)

    if(len(S_minus) != 0):
        x = get_median_of_intervals(S_minus, solution)
        intervals_to_remove = list()

        for interval in S_crossing:
            if (x >= interval[0] and x <= interval[1]):
                intervals_to_remove.append(interval)

        S_crossing = [item for item in S_crossing if item not in intervals_to_remove]
    
    # Find the leftmost right endpoint
    if(len(S_crossing) != 0):
        leftmost_right_endpoint = 1000
        leftmost_right_interval = None

        for interval in S_crossing:
            if(interval[1] < leftmost_right_endpoint):
                leftmost_right_endpoint = interval[1]
                leftmost_right_interval = interval

        S_crossing = [leftmost_right_interval]  

    if(len(S_plus) == 0):
        if(len(S_crossing) == 1):
            # print(S_crossing[0])
            solution.append(S_crossing[0])
            x = S_crossing[0][1]
    else:
        S_crossing.extend(S_plus) # Adds all the elements of S_plus to S_crossing
        x = get_median_of_intervals(S_crossing, solution)

    return x


  
if __name__ == '__main__':

    intervals = get_intervals_from_input("input.csv")
    answer_list = []
    answer = get_median_of_intervals(intervals, answer_list)

    # print(answer_list)

    output_intervals(answer_list)
