#test_classification_unittest.py
#unittest class for Classification.py
import sys
import os
import unittest
import re

sys.path.append('../Modules/')
import Classification


class TestClassification(unittest.TestCase):
    
    def setUp(self):
        """
        !!!NOTE:
        I don't think an image file is correct here, I believe it is looking for some kind of tab seperated
        value sheet, I'll have to look around the 'test' folder and see if there is one I can easily use.
        Contd:
        I looked into the 'test' file and found a file which appears to have several features which this program refers to,
        i.e, a line with --Classifications-- and --Assignments--- ect.
        """
        self.File = '../test/test_classifications.txt'     
        self.parsers = Classification.Parsers(self.File)
        
        
    def test_tab(self):
        tabClass = self.parsers.tab()
        
        fin = open(self.File,'r')
        classification = {}
        for line in fin:
            line = line.rstrip()
            l = line.split("\t")
            if l[-1] != '-':
                classification[l[0]] = l[-1]

        self.assertEqual(tabClass,classification)

    def test_zawadaClassifications(self):
        zawadaClassifications = self.parsers.zawadaClassifications()
        classifications = {
            '0':'Indeterminate', 
            '1':'Seagrasses', 
            '2':'Hardbottom', 
            '3':'Senile coral reef', 
            '4':'Coral rubble', 
            '5':'Carbonate sand', 
            '6':'Live reef', 
            '1 a':'Thalassia', 
            '1 b':'Syringodium', 
            '1 c':'Mixed'
        }
        self.assertEqual(zawadaClassifications,classifications)
        
    def test_zawada(self):
        zawada = self.parsers.zawada()  
        
        fin = open(self.File,'r')
        classification={}
        assignment={}
        inassignment = False
        lastpart = 0
        for line in fin:
            line = line.rstrip()
            if line =='':
                continue
            if line == 'dots=1':    #This is noted as being ambigious in the code, but is neccessary.
                continue            #On line 14 of test_classifications.txt there is a statement 'dots=1'
            if line.startswith('--Classifications--'):
                continue
            if line.startswith('--Assignments--'):
                inassignment=True
                continue
            
            if inassignment:
                parts=line.split('::')
                path=parts[0].split('\\')
                filename=path[0]
                if len(path) > 1:
                    filename=os.path.join(path[0],path[1])
                m=re.search('d.*\)\s*(\d+)\s*(\S*);', parts[1])
                if m==None:
                    continue
                if(m.group(1) !='') & (m.group(2) !=''):
                    classification[filename]=assignment[m.group(1) + m.group(2)] 
                elif m.group(1) !='':
                    classification[filename]=assignment[m.group(1)]
                elif m.group(2) !='': 
                    sys.stderr.write("Error while parsing "+ parts[1])
            else:
                line = line.lstrip()
                parts = line.split(':')
                if re.match('^\d', line):
                    assignment[parts[0]] = parts[1]
                    lastpart=parts[0]
                elif re.match('^\w', line):
                    assignment[lastpart + parts[0]]=parts[1]
                else:
                    sys.stderr.write("Error while parsing " + line + " for assignment")
            
        self.assertEqual(zawada,classification)
            

if __name__=="__main__":
    unittest.main()