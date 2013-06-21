import sys 
sys.path.append('../Modules')

import Classification

testF = 'test_classifications.txt'
cp = Classification.Parsers(testF)
cl = cp.zawada()
