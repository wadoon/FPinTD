'''

:Version: 30.05.2011

:Authors:
    knopsa,
    Alexander Weigl (re-documentation for sphinx)
'''

import sys
import tempfile
from os import path

from xml.etree import ElementTree as ET


_DEA = "DEA"
_NEA = "NEA"
_ENEA = "ENEA"
_EPSILON = "\u03B5"
_EMPTYSET = "\u2205"
_KLEENE_STAR = "\u002A"
_ALTERNATION = "\u002B"
_LPARENTHESIS = "\u0028"
_RPARENTHESIS = "\u0029"
_DEFAULT_FILE = tempfile.gettempdir() + "/trap.xml"



#
# Different implementations
# for Python 2 and Python 3 compatibility.
#
if sys.version_info[0] < 3:
#    print("Trap doesn't support Python " +
#     		sys.version_info[0].__str__()+ ".X!")
    _python_input = raw_input
else:
    _python_input = input


def load(filename=None, alt_order=False):
    """Loads a model from the given path.

    Parameter:
    :param filename: the path of the source-file
    :param alt_order: the order of the tulple in case of an automata.
                      If false then[Q, Sigma, delta, start, F]
                      else [Sigma, Q, delta, start, F]

    The Return-value is a finite state machine or a regular expression.

    Finite State Machine:
    A finite state Machine is a list
    [Q, Sigma, delta, start, F] or [Sigma, Q, delta, start, F] with
    - Q is a set of states (set of int values)
    - Sigma is a a alphabet (set of str values of length 1)
    - delta is the transition function  (dictionary)
    - start is the start-state (int value)
    - F is a set of accept states (set of int values)

    Regular Expression:
    The return value is a list [exp, Sigma] with
    - exp is the regular Expression (str vaule)
    - Sigma is a a alphabet (set of int values)

    :return: a list of five elements, see above
    """

    def read_alphabet(xml_EA):
        """Creates a set (Alphabet) from an ElementTree.Element"""

        token_Set = set([])
        for token in xml_EA.find("alphabet"):
            token_Set.add(token.text)
        return token_Set

    def load_ea(xml_EA, alt_order):
        """Creates a finite state machine Machine from Element"""

        #
        # read states
        #  
        is_DEA = xml_EA.attrib["type"] == _DEA
        xml_states = xml_EA.find("states")
        str_state_set = set([])
        int_state_set = set([])
        str_accepting_set = set([])
        state_map = {}
        for xml_state in xml_states:
            str_state = xml_state.attrib["name"]
            if str_state.isdigit() and (len(str_state) == 1 or str_state[0] != "0"):
                state_map[str_state] = int(str_state)
                int_state_set.add(state_map[str_state])
            else:
                str_state_set.add(str_state)
            if xml_state.attrib["accepting"].lower() == "true":
                str_accepting_set.add(str_state)
        i = 0

        for str_state in sorted(str_state_set):
            while i in int_state_set:
                i += 1
            int_state_set.add(i)
            state_map[str_state] = i
            #
        # create Accepting Set
        #    
        int_accepting_set = set([])
        for str_state in str_accepting_set:
            int_accepting_set.add(state_map[str_state])


        #
        # read Transitons
        #
        delta = {}
        xml_transitions = xml_EA.find("transitions")
        for xml_trans in xml_transitions:
            start = xml_trans.attrib["start"]
            end = xml_trans.attrib["end"]
            token = xml_trans.attrib["token"]
            if is_DEA:
                delta[state_map[start], token] = state_map[end]
            elif (state_map[start], token) in delta:
                delta[state_map[start], token].add(state_map[end])
            else:
                delta[state_map[start], token] = set([state_map[end]])

        start_state = state_map[xml_EA.find("startState").attrib["name"]]

        ea = [int_state_set, read_alphabet(xml_EA), delta, start_state, int_accepting_set]
        if alt_order == True:
            ea = _twist(ea)

        #weigl:        print(xml_EA.attrib["type"] + " loaded")
        return ea

    def load_regex(xml_regex):
        """Creates a  regular Expression from an ElementTree.Element"""

        str_exp = xml_regex.find("expression").text
        sigma = read_alphabet(xml_regex)

        print("reg. Expression" + " loaded")
        return str_exp, sigma


    try:
        if filename == None:
            if not path.isfile(_DEFAULT_FILE):
                print("File does not exist")
                return None
            filename = _DEFAULT_FILE

        tree = ET.parse(filename)
        xml_EA = tree.find("automata")
        xml_EA
        if (xml_EA != None):
            return load_ea(xml_EA, alt_order)
        else:
            xml_regex = tree.find("regularExpression")
            if (xml_regex != None):
                return load_regex(xml_regex)
            else:
                print("Illegal file format")
                return None
    except IOError as e:
        print("'" + e.filename + "'" + ": " + e.strerror)
        return None
    except KeyError as e:
        print(e.__str__() + " is not a State")
        return None


def save_dea(dea, filename=None, alt_order=False):
    """Writes an DEA to the given file.
    
    :param dea: an deterministic finite-state machines
    :param filename: the path of the target-file
    :param alt_order: the order of the DEA-tulple
                    false:  [Q, Sigma, delta, start, F]
                    true: [Sigma, Q, delta, start, F]
    
    
    :return: true, if the file was written successfully.
    
     A deterministic finite-state Machine is a list  
    [Q, Sigma, delta, start, F] with
    - Q is a set of states (set of int values)
    - Sigma is a a alphabet (set of str values of length 1)
    - delta is the transition function  
      (dictionary: state X token -> state)
    - start is the start-state (int value)
    - F is a set of accept states (set of int values)
    """
    if alt_order == True:
        dea = _twist(dea)
    return _save_ea(filename, dea, _DEA)


def save_nea(nea, filename=None, alt_order=False):
    """Writes an NEA to the given file.
    
    :param nea: an nondeterministic finite-state machines
    :param filename: the path of the target-file
    :param alt_order: the order of the NEA-tulple
                 false:  [Q, Sigma, delta, start, F] 
                 true: [Sigma, Q, delta, start, F]
    
    :return: true iff the file was written successfully.
    
    A nondeterministic finite-state machines with epsilon moves Machine is a
    list  [Q, Sigma, delta, start, F] with
    - Q is a set of states (set of int values)
    - Sigma is a a alphabet (set of str values of length 1)
    - delta is the transition function  
      (dictionary: state X (token + epsilon) -> set of states)
    - start is the start-state (int value)
    - F is a set of accept states (set of int values)
    
    """
    if alt_order == True:
        nea = _twist(nea)
    return _save_ea(filename, nea, _NEA)


def save_enea(enea, filename=None, alt_order=False):
    """Writes an ENEA to the given file.

    :param enea: an nondeterministic finite-state machines  with epsilon moves
    :param filename: the path of the target-file
    :param alt_order:
        the order of the ENEA-tulple
        false:  [Q, Sigma, delta, start, F]
        true: [Sigma, Q, delta, start, F]
    
    :return:true, iff the file was written successfully.
    
    A nondeterministic finite-state machines with epsilon moves is a
    list  [Q, Sigma, delta, start, F] with
    - Q is a set of states (set of int values)
    - Sigma is a a alphabet (set of str values of length 1)
    - delta is the transition function  
      (dictionary: state X (token + epsilon) -> set of states)
    - start is the start-state (int value)
    - F is a set of accept states (set of int values)
    """
    if alt_order == True:
        enea = _twist(enea)
    return _save_ea(filename, enea, _ENEA)


def _save_ea(filename, ea, type):
    """Writes an EA to a file."""

    def add_transition(xml_transitions, from_state, token, to_state):
        xml_trans = ET.SubElement(xml_transitions, "transition")
        xml_trans.attrib["start"] = from_state.__str__()
        xml_trans.attrib["token"] = token.__str__()
        xml_trans.attrib["end"] = to_state.__str__()

    type = type.upper()

    if is_ea_consistent(ea, type) == False:
        return False

    [states, alphabet, delta, start_state, accepting_set] = ea

    xml_model = ET.Element("model")

    xml_automata = ET.SubElement(xml_model, "automata", {"type": type})

    ET.SubElement(xml_automata, "startState", {"name": start_state.__str__()})

    xml_states = ET.SubElement(xml_automata, "states")

    for state in states:
        xml_state = ET.SubElement(xml_states, "state")
        xml_state.attrib["name"] = state.__str__()
        xml_state.attrib["accepting"] = (state in accepting_set).__str__().lower()

    xml_transitions = ET.SubElement(xml_automata, "transitions")
    for q, t in delta:
        if type == _DEA:
            add_transition(xml_transitions, q, t, delta[q, t])
        else:
            for q2 in delta[q, t]:
                add_transition(xml_transitions, q, t, q2)

    xml_automata.append(_create_alphabet(alphabet))

    tree = ET.ElementTree(xml_model)
    return _write(tree, filename, type.upper())


def is_ea_consistent(ea, type):
    """ Checks if the given ea is consistent.
    
    :return:
        false, iff the ea uses any state/token,
        which is not a member of the state-set/ alphabet.
    """

    [states, alphabet, delta, start_state, accepting_set] = ea

    if not is_sigma_consistent(alphabet):
        return False

    for q in accepting_set:
        if q not in states:
            print(q.__str__() + " is not a State")
            return False

    if type not in (_DEA, _NEA, _ENEA):
        print("Illegal type '" + type + "'")
        return False

    if start_state not in states:
        print(start_state.__str__() + " is not a State")
        return False

    for q, t in delta:
        if t not in alphabet and not ( t == _EPSILON and type == _ENEA):
            print(t.__str__() + " is not a Token")
            return False
        if q not in states:
            print(q.__str__() + " is not a State")
            return False

        if type == _DEA:
            if delta[q, t] != None and delta[q, t] not in states:
                print(delta[q, t].__str__() + " is not a State")
                return False
        else:
            for q2 in delta[q, t]:
                if q2 not in states:
                    print(q2.__str__() + " is not a State")
                    return False


def is_sigma_consistent(sigma):
    for t in sigma:
        if type(t) != str:
            print("Illegal alphabet token")
            return False
        if len(t) != 1:
            print("Illegal alphabet token '" + t + "'")
            return False
        if t in (_EPSILON, _EMPTYSET, _KLEENE_STAR, _ALTERNATION, _RPARENTHESIS, _LPARENTHESIS ):
            print("Illegal special token '" + t + "'")
            return False
    return True


def save_regex(expression, sigma, file_name=None):
    """Writes an regular Expression to the given file.
    
    :param expression: The regular Expression.
    :param sigma: the Alphabet.
    :param file_name: The name of the file.
    
    :return: true, iff the file was written successfully.
    """
    if not is_sigma_consistent(sigma):
        return False
    xml_model = ET.Element("model")
    xml_regex = ET.SubElement(xml_model, "regularExpression")

    xml_exp = ET.SubElement(xml_regex, "expression")
    xml_exp.text = expression

    xml_regex.append(_create_alphabet(sigma))

    tree = ET.ElementTree(xml_model)
    return _write(tree, file_name, "reg. Expression")


def _twist(ea):
    [A, B, delta, q0, F] = ea
    return [B, A, delta, q0, F]


def _write(tree, filename, type):
    """Writes a ElementTree to a file."""
    message = type + " saved"
    try:
        if filename != None:
            if path.isfile(filename):
                print("File does already exist!")
                choice = None
                while choice == None:
                    print('Do you want to replace the existing file? "Yes"/"No"')
                    choice = _python_input().lower()

                    if choice != "yes" and choice != "no":
                        choice = None
                if choice == "no":
                    print("Canceled")
                    return None
            message = message + "(" + filename + ")"
        else:
            filename = _DEFAULT_FILE

        tree.write(filename, encoding="UTF-8")
        print(message)
        return True

    except IOError as e:
        print("'" + e.filename + "'" + ": " + e.strerror)
        return False


def _create_alphabet(sigma):
    """Creates a subtree from an alphabet."""
    xml_alphabet = ET.Element("alphabet")
    for t in sigma:
        xml_token = ET.SubElement(xml_alphabet, "token")
        xml_token.text = t.__str__()
    return xml_alphabet

