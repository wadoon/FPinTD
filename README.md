Forbidden Patterns in Transition Diagrams
===============================================================================

    License:         BSD
    Author:          Alexander Weigl <weigla@fh-trier.de>
    Date:            31. Juli 2012
    Documentation:   http://fpintd.readthedocs.org

[![Build Status](https://secure.travis-ci.org/areku/FPinTD.png?branch=master)](http://travis-ci.org/areku/FPinTD)

This software package provides facilities for detecting forbidden pattern in deterministic finite automata (DFA).
DFA should be created with TrAP[^1] and saved for reading in with the _trap_ Python Module or by using the _dfa_ module.
Both are includes in this package. There are two version of the algorithms for the following language class:

 * Straubing-Therien: 1/2, 1, 3/2
 * dot-depth hierarchy: 1/2, 1, 3/2

for some Alphabet.


Installation
--------------------------------------------------------------------------------

These package can be installed with:

  python setup.py install [--user]

With the _--user_ parameter you can make a user local installation.

After installation you can call _fp_in_td_ script for checking DFAs in the TrAP[1] file format.

[1]: http://trap.fh-trier.de/

Literature 
---------------------------------------------------------------------------------


*Primary:*

[Sch00] Schmitz, Heinz: The Forbidden Pattern Approach to Concatenation Hierarchies. 2000. – https://fht.fh-trier.de/fileadmin/users/41/Publikationen/phd-thesis.pdf

[Weigl12] Weigl, Alexander: Algorithms for Forbidden Pattern Detection in Transitiondiagrams; 2012.

*Secondary:*

[AB02] Asteroth, Alexander; Baier, Christel: Theoretische Informatik - Eine Einführung in Berechenbarkeit, Komplexit und formale Sprachen mit 101 Beispielen. Pearson Studium, 2002

[Chr08] Christian Glaßer, Heinz Schmitz: Languages of Dot-Depth 3/2. In: Theory of Computing Systems 42 (2008), Nr. 2, S. 256–286. – http://www.springerlink.com/content/gv076686h4368427/

[CLRS09] Cormen, Thomas H.; Leiserson, Charles E.; Rivest, Ronald L.; Stein, Clifford: Introduction to Algorithms, Third Edition. 3rd. The MIT
Press, 2009.

[CPP93] Cohen, Jo ̈lle; Perrin, Dominique; Pin, Jean-Eric: On the expressive power of temporal logic. In: Journal of Computer and System Sciences 46 (1993), Nr. 3, 271 - 294.

[HL11] Hofmann, M.; Lange, M.: Automatentheorie und Logik. Springer Verlag, 2011.

[Rot08] Rothe, Jörg: Komplexit ̈tstheorie und Kryptologie: Eine Einführung in Kryptokomplexit. Gabler Wissenschaftsverlage, 2008. 

[Sch00] Schmitz, Heinz: The Forbidden Pattern Approach to Concatenation Hierarchies. 2000. – https://fht.fh-trier.de/fileadmin/users/41/Publikationen/phd-thesis.pdf

[Tar72] Tarjan, Robert E.: Depth-First Search and Linear Graph Algorithms. In: SIAM J. Comput. 1 (1972), Nr. 2, S. 146–160


