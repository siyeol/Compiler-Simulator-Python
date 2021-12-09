import re

class scanner:
    def __init__(self):
        self.list=[]
        
    def append(self, id, value=-1):
        self.list.append([id, value])
    

    def tokenizing(self, scan_bus):
        for i in range(len(scan_bus)):
            
            if not scan_bus[i] :                       # when token is empty
                continue
            
            tmp = scan_bus[i].replace('\t', '').replace('\n', '')
            
            if tmp == "(":
                self.append(2, -1)
            elif tmp == ")":
                self.append(3, -1)
            elif tmp == ";":
                self.append(4, -1)
            elif tmp == "int":
                self.append(5, -1)
            elif tmp == "char":
                self.append(6, -1)
            elif tmp == "{":
                self.append(7, -1)
            elif tmp == "}":
                self.append(8, -1)
            elif tmp == "IF":
                self.append(9, -1)
            elif tmp == "THEN":
                self.append(10, -1)
            elif tmp == "ELSE":
                self.append(11, -1)
            elif tmp == "=":
                self.append(12, -1)
            elif tmp == "EXIT":
                self.append(13, -1)
            elif tmp == "<":
                self.append(14, -1)
            elif tmp == "+":
                self.append(15, -1)
            elif re.findall('[0-9]', scan_bus[i]):
                # When there is a num and a value other than num in the token
                if(len(scan_bus[i])-len(re.findall('[0-9\t\n]', scan_bus[i])) != 0):
                    print("Error num")
                    continue
                else : 
                    self.append(16, scan_bus[i].replace('\t', '').replace('\n', ''))
            else:
                # When there is a word and a value other than word in the token
                if (len(scan_bus[i])-len(re.findall('[a-zA-Z]', scan_bus[i])) != 0):
                    continue
                else :
                    self.append(1, scan_bus[i].replace('\t', '').replace('\n', ''))

        print(f"{self.list}\n")
        return self.list
