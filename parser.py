import re
import sys
from parsec import *

whitespace = regex(r'\s+', re.MULTILINE)
ignore = many(whitespace)

lexeme = lambda p: p << ignore  # skip all ignored characters.

openbr = lexeme(string('('))
closebr = lexeme(string(')'))
opensq = lexeme(string('['))
closesq = lexeme(string(']'))
con = lexeme(string(','))
dot = lexeme(string('.'))
tail = lexeme(string('|'))
dis = lexeme(string(';'))
defi = lexeme(string(':-'))
mod = lexeme(string('module'))
arrow = lexeme(string('->'))
tpe = lexeme(string('type'))
lit = lexeme(regex(r'\b((?!module|type)([a-z][A-Za-z_0-9]*))\b'))
var = lexeme(regex(r'[A-Z][A-Za-z_0-9]*'))

# -----------------------------

@generate
def cons_comma():
    yield con
    a = yield (atom ^ var ^ cons)
    l = yield cons_seq
    return '(ATOM cons ' + str(a) + ' ' + str(l) + ')'

@generate
def cons_tail():
    yield tail
    l = yield var
    return str(l)

@generate
def cons_end():
    yield con
    l = yield (atom ^ var ^ cons)
    return '(ATOM cons ' + str(l) + ' nil)'

cons_seq = cons_comma ^ cons_tail ^ cons_end

# -----------------------------

# -----------------------------

@generate
def cons():
    yield opensq
    a = yield (atom ^ var ^ cons)
    l = yield many(cons_seq)
    yield closesq
    if not l:
        return '(ATOM cons ' + str(a) +' nil)'
    return '(ATOM cons ' + str(a) + ' ' +  ' '.join(l) + ')'

@generate
def empty_cons():
    yield opensq
    yield closesq
    return '(ATOM nil)'

@generate
def exp_br_seq():
    yield openbr
    l = yield (atom ^ exp_br_seq)
    yield closebr
    return str(l)

seq = var ^ cons ^ empty_cons ^ lit ^ exp_br_seq

# -----------------------------

# -----------------------------

"""
atom = lit seq
     | (atom)
"""

@generate
def atom():
    l = yield lit
    e = yield many(seq)
    if not e:
        return '(ATOM ' + str(l) + ')'
    return '(ATOM ' + str(l) + ' ' + ' '.join(e) + ')'

# -----------------------------

# -----------------------------

"""
subatom = ( disj ) 
        | atom
"""

@generate
def exp_subatom():
    yield openbr
    e = yield disj
    yield closebr
    return str(e)

subatom = exp_subatom ^ atom

# -----------------------------

# -----------------------------

"""
conj = subatom , conj
     | subatom
"""

@generate
def exp_conj():
    e1 = yield subatom
    yield con
    e2 = yield conj
    return 'CONJ (' + str(e1) + ')(' + str(e2) + ')'

conj = exp_conj ^ subatom

# -----------------------------

# -----------------------------

"""
disj = conj ; disj
     | conj
"""
@generate
def exp_disj():
    e1 = yield conj
    yield dis
    e2 = yield disj
    return 'DISJ (' + str(e1) + ')(' + str(e2) + ')'

disj = exp_disj ^ conj

# -----------------------------

# -----------------------------

"""
types = atom -> 
      | (types atom)
"""

@generate
def expr_types():
    a = yield param_type
    yield arrow
    b = yield types
    return '(ARROW ' + str(a) + ' ' + str(b) + ')'

@generate
def br_type():
    yield openbr
    l = yield types
    yield closebr
    return str(l)

param_type = atom ^ var ^ br_type

types = expr_types ^ param_type

# -----------------------------

# -----------------------------

"""
sentence = atom . 
         | atom :- disj .
"""

@generate
def sen():
    l = yield atom
    yield dot
    return '(RELATION HEAD(' + str(l) + '))'

@generate
def big_sen():
    l1 = yield atom
    yield defi
    l2 = yield disj
    yield dot
    return '(RELATION HEAD(' + str(l1) + ') BODY(' + str(l2) + '))'

@generate
def module():
    yield mod
    l = yield lit
    yield dot
    return '(MODULE ' + str(l) + ')'

@generate
def typedef():
    yield tpe
    l1 = yield lit
    e = yield types
    yield dot
    return '(TYPE ' + str(l1) + ' ' + str(e) + ')'

expr = sen ^ big_sen ^ module ^ typedef

# -----------------------------

program = ignore >> many(expr)

start_atom = ignore >> many(atom)

start_types = ignore >> many(types)

start_typedef = ignore >> many(typedef)

start_module = ignore >> many(module)

start_relation = ignore >> many(sen ^ big_sen)

start_list = ignore >> many(cons ^ empty_cons)

def parse_file(file_name, flag):

    input_file = open(file_name)
    inp = input_file.read()
    input_file.close()

    output_file = open(file_name + '.out', 'w')

    regex = re.compile(r'^[ \n\t]*$')
    if regex.match(inp):
        output_file.write("Empty file")
        output_file.close()
        return "Empty file"

    if flag == '--type' or flag == '--module' or flag == '--relation' or flag == '--prog':
        inp = inp.replace('\n', ' ')
        inp = inp.replace('.', '.\n')

    tokens = inp.split('\n')

    ans_str = ""

    try:
        for token in tokens:
            if not regex.match(token):
                if flag == '--atom':
                    outp = start_atom.parse(token)
                elif flag == '--typeexpr':
                    outp = start_types.parse(token)
                elif flag == '--type':
                    outp = start_typedef.parse(token)
                elif flag == '--module':
                    outp = start_module.parse(token)
                elif flag == '--relation':
                    outp = start_relation.parse(token)
                elif flag == '--list':
                    outp = start_list.parse(token)
                else:
                    outp = program.parse(token)
                if not outp:
                    output_file.write("Can't build syntax tree")
                    output_file.close()
                    return None
                else:
                    ans_str = ans_str + outp[0] + '\n'
    except:
        output_file.write("Can't build syntax tree")
        output_file.close()
        return None

    output_file.write(ans_str)
    output_file.close()
    return ans_str

if __name__ == "__main__":
    if len(sys.argv[1:]) == 1:
        arg = '--prog'
    else:
        arg = sys.argv[2]
    parse_file(sys.argv[1], arg)
