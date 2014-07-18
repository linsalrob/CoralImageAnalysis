#munger.py
#Data munging helper for 2D ndarrays from numpy package.
import numpy

def testFunction(array):
    length=len(array)
    array = array[:length,1:]
    return array

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

def deleteLastCol(array):
    """Deletes the last column of a 2D array. 
    It returns a copy of the new array"""
    array = array[:,:-1]
    return array

def deleteLastRow(array):
    """Deletes the last row of a 2D array. 
    It returns a copy of the new array"""
    array = array[:len(array)-1:]
    return array

def deleteNthCol(array,n):
    """docstring for deleteNthColumn"""
    pass
    
def deleteNthRow(array,n):
    """docstring for deleteNthRow"""
    pass

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

def getFirstCol(array):
    """Returns the first column of entered array."""
    col = array[:,:1]
    return col
    
def getFirstRow(array): 
    """Returns the first row of the entered array."""
    row = array[0,:]  
    return row

def getLastRow(array):
    row = array[len(array)-1::]
    return row
    
if __name__ == '__main__':
    arr=numpy.array([
    ["a1","a2","a3","a4","a5"],
    ["b1","b2","b3","b4","b5"],
    ["c1","c2","c3","c4","c5"],
    ["d1","d2","d3","d4","d5"],
    ["e1","e2","e3","e4","e5"],
    ])
    newArr=deleteColSequence(arr,2,)
    print newArr
    print ""
    print arr