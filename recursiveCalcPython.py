import sys
#<expr> -> <term> { <addop> <term> }
#<addop> -> + | -
#<term> -> <factor> { <mulop> <factor> }
#<mulop> -> *
#<factor> -> ( <expr> ) | number

#Class to represent nodes in the parse tree
class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

#Class for parsing and to construct a parse tree for a given expression
class Parser:
    def __init__(self, expression):
        self.expression = expression  #Initialize the expression to parse
        self.position = 0  #Initialize the current position in the expression

    def parse(self):
        try:
            #Start parsing the expression and construct the parse tree
            parse_tree = self.expr()
            #Check if the entire expression has been parsed
            if self.position == len(self.expression):
                return parse_tree
            else:
                self.errorParse()  
        except:
            self.errorParse()
    
    #Function to report early error and exit the program
    def error(self):
        sys.stderr.write("Early error, this string is illegal!.\n")
        sys.exit(1)

    #Function to report an error and exit the program
    def errorParse(self):
        sys.stderr.write("Error, cannot display parse tree, program will exit.\n")
        sys.exit(1)

    #Parse and construct the parse tree for expressions
    def expr(self):
        left = self.term()  #Parse the left operand
        while self.position < len(self.expression) and self.expression[self.position] in ('+', '-'):
            operator = self.expression[self.position]  # Get the operator (+ or -)
            self.position += 1  #Move to the next character
            right = self.term()  #Parse the right operand
            left = Node(operator, left, right)  #Create a new node for the operation
        return left  #Return the parse tree for the expression

    #Parse and construct the parse tree for terms
    def term(self):
        left = self.factor()  #Parse the left factor
        while self.position < len(self.expression) and self.expression[self.position] in ('*', '/'):
            operator = self.expression[self.position]  #Get the operator (* or /)
            self.position += 1  #Move to the next character
            right = self.factor()  #Parse the right factor
            left = Node(operator, left, right)  #Create a new node for the operation
        return left  #Return the parse tree for the term

    #Parse and construct the parse tree for factors
    def factor(self):
        if self.position < len(self.expression) and self.expression[self.position] == '(':
            self.position += 1  
            temp = self.expr()  #Parse the expression within the parentheses
            if self.position < len(self.expression) and self.expression[self.position] == ')':
                self.position += 1  
            else:
                self.error()  #Report an error if the closing parenthesis is missing
        elif self.position < len(self.expression) and self.expression[self.position].isdigit():
            start = self.position  #Start of a numeric value
            while self.position < len(self.expression) and self.expression[self.position].isdigit():
                self.position += 1  
            temp = int(self.expression[start:self.position])  #Convert the numeric value to an integer
        else:
            self.error()  #Report an error if the factor is not a valid expression or numeric value
        return temp  #Return the factor's value

#Function to display the parse tree on the screen
def display_parse_tree(node, prefix="", is_left=True):
    if isinstance(node, Node):
        print(prefix, "|-- " if is_left else "-- ", node.value)
        prefix += "    |" if is_left else "     "
        display_parse_tree(node.left, prefix, True)
        display_parse_tree(node.right, prefix, False)
    else:
        print(prefix, "|-- " if is_left else "-- ", node)

def evaluate_tree(node):
    if isinstance(node, Node):
        left = evaluate_tree(node.left)
        right = evaluate_tree(node.right)
        if node.value == '+':
            return left + right
        elif node.value == '-':
            return left - right
        elif node.value == '*':
            return left * right
        elif node.value == '/':
            return left / right
    else:
        return node

def calculator_program():
    print("~~~~~ A RECURSIVE-DESCENT CALCULATOR ^w^ ~~~~")
    print("||||||      By: Tiffany & Jocelin      ||||||")
    print("=============================================")
    print("the valid operations are +, -, * and /")
    print("Enter the calculation string, e.g. '34+6*56'")
    print("=============================================")
    expression = input("Enter an expression: ")
    expression = ''.join(expression.split())
    
    print("Your input", expression)
    parser = Parser(expression)
    parse_tree = parser.parse()
    display_parse_tree(parse_tree)

    result = evaluate_tree(parse_tree)
    print(f"Result = {result}")

calculator_program()

