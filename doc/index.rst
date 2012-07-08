.. Recognition of Forbidden Pattern documentation master file, created by
   sphinx-quickstart on Mon May  7 18:19:23 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Recognition of Forbidden Pattern
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
    \lclass B_{1/2}   &\mathdef ~ w_0\Sigma^* w_1 \Sigma^* \cdots \Sigma^* w_n
                     && \text{für } n\ge 0 \wedge  w_i \in \Sigma^*, \\
    \lclass B_{n+1}   &\mathdef \BC(\lclass B_{n+1/2}) && \text{für } n \ge 0 \text{ und}\\
    \lclass B_{n+3/2} &\mathdef \Pol(\lclass B_{n+1})&& \text{für } n \ge 0\text{.}
    \end{align}


The classes of the Straubin-Therien depth hierarchy is defined as follows:

.. math::
    \begin{align}
        \lclass L_{1/2}  &\mathdef ~ \Sigma^*a_1\Sigma^* \cdots \Sigma^* a_m\Sigma^*
                        && \text{für } m \ge 0 \wedge  a_i \in \Sigma, \\
        \lclass L_{n+1}  &\mathdef \BC(\lclass L_{n+1/2}) && \text{für } n \ge 0 \text{ und}\\
        \lclass L_{n+3/2} &\mathdef \Pol(\lclass L_{n+1}) && \text{für } n \ge 0  \text{.}
    \end{align}

If you need more information you should refer to [Weigl12]_ and [Schm00]_.

Dependencies:
    * `ply (3.0 above) <http://www.dabeaz.com/ply/>`_
    * python >= 3.0
.. Authors:
    Alexander Weigl <weigla@fh-trier.de>

.. Version:
    0.1alpha -- 2012-06-16


Software Overview
-------------------------------------------------------------

* Modules

    * `dea <dea>`_: utilities for the algorithms
    * `trap <trap>`_: for loading DFA in xml files. see http://trap.fh-trier.de for more information about TrAP
    * `algorithms <algorithms>`_: this module contains the decision algorithms
    * `witnesscheck <witnesscheck>`_ special module for providing a control mechanism for the decision algorithm
    * `generator <generator>`_

Contents
-------------------------------------------------------------

.. toctree::
   :maxdepth: 2



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

.. [Weigl12] Weigl, Alexander: Algorthims for Forbidden Pattern Detection in Transitiondiagrams; 2012 (German).


.. [Schm00] Schmitz, Heinz: The Forbidden Pattern Approach to Concatenation Hierarchies, 2000 (English). http://fh-trier.de?id=schmitz




