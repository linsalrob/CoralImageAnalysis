#munger.py
#Data munging helper for 2D ndarrays from numpy package.
import numpy

def deleteFirstRow(array):
    """Deletes the first row of a 2D array. 
    It returns a copy of the new array"""
    array = array[1::]    
    return array

def deleteFirstCol(array):
    """Deletes the first column of a 2D array. 
    It returns a copy of the new array"""
    array = array[:,1:]  
    return array

def deleteLastRow(array):
    """Deletes the last row of a 2D array. 
    It returns a copy of the new array"""
    array = array[:len(array)-1:]
    return array

def deleteLastCol(array):
    """Deletes the last column of a 2D array. 
    It returns a copy of the new array"""
    array = array[:,:-1]
    return array

def deleteNthRow(array,n):
    """Deletes the nth row, not 0 based. returns new array with row deleted."""
    start=n-1
    end=n
    array=numpy.delete(array,xrange(start,end),0)
    return array

def deleteNthCol(array,n):
    """Deletes the nth column, not 0 based. returns new array with column deleted."""
    start=n-1
    end=n
    array=numpy.delete(array,xrange(start,end),1)
    return array
    
def deleteRowSequence(array,start,end):
    """Deletes the entered sequence of indicides from the array.
    Note, input should not be 0 based, it begins at '1' for the 1st row.
    In addition, the 'end' should be inclusive.
    i.e. deleteRowSequence(arr,1,3) will delete the 1st,2nd and 3rd rows.
    1 1 1                                   4 4 4
    2 2 2 --deleteRowSequence(arr,1,3)-->   5 5 5
    3 3 3
    4 4 4
    5 5 5
    """
    start-=1
    array=numpy.delete(array,xrange(start,end),0)
    return array

def deleteColSequence(array,start,end):
    """Deletes the entered sequence of indicides from the array.
    Note, input should not be 0 based, it begins at '1' for the 1st column.
    In addition, the 'end' should be inclusive.
    i.e. deleteRowSequence(arr,1,3) will delete the 1st,2nd and 3rd rows.
    1 2 3 4 5                                  4 5 
    1 2 3 4 5 --deleteColSequence(arr,1,3)-->  4 5
    1 2 3 4 5                                  4 5
    """
    start-=1
    array=numpy.delete(array,xrange(start,end),1)
    return array

def getFirstRow(array): 
    """Returns the first row of the entered array."""
    row = array[0,:]  
    return row

def getFirstCol(array):
    """Returns the first column of entered array."""
    col = array[:,:1]
    return col

def getLastRow(array):
    """Returns the last row of the entered array."""
    row = array[len(array)-1::]
    return row
    
def getLastCol(array):
    """Returns the last column of the entered array."""
    col = array[:,len(array)-1:]
    return col

#Simple testing setup    
#if __name__ == '__main__':
#    arr=numpy.array([
#    ["a1","a2","a3","a4","a5"],
#    ["b1","b2","b3","b4","b5"],
#    ["c1","c2","c3","c4","c5"],
#    ["d1","d2","d3","d4","d5"],
#    ["e1","e2","e3","e4","e5"],
#    ])
#    newArr=getFirstRow(arr)
#    print newArr
#    print ""
#    print arr