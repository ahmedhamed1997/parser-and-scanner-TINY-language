class Scanner:

    def __init__(self, specialSymbols=None, reservedWords=None):
        if reservedWords is None:
            self.reservedWords = ["if", "then", "else", "end", "repeat",
                                  "until", "read", "write"]

        if specialSymbols is None:
            self.specialSymbols = ["+", "-", "*", "/", "=",
                                   "<", "(", ")", ";"]
        self.number = "0123456789"
        self.identifier = "abcdefghijklmnopqrstuvwxyz"
        self.value = ""
        self.type = ""
        self.currentState = 1
        self.Position = 0
        self.token = []
        self.code_list = []
        self.tokens_list = []

    def takeToken(self, nextState):
        if self.currentState == 1:  # start state
            if nextState == "{":
                self.currentState = 2
            elif nextState == ":":
                self.type = ",ASSIGNMENT"
                self.currentState = 3
            elif nextState in self.number:
                self.type = ",NUMBER"
                self.value = nextState
                self.currentState = 5
            elif nextState in self.identifier:
                self.type = ",IDENTIFIER"
                self.value = nextState
                self.currentState = 4
            elif nextState in self.specialSymbols:
                self.type = ",SPECIAL SYMBOL"
                self.value = nextState
                self.currentState = 6
            elif nextState != " " and nextState != "\n":
                self.currntState = -1
        elif self.currentState == 2:  # INCOMMENT state
            if nextState == "}":
                self.currentState = 1
                self.value = ""
        elif self.currentState == 3:  # INASSIGN state
            if nextState == "=":
                self.value = ":="
                self.currentState = 6
        elif self.currentState == 4:  # INID state
            if nextState in self.identifier:
                self.value += nextState
            else:
                self.currentState = 6

                if self.value in self.reservedWords:
                    self.type = ",RESERVED WORD"
                    self.Position -= 1
                else:
                    self.Position -= 1
        elif self.currentState == 5:  # INNUM state
            if nextState in self.number:
                self.value += nextState
            else:
                self.currentState = 6
                self.Position -= 1
        elif self.currentState == 6:  # final state
            self.token.append(self.value + self.type)
            self.Position -= 1
            self.currentState = 1
        self.Position += 1

    def in_out_file(self, inputFile="TINY_in_code.txt", outputFile="output.txt"):
        inFile = open(inputFile, "a+")
        inFile.write("\n")
        inFile = open(inputFile)
        # print(inFile.readlines())
        for line in inFile.readlines():
            endOfLine = len(line[:-1])
            while self.Position <= endOfLine:
                self.takeToken(line[self.Position])
            self.Position = 0
            if self.currentState < 0:
                break
        inFile.close()

        outFile = open(outputFile, "w")

        for i in self.token:
            x = i.split(",")
         #   print(x)
            if x[1] == "RESERVED WORD" or x[1] == "SPECIAL SYMBOL" or x[1] == "ASSIGNMENT":
                temp: object = x[0]
                x[1] = temp
            out1 = x[0].lower()
            out2 = x[1].lower()

            self.code_list.append(out1)
            self.tokens_list.append(out2)
            outFile.write(i + "\n")

        #print(self.code_list)
        #print(self.tokens_list)

        outFile.close()


a = Scanner()
a.in_out_file()
