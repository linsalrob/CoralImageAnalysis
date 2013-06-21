
import sys


'''
A file to parse the different file classification formats that we are using. 

We have tab separated text, and also Dave's classification method

'''

class Parsers:
    ''' Different parsers for classification files'''

    def __init__(self, file):
        self.fin = open(file, 'r')

    def tab(self):
        '''Simple tab separated format with the assignment as the last element'''
        classification={}
        for line in self.fin:
            line = line.rstrip()
            l = line.split("\t")
            if l[-1] != '-':
                classification[l[0]] = l[-1]
        return classification

    def zawada(self):
        '''Dave Z's complex format'''
        classification={}
        assignment={}
        inassignment = False
        lastpart=0
        for line in self.fin:
            line = line.rstrip()
            # ignore blank lines
            if line == '':
                continue
            # I don't know what this line is for
            if line == 'dots=1':
                continue

            # where are we
            if line.startswith('--Classifications--'):
                continue
            if line.startswith('--Assignments--'):
                inassignment=True
                continue

            if inassignment:
                parts=line.split('::')
                path=parts[0].split('\\')
                filename=os.path.join(path)
                m=re.search('d.*\)\s*(\d+)\s*(\S*);', parts[1])
                if m.group(1) & m.group(2):
                    classification[filename]=assignment[m.group(1) + m.group(2)]
                elif m.group(1):
                    classification[filename]=assignment[m.group(1)]
                elif m.group(2):
                    sys.stderr.write("Error while parsing " + parts[1])
            else:
                line = line.lstrip()
                parts = line.split(':')
                if re.match('^\d', line):
                    assignment[parts[0]]=parts[1]
                    lastpart=parts[0]
                elif re.match('^\w', line):
                    assignment[lastpart + parts[0]]=parts[1]
                else:
                    sys.stderr.write("Error while parsing " + line + " for assignment")

        return classification


