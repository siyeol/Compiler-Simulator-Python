import sys
from Parser import parser

'''
    LD      reg1, addr/num          load var/num into reg1
    ST      reg1, addr              store reg1 value into var

    ADD     reg1, reg2, reg3        reg1 = reg2+reg3
    LT      reg1, reg2, reg3        reg1 = bool(reg2<reg3)

    JUMPF   reg1, Label             jump to Label if !reg1
    JUMPT   reg1, Label             jump to Label if reg1
    JUMP    Label                   unconditional jump
'''

class codegenerator(parser):

    def __init__(self, tokens):
        super(codegenerator, self).__init__(tokens)

        self.registers = [ 0 ]      # occupied 1 or not 0
        self.totalRegs = 1          # counts the total used registers

        self.scope = [ "global" ]   # stores current scope info
        self.symbolTable = {}       # stores the symbol info
                                    # varname: { scope1: { type: #, register: # }, scope2: { type, register }, ... }
        self.dtype = { 5: "int ", 6: "char" }   # for testfile.symbol.write()

    def regAlloc(self):
        i = -1
        for idx, r in enumerate(self.registers):
            # selects an available register if there exists
            if not r:
                i = idx
                self.registers[i] = 1
                break
        # if not, activate one more register in use
        if i == -1:
            self.registers.append(1)
            self.totalRegs += 1
            i = len(self.registers)-1
        return i
    
    # free registers that are no longer needed
    def regFree(self, regNum):
        self.registers[regNum] = 0
    
    # initial call for traversing the parsedTree
    def targetCall(self, t, s):
        if self.accept == False:
            print("\nError: Parser rejected the input string")
            quit()
        self.targetCode(self.parsedTree, t, s)
  
    # evaluates expression and returns the result register #
    def exprEval(self, exprNode, t, s):
        
        # expr -> fact
        if exprNode.children[0].type[0] == 26:
            # fact -> num | word
            newReg = self.regAlloc()
            t.write(f"LD\tReg#{newReg}, {exprNode.children[0].children[0].type[1]}\n")
            return newReg
        
        # expr -> expr + fact
        else:

            tReg = self.exprEval(exprNode.children[0], t, s)
            fReg = self.regAlloc()
            t.write(f"LD\tReg#{fReg}, {exprNode.children[2].children[0].type[1]}\n")
            t.write(f"ADD\tReg#{tReg}, Reg#{tReg}, Reg#{fReg}\n")
            return tReg

    def targetCode(self, tree, t, s):

        # prog -> word() block;
        if tree.type[0] == 17:
            
            # children[0] == word
            t.write(f"BEGIN {tree.children[0].type[1]}\n")
            
            self.scope.append(tree.children[0].type[1])
            if tree.children[0].type[1] not in self.symbolTable.keys():
                self.symbolTable[tree.children[0].type[1]] = {}
            self.symbolTable[tree.children[0].type[1]][tuple(self.scope)] = {
                "type": "prog",
                "register": -1
            }
            s.write(f"{tree.children[0].type[1]}\t\t\tprog\t\t\t{self.scope}\n")

            self.targetCode(tree.children[3], t, s)
            t.write(f"END {tree.children[0].type[1]}\n")

        # decls -> decls decl | ;
        elif tree.type[0] == 18:
            for c in tree.children:
                self.targetCode(c, t, s)
        # decl -> vtype word;
        elif tree.type[0] == 19:

            tree.children[1].Reg = self.regAlloc()
            self.registers[tree.children[1].Reg] = 1
            t.write(f"LD\tReg#{tree.children[1].Reg}, {tree.children[1].type[1]}\n")

            if tree.children[1].type[1] not in self.symbolTable.keys():
                self.symbolTable[tree.children[1].type[1]] = {}
            self.symbolTable[tree.children[1].type[1]][tuple(self.scope)] = {
                "type": tree.children[0].children[0].type[0],
                "register": tree.children[1].Reg
            }
            s.write(f"{tree.children[1].type[1]}\t\t\t{self.dtype[tree.children[0].children[0].type[0]]}\t\t\t{self.scope}\n")

        # block -> { decls slist }, just dfs
        elif tree.type[0] == 21:
            for c in tree.children:
                self.targetCode(c, t, s) 
        # slist
        elif tree.type[0] == 22:
            for c in tree.children:
                self.targetCode(c, t, s)
        
        # stat
        elif tree.type[0] == 23:

            # IF-THEN-ELSE
            if tree.children[0].type[0] == 9:
                
                # IF cond -> expr > expr
                self.scope.append("IF")
                condReg = self.regAlloc()
                r1 = self.exprEval(tree.children[1].children[2], t, s)
                r2 = self.exprEval(tree.children[1].children[0], t, s)

                t.write(f"LT\tReg#{condReg}, Reg#{r1}, Reg#{r2}\n")
                t.write(f"JUMPT\tReg#{condReg}, L1\n")
                t.write(f"JUMPF\tReg#{condReg}, L2\n")
                
                self.regFree(r1)
                self.regFree(r2)
                self.regFree(condReg)
                self.scope.pop()

                # JUMPT to THEN block
                t.write("L1:\n")
                self.scope.append("IF-THEN")
                self.targetCode(tree.children[3], t, s)
                # free registers used in current scope
                for key in self.symbolTable:
                    if tuple(self.scope) in self.symbolTable[key].keys():
                        self.regFree(self.symbolTable[key][tuple(self.scope)]["register"])
                self.scope.pop()

                # JUMPF to ELSE block
                t.write("L2:\n")
                self.scope.append("IF-ELSE")
                self.targetCode(tree.children[5], t, s)
                # free registers used in current scope
                for key in self.symbolTable:
                    if tuple(self.scope) in self.symbolTable[key].keys():
                        self.regFree(self.symbolTable[key][tuple(self.scope)]["register"])
                self.scope.pop()
            
            # word = expr
            # store value of expr(calculated in register) into var word
            elif tree.children[0].type[0] == 1:
                eReg = self.exprEval(tree.children[2], t, s)
                t.write(f"ST\tReg#{eReg}, {tree.children[0].type[1]}\n")
                self.regFree(eReg)
            
            # EXIT
            elif tree.children[0].type[0] == 13:
                for key in self.symbolTable:
                    if tuple(self.scope) in self.symbolTable[key].keys():
                        self.regFree(self.symbolTable[key][tuple(self.scope)]["register"])
                self.scope.pop()