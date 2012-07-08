
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.2'

_lr_method = 'LALR'

_lr_signature = '\x99\xed\xa7\xfe\xf5\xd1\x91w\xd2\xc6\xff\x08\xda\x01\x03g'
    
_lr_action_items = {'RPAREN':([6,7,13,],[-6,9,-5,]),'NAME':([0,1,2,3,5,8,10,12,14,17,18,],[4,4,-1,6,-2,11,13,15,16,-3,-4,]),'INVSTMT':([15,16,],[17,18,]),'ARROW':([11,],[14,]),'COMMA':([6,7,13,],[-6,10,-5,]),'LPAREN':([0,1,2,5,17,18,],[3,3,-1,-2,-3,-4,]),'IN':([9,],[12,]),'MINUS':([4,],[8,]),'$end':([1,2,5,17,18,],[0,-1,-2,-3,-4,]),}

_lr_action = { }
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = { }
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'slist':([0,],[1,]),'plist':([3,],[7,]),'statement':([0,1,],[2,5,]),}

_lr_goto = { }
for _k, _v in _lr_goto_items.items():
   for _x,_y in zip(_v[0],_v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = { }
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> slist","S'",1,None,None,None),
  ('slist -> statement','slist',1,'p_slist_stmt','/home/weigla/docs/fht/06/Thesis/code/src/generator.py',68),
  ('slist -> slist statement','slist',2,'p_slist_recur','/home/weigla/docs/fht/06/Thesis/code/src/generator.py',74),
  ('statement -> LPAREN plist RPAREN IN NAME INVSTMT','statement',6,'p_statement_in','/home/weigla/docs/fht/06/Thesis/code/src/generator.py',79),
  ('statement -> NAME MINUS NAME ARROW NAME INVSTMT','statement',6,'p_statement_bfs','/home/weigla/docs/fht/06/Thesis/code/src/generator.py',84),
  ('plist -> plist COMMA NAME','plist',3,'p_plist_recur','/home/weigla/docs/fht/06/Thesis/code/src/generator.py',88),
  ('plist -> NAME','plist',1,'p_plist_NAME','/home/weigla/docs/fht/06/Thesis/code/src/generator.py',93),
]
