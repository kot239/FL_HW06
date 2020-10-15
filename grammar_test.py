import pytest
from parser import parse_file

def test_atom():
    assert parse_file('test_files/atom_test.txt', '--atom') == '''(ATOM a)
(ATOM a b c)
(ATOM a (ATOM b c))
(ATOM a (ATOM b c))
(ATOM a (ATOM b c) d)
(ATOM a (ATOM b c) (ATOM d))
(ATOM a (ATOM b c) (ATOM d))
(ATOM a (ATOM b c) (ATOM d))
(ATOM a B C (ATOM cons X (ATOM cons Y nil)))
'''

def test_relation():
    assert parse_file('test_files/relation_test.txt', '--relation') == '''(RELATION HEAD((ATOM a)))
(RELATION HEAD((ATOM a b)))
(RELATION HEAD((ATOM a)) BODY((ATOM a)))
(RELATION HEAD((ATOM a)) BODY((ATOM a)))
(RELATION HEAD((ATOM a)) BODY((ATOM a b)))
(RELATION HEAD((ATOM a b)) BODY((ATOM a b)))
(RELATION HEAD((ATOM a b)) BODY(DISJ ((ATOM a))(CONJ ((ATOM b))((ATOM c)))))
(RELATION HEAD((ATOM a b)) BODY(DISJ ((ATOM a))(CONJ ((ATOM b))((ATOM c)))))
(RELATION HEAD((ATOM a b)) BODY(CONJ (DISJ ((ATOM a))((ATOM b)))((ATOM c))))
(RELATION HEAD((ATOM a b)) BODY(DISJ ((ATOM a))(DISJ ((ATOM b))((ATOM c)))))
(RELATION HEAD((ATOM a b)) BODY(CONJ ((ATOM a))(CONJ ((ATOM b))((ATOM c)))))
(RELATION HEAD((ATOM a (ATOM b (ATOM c)))) BODY((ATOM a b)))
(RELATION HEAD((ATOM a X Y)) BODY((ATOM clone (ATOM cons (ATOM x) (ATOM cons (ATOM y) (ATOM cons (ATOM z) nil))))))
(RELATION HEAD((ATOM print G)) BODY((ATOM clone G (ATOM cons X nil))))
'''

def test_type():
    assert parse_file('test_files/type_test.txt', '--type') == '''(TYPE a (ATOM b))
(TYPE a (ARROW (ATOM b) X))
(TYPE filter (ARROW (ARROW A (ATOM o)) (ARROW (ATOM list a) (ARROW (ATOM list a) (ATOM o)))))
(TYPE filter (ARROW (ARROW A (ATOM o)) (ARROW (ATOM list A) (ARROW (ATOM list A) (ATOM o)))))
(TYPE filter (ARROW (ARROW A (ATOM o)) (ARROW (ATOM list A) (ARROW (ATOM list A) (ATOM o)))))
(TYPE a (ATOM b))
(TYPE d (ARROW (ATOM a) (ATOM b)))
'''

def test_typeexpr():
    assert parse_file('test_files/typeexpr_test.txt', '--typeexpr') == '''(ATOM a)
(ARROW Y X)
(ARROW Y X)
(ARROW (ARROW A B) C)
(ARROW A (ARROW B C))
(ARROW (ATOM list (ATOM list A)) (ARROW (ATOM list A) (ATOM o)))
(ARROW (ATOM pair A B) (ARROW (ARROW A C) (ARROW (ARROW B D) (ATOM pair C D))))
'''

def test_module():
    assert parse_file('test_files/module_test.txt', '--module') == '''(MODULE name)
(MODULE name_123)
'''

def test_list():
    assert parse_file('test_files/list_test.txt', '--list') == '''(ATOM nil)
(ATOM cons (ATOM a) nil)
(ATOM cons A (ATOM cons B nil))
(ATOM cons (ATOM a (ATOM b c)) (ATOM cons B (ATOM cons C nil)))
(ATOM cons (ATOM a) T)
(ATOM cons (ATOM cons (ATOM a) nil) T)
(ATOM cons (ATOM cons H T) (ATOM cons (ATOM a) nil))
(ATOM cons (ATOM cons (ATOM name) (ATOM cons (ATOM password) nil)) (ATOM cons (ATOM cons (ATOM id) (ATOM cons (ATOM number) nil)) Qwerty))
'''

def test_prolog():
    assert parse_file('test_files/prolog.txt', '--prog') == '''(MODULE main)
(TYPE print (ARROW X (ATOM show Y)))
(RELATION HEAD((ATOM print (ATOM cons X nil))) BODY((ATOM show (ATOM cons (ATOM x) T))))
(RELATION HEAD((ATOM print (ATOM cons T nil))) BODY((ATOM show T)))
'''

def test_atom_err():
    assert not parse_file('test_files/atom_err1.txt', '--atom')
    assert not parse_file('test_files/atom_err2.txt', '--atom')
    assert not parse_file('test_files/atom_err3.txt', '--atom')

def test_type_err():
    assert not parse_file('test_files/type_err1.txt', '--type')
    assert not parse_file('test_files/type_err2.txt', '--type')
    assert not parse_file('test_files/type_err3.txt', '--type')

def test_module_err():
    assert not parse_file('test_files/module_err1.txt', '--module')
    assert not parse_file('test_files/module_err2.txt', '--module')
    assert not parse_file('test_files/module_err3.txt', '--module')
