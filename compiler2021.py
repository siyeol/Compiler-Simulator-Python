from Scanner import scanner
from Parser import parser
from CodeGenerator import codegenerator
import sys

# ----------------------- Compiler1 - Scanner: tokenizes the input source code -----------------------

inputFile = sys.argv[1]
srcFile = open(inputFile, "r")
scan_bus = ""
read_buffer = srcFile.readline()
while read_buffer:
    scan_bus += read_buffer
    read_buffer = srcFile.readline()
scan_bus = scan_bus.strip().split(" ")
tokens = scanner().tokenizing(scan_bus)



# ------------------------------- Initializing output file descriptors -------------------------------

target = open("testfile.code", "w")
symbol = open("testfile.symbol", "w")
symbol.write("*************************************************************************\n")
symbol.write("Name\t\t\tType\t\t\tScope\n")
symbol.write("*************************************************************************\n")



# ----------------------------- Compiler2 - SLR Parser and Code Generator -----------------------------

compiler = codegenerator(tokens)
compiler.parse()
compiler.targetCall(target, symbol)



# -------------------------------------- Some result instructions --------------------------------------

print("\nCheck the target code in testfile.code")
print("Check the symbol table in testfile.symbol\n")
print("Total %d registers have been used for execution\n"%(compiler.totalRegs))

target.close()
symbol.close()
