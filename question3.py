""" 
program: question3_SSMIF.py
author: Eden Luvishis

In order to complete this logic question more efficiently, I have
defined 2 functions. The main one, sum_ssmif, expects a nested list 
as an input and iterates through it, sorting the list by even and odd
indices. In order to make the function more efficient, I have defined
a second function, get_sum, that is executed 3 times in the main. I 
realized that all 3 steps in the instructions follow a very similar
pattern. They have a start and end value and a multiplier that determines
the modified lists' values. In the final case, if 4 and 5 are present, 
this muliplier is just 0. Therefore, for lists with an even index, I call
the get_sum function with the values 9, 6, and 2, while for odd I call 
it with 7,4, and 3. 

Within the get_sum function, I parce through the list and find the total
sum of the normal list to begin with. Then, if the start value is present,
I create a new list that begins with the start value and contains the 
rest of the list. I then search for the end value in the remaining list. 
If it exists, the list is ammended to just contain values beginning from 
the start value and ending at the first occurence of the ending index. 
This list is then multiplied by the (multiplier - 1) because one case of 
each value was already accounted for in the total sum at the beginning 
of the function. In the case of 0 being the multiplier, the total sum 
is first found and then the "special" list is subtracted from the total 
sum by multiplying its values by -1. 

"""

def get_sum(l ,start, end, multiplier):
    """Returns sum of each inner-list depending on multiplier"""

    #one instance is already accounted for in totSum
    multBy = multiplier - 1 
    totSum = sum(l)

    #creates a new list in start and end are in the original list
    if start in l:
        startIndex = l.index(start)
        remainingList = l[startIndex:]

        if end in remainingList:
            endIndex = remainingList.index(end)

            #includes the end value
            totSum += sum(remainingList[:endIndex + 1 ]) * multBy

    return totSum

def sum_ssmif(l):
    """Returns the ssmif_sum of a nested list"""

    #new list to append values to
    myList = []

    for i in range(len(l)):
        #even indices
        if i % 2 == 0:
            evenResult = get_sum(l[i], 9, 6, 2)
            myList.append(evenResult)

        #odd indices 
        else:
            oddResult = get_sum(l[i], 7, 4, 3)
            myList.append(oddResult)

    #final list checks for 4 and 5
    finList = get_sum(myList, 4, 5, 0)

    return finList 

test = [[1,2,3,9,2,6,1], [1,3], [1,2,3], [7,1,4,2], [1,2,2]]

print(sum_ssmif(test))


