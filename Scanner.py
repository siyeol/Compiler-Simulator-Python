import re

class scanner:
    def __init__(self):
        self.list=[]
        
    def append(self, id, value=-1):
        self.list.append([id, value])
    

    def tokenizing(self, btw):
        for i in range(len(btw)):
            
            if not btw[i] :                       # when token is empty
                continue
            elif btw[i].replace('\t', '').replace('\n', '')=="(":
                self.append(2, -1)
            elif btw[i].replace('\t', '').replace('\n', '')== ")":
                self.append(3, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == ";":
                self.append(4, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "int":
                self.append(5, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "char":
                self.append(6, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "{":
                self.append(7, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "}":
                self.append(8, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "IF":
                self.append(9, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "THEN":
                self.append(10, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "ELSE":
                self.append(11, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "=":
                self.append(12, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "EXIT":
                self.append(13, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == ">":
                self.append(14, -1)
            elif btw[i].replace('\t', '').replace('\n', '') == "+":
                self.append(15, -1)
            elif re.findall('[0-9]', btw[i]):
                # When there is a num and a value other than num in the token
                if(len(btw[i])-len(re.findall('[0-9\t\n]', btw[i])) != 0):
                    print("Error num")
                    continue
                else : 
                    self.append(16, btw[i].replace('\t', '').replace('\n', ''))
            else:
                # When there is a word and a value other than word in the token
                if (len(btw[i])-len(re.findall('[a-zA-Z]', btw[i])) != 0):
                    continue
                else :
                    self.append(1, btw[i].replace('\t', '').replace('\n', ''))

        print(f"{self.list}\n")
        return self.list