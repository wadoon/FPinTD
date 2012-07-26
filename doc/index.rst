Recognition of Forbidden Pattern - |release|
============================================================

This software provides algorithms for checking if languages is in special language classes.
In special we use an forbidden pattern approach to decide if language defined with an
`deterministic finite automate <http://en.wikipedia.org/wiki/Deterministic_finite_automaton>`_.
We can decide the following classes: :math:`\mathcal B_{1/2,1}` and :math:`\mathcal L_{1/2,1,3/2}`.


.. math::
    \newcommand\mathdef{{=_{\text{def}}}}
    \newcommand\lclass[1]{{\mathcal{#1}}}
    \newcommand\dea[1]{{\mathcal{#1}}}
    \newcommand\reg[1]{{\mathbf{#1}}}
    \let\notmodels\nvDash

    \DeclareMathOperator{\Pol}{Pol}
    \DeclareMathOperator{\FU}{FU}
    \DeclareMathOperator{\BC}{BC}
    \DeclareMathOperator{\co}{co}
    \DeclareMathOperator{\BFS}{BFS}
    \DeclareMathOperator{\ZK}{ZK}
    \DeclareMathOperator{\sZK}{sZK}

    \DeclareMathOperator{\first}{first}
    \DeclareMathOperator{\last}{last}
    \DeclareMathOperator{\append}{append}

    \newcommand\FP{\ensuremath{\mathcal{FP}}\xspace}


The classes of the dot depth hierarchy is defined as follows:

.. math::
    \begin{align}
    \lclass B_{1/2}   &\mathdef ~ \FU( w_0\Sigma^* w_1 \Sigma^* \cdots \Sigma^* w_n)
                     && \text{für } n\ge 0 \wedge  w_i \in \Sigma^*, \\
    \lclass B_{n+1}   &\mathdef \BC(\lclass B_{n+1/2}) && \text{für } n \ge 0 \text{ und}\\
    \lclass B_{n+3/2} &\mathdef \Pol(\lclass B_{n+1})&& \text{für } n \ge 0\text{.}
    \end{align}


The classes of the Straubin-Therien depth hierarchy is defined as follows:

.. math::
    \begin{align}
        \lclass L_{1/2}  &\mathdef ~ \FU(\Sigma^*a_1\Sigma^* \cdots \Sigma^* a_m\Sigma^*)
                        && \text{für } m \ge 0 \wedge  a_i \in \Sigma, \\
        \lclass L_{n+1}  &\mathdef \BC(\lclass L_{n+1/2}) && \text{für } n \ge 0 \text{ und}\\
        \lclass L_{n+3/2} &\mathdef \Pol(\lclass L_{n+1}) && \text{für } n \ge 0  \text{.}
    \end{align}



:math:`\FU` is the finite union. :math:`\BC` the boolean closure under complement, intersection and union. :math:`\Pol` the polynominal closure (:math:`\FU + \cdot`).

If you need more information you should refer to [Weigl12]_ and [Schm00]_ as the primary sources. [Weigl12]_ explains the algorithms and [Schm00]_ the forbidden patterns.

Dependencies:

    * `ply (3.0 above) <http://www.dabeaz.com/ply/>`_
    * python >= 3.0


.. Authors:
    Alexander Weigl <weigla@fh-trier.de>

.. Version:
   |release| -- 2012-07-21


Software Overview
-------------------------------------------------------------

* Modules
    * :py:mod:`dea`: utilities for the algorithms
    * :py:mod:`trap`: for loading DFA in xml files. see http://trap.fh-trier.de for more information about TrAP
    * :doc:`algorithms <algorithms>`: this module contains the decision algorithms
    * :py:mod:`witnesscheck`: special module for providing a control mechanism for the decision algorithm
    * :py:mod:`generator`: Prototype and framework for generating algorithms
* Scripts
    * :doc:`dfa_in_lc <dfa_in_lc>` 


Indices and tables
-------------------------------------------------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`



License
--------------------------------------------------------------

This software is license under `GPL 3 <http://www.gnu.org/licenses/gpl.html>`_


Citation
--------------------------------------------------------------

**primary:**

.. [Schm00] Schmitz, Heinz: The Forbidden Pattern Approach to Concatenation Hierarchies. 2000. – https://fht.fh-trier.de/fileadmin/users/41/Publikationen/phd-thesis.pdf

.. [Weigl12] Weigl, Alexander: Algorthims for Forbidden Pattern Detection in Transitiondiagrams; 2012 (German).

*secondary:*

.. [AB02] Asteroth, Alexander; Baier, Christel: Theoretische Informatik - Eine Einführung in Berechenbarkeit, Komplexit und formale Sprachen mit 101 Beispielen. Pearson Studium, 2002

.. [Chr08] Christian Glaßer, Heinz Schmitz: Languages of Dot-Depth 3/2. In: Theory of Computing Systems 42 (2008), Nr. 2, S. 256–286. – http://www.springerlink.com/content/gv076686h4368427/

.. [CLRS09] Cormen, Thomas H.; Leiserson, Charles E.; Rivest, Ronald L.; Stein, Clifford: Introduction to Algorithms, Third Edition. 3rd. The MIT Press, 2009.

.. [CPP93] Cohen, Jo ̈lle; Perrin, Dominique; Pin, Jean-Eric: On the expressive power of temporal logic. In: Journal of Computer and System Sciences 46 (1993), Nr. 3, 271 - 294.

.. [HL11] Hofmann, M.; Lange, M.: Automatentheorie und Logik. Springer Verlag, 2011.

.. [Rot08] Rothe, Jörg: Komplexit ̈tstheorie und Kryptologie: Eine Einführung in Kryptokomplexit. Gabler Wissenschaftsverlage, 2008. 

.. [Sch00] Schmitz, Heinz: The Forbidden Pattern Approach to Concatenation Hierarchies. 2000. – https://fht.fh-trier.de/fileadmin/users/41/Publikationen/phd-thesis.pdf

.. [Tar72] Tarjan, Robert E.: Depth-First Search and Linear Graph Algorithms. In: SIAM J. Comput. 1 (1972), Nr. 2, S. 146–160







