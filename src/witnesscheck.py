# -*- encoding: utf-8 -*-
"""
This module provide functionality for checking the correctness of
witnesses from the forbidden pattern algorithm.
"""

__author__ = "Alexander Weigl <weigla@fh-trier.de>"
__date__ = "2012-06-12"


from dea import iterwords, DEA

class WitnessChecker(object):
    """
    Describes an checker for witnesses. Can be constructed by a string specification
    and a list of other WitnessChecker.

    A WitnessChecker has to implement the protocol:

    >>> MyChecker(object):
    >>>    def __call__(self, dea, witness):
    >>>        raise Exception("...") # if a constraint was violated
    >>>        return True # if every constraint was hit

    Also __str__ and __repr__ should be implemented for nice printing.
    """

    def __init__(self, spec=None, usecheckers=None):
        """
        """
        if usecheckers:
            self.call_checkers = usecheckers
        else:
            self.call_checkers = []

        self.spec = spec
        self.checks = []

        if spec:
            self.checks = parseSpecification(spec)

    def __iadd__(self, other):
        print("__iadd__")
        if type(other) is (list, tuple):
            self.checks += other
        else:
            self.checks.append(other)

    def __str__(self):
        string = ""

        if self.spec:
            string = "created from spec: \n %s \n#end spec\n" % self.spec

        if self.call_checkers:
            string += "rules from other checkers:\n+" + "-" * 20 + "\n|\t"
            for w in self.call_checkers:
                string += str(w).replace("\n", "\n|\t") + "\n+" + "-" * 20

        string += "\n"

        if self.checks:
            string += "checks:\n"
            for checker in self.checks:
                string += "\t" + str(checker) + "\n"

        return string

    def __repr__(self):
        return "WitnessChecker(%s,%s)" % \
               (repr(self.spec), repr(self.call_checkers))

    def __call__(self, dea, witness):
        for w in self.call_checkers:
            w(dea, witness)

        for checker in self.checks:
            checker(dea, witness)

        #False by Exception
        return True


def generateParser():
    import ply.yacc as yacc
    import ply.lex as lex

    literals = ("-", ",",'#')
    tokens = ["DELIM", "NAME" , "ANTI",  "ARROW" ]
    t_DELIM  = r"(\n|;)"
    t_ANTI   = r"<[#]>"
    t_ARROW  =r"->"
    t_ignore = " \t"

    def t_NAME(t):
        r'[a-zA-Z_][a-zA-Z_0-9]*?'
        return t

#    def t_newline(t):
#        r"\n+"
#        t.lexer.lineno += t.value.count("\n")
#        t.type = "DELIM"


    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        print(t)
        t.lexer.skip(1)


    start = "cnstrnts"

    def p_cnstrnts_recur(p):
        '''cnstrnts : cnstrnts DELIM def'''

        p[1].append(p[3])
        p[0] = p[1]

    def p_cnstrnts_anchor(p):
        '''cnstrnts : def'''
        p[0] = list(( p[1], ))


    def p_def_path(p):
        '''def :  NAME '-' NAME ARROW NAME
               |  NAME '-' NAME ARROW NAME '-' NAME'''
        if len(p) == 8:
            p[5] = p[5]+ "\\" +p[7]
        p[0] = path(p[1], p[3], p[5])


    def p_def_antivalence(p):
        '''def :  NAME ',' NAME ANTI NAME ',' NAME'''
        p[0] = antivalence(p[1], p[3], p[5], p[6])

    def p_def_neq(p):
        '''def : NAME '#' NAME'''
        p[0] = neq(p[1], p[3])


    def p_error(t):
        print(t)
        if t:
            print("Syntax error at '%s' on line %d:%d" % (t.value, t.lineno, t.lexpos))
            print(spec)

    def find_column(input,token):
        last_cr = input.rfind('\n',0,token.lexpos)
        if last_cr < 0:
            last_cr = 0
        column = (token.lexpos - last_cr) + 1
        return column

    lexer = lex.lex()
    yacc.yacc( debug = False, write_tables = False)
    return yacc

_parser =  generateParser()
parseSpecification = lambda spec: _parser.parse(spec.strip())


class composable(object):
    """
    Defines the addition operator for building lists:
    >>> a,b,c = composable(),composable(),composable()
    >>> a + b + c
    [ a , b , c]
    """

    def __add__(self, other):
        if type(other) in (list,):
            other.append(self)
            return other
        else:
            return list((self, other))


class path(composable):
    def __init__(self, *args):
        if len(args) == 1:
            self.start, self.words, self.target = parseSpecification(args[0])
        else:
            self.start, self.words, self.target = args

        self.start, self.words, self.target = map(str, self._tuple())

    def _tuple(self):
        return self.start, self.words, self.target

    def __repr__(self):
        return "path('{0} - {1} -> {2}')".format(*self._tuple())

    def __str__(self):
        return "check if \hat \delta({0}, {1}) = {2}".format(*self._tuple())

    def __call__(self, dea, witness, msg = ""):
        word = []
        for w in iterwords(self.words):
            word += witness[w]

        start_state = witness[self.start]
        end_state = dea(start_state, word)

        if  self.target == "F":
            ret = end_state in dea.F
        elif self.target in ("Q-F","Q\\F"):
            ret = end_state in (dea.Q - dea.F)
        else:
            target_state = witness[self.target]
            ret = end_state == target_state

        if not msg:
            msg = "%s - %s -> %s" % (self.start, self.words, self.target)

        if not ret:
            raise Exception("path check failed: " + msg)
        else:
            print(str(self), "is satisfied")
        return True


class antivalence(composable):
    def __init__(self, *args):
        if len(args) == 1:
            self.state1, self.word1, self.state2, self.word2 = parseSpecification(args[0])
        else:
            self.state1, self.word1, self.state2, self.word2 = args

    def _tuple(self):
        return self.state1, self.word1, self.state2, self.word2

    def __repr__(self):
        return "path('{0},{1} <#> {2},{3}')".format(*self._tuple())

    def __str__(self):
        return "check if \delta({0}, {1}) \in F <#> \delta({2},{3}) \\notin F".format(*self._tuple())

    def __call__(self,start1, word1, start2, word2, msg=""):
        word = []
        for w in iterwords(words):
            word += self.witness[w]

        end1 = self.dea(start1, word1)
        end2 = self.dea(start2, word2)

        if not (end1 in self.F ^ end2 not in self.F ):
            raise Exception("failed: " + msg)


class neq(composable):
    def __init__(self, *args):
        if len(args) == 1:
            self.state1, self.state2 = parseSpecification(args[0])
        else:
            self.state1, self.state2 = args

    def _tuple(self):
        return self.state1, self.state2

    def __repr__(self):
        return "path('{0} # {1}')" .format(*self._tuple())

    def __str__(self):
        return "check if {0} \\neq {0}".format(*self._tuple())

    def __call__(self, dea, witness):
        check = witness[self.state1] != witness[self.state2]
        if not check:
            raise Exception("neq failed: %s = %s" % (self.state1, self.state2))


checkWitnessL12 = WitnessChecker(
    """
    p - w -> q
    p - z -> F
    q - z -> Q - F
    p # q
    """
)

checkWitnessB12 = WitnessChecker(
    """
    p - v -> q
    q - v -> q
    """,
    (checkWitnessL12,))

checkWitnessL1_1 = WitnessChecker(
    """
    p - w -> q
    q - v -> p
    p,z <#> q,z
    """)

checkWitnessL1_2 = WitnessChecker("""
    q - u -> p
    p - v -> r
    r - u -> p
    q - v -> s
    s - u -> t
    t - v -> s
    t,z <#> p,z
    p # t
    """)


if __name__ == "__main__":
    print("Witness Checkers:")
    print(repr(checkWitnessL12))
    print(checkWitnessB12)
    print(checkWitnessL1_1)
    print(checkWitnessL1_2)