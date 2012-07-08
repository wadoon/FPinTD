"""
This modules provides an simple interface for generating
algorithm for forbidden pattern from an intermediate language:

    slist           : statement
                    | slist statement


    statement       : LPAREN plist RPAREN IN NAME INVSTMT
                    | NAME MINUS NAME ARROW NAME  INVSTMT


    plist           : plist COMMA NAME
                    | NAME

Please see: http://www.dabeaz.com/ply/ply.html for more details of ply.

"""

__author__ = 'Alexander Weigl <weigla@fh-trier.de>'
__date__ = '2012-06-13'

import ply.lex  as lex
import ply.yacc as yacc

#__all__ = ["generateCode"]

reserved = {
    'in' : 'IN',
}


tokens = ["INVSTMT" , "NAME", "LPAREN", "RPAREN", "COMMA","ARROW", "MINUS"] + list(reserved.values())

t_LPAREN = r"\("
t_RPAREN = r"\)"
t_COMMA  = r","
t_ARROW  = r"->"
t_MINUS  = r"-"
t_ignore = " \t"


def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'NAME')    # Check for reserved words
    return t

def t_INVSTMT(t):
    r'\[.*?\]'
    t.value = t.value.strip("[]")
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

lex.lex()


#start symbol
start = "slist"

def p_slist_stmt(t):
    '''slist : statement'''
    print("recur anchor slist", type(t[1]))
    t[1].innerBlock = "return True"
    t[0] = t[1]

def p_slist_recur(t):
    '''slist : slist statement'''
    t[1].innerBlock = t[2] #building a chained list
    t[0] = t[1]

def p_statement_in(t):
    '''statement : LPAREN plist RPAREN IN NAME INVSTMT'''
    print("InStatement")
    t[0] = InStatement( t[2], t[5], t[6])

def p_statement_bfs(t):
    '''statement : NAME MINUS NAME ARROW NAME  INVSTMT'''
    t[0] = BfsStatement( t[1] , t[3], t[5], t[6])

def p_plist_recur(t):
    '''plist : plist COMMA NAME'''
    t[1].append(t[3])
    t[0] = t[1]

def p_plist_NAME(t):
    '''plist : NAME'''
    t[0] = list(( t[1] , ))


def p_error(t):
    print(t)
    print("Syntax error at '%s'" % t.value)

yacc.yacc()


def indent(string, level = 1, fmt = " " * 4):
    s = fmt*level
    return s+ string.replace("\n", "\n"+s)

def codegen(tupl):
    code = ""
    newline = False
    print(tupl)
    for obj in tupl:
        if type(obj) is tuple:
            s = indent(codegen(obj))
            code += "\n"+s
        else:
            if newline:
                code += "\n"
            newline = True
            code += str(obj)

    return code


class InStatement(object):
    def __init__(self, vars, inSet, invariant , innerBlock = ""):
        self.vars = vars
        self.inSet = inSet
        self.invariant = "True" if invariant == "" else invariant
        self.innerBlock = innerBlock

    def __str__(self):
        """code generation"""
        return codegen((
            "for (%s) in %s:" % (",".join(self.vars), self.inSet),
                ("if %s:" % self.invariant,
                    (self.innerBlock,))))

def BfsStatement(object):
    def __init__(self, start, word, end, invariant, innerBlock = ""):
        self.start = start
        self.word  = word
        self.end   = end
        self.invariant = invariant
        self.innerBlock = innerBlock

    def __str__(self):
        ib = indent(str(self.innerBlock),2)
        return "for (%s,%s) in dea.search(%s):\n\tif %s:\n%s" %(
                    self.end, self.word, self.start, self.invariant, ib
                )


def generateCode(spec):
    """
    :param spec: a str
    :return: the generated code with a str:
    """
    return str( yacc.parse( spec ) )

if __name__ == "__main__":
    for s in ("q -v-> q", "[]", "[q=p]", "(p,r,a) in T"):
        lex.input(s)
        while True:
            tok = lex.token()
            print(tok)
            if not tok: break
        print()

    p = ( yacc.parse("(q,p,r) in Q []") )
    print(type(p))
    print(p)
