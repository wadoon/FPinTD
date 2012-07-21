algorithms{1,2} modules
=======================================



We describe the interface for the algorithms.

Both modules: :py:mod:`algorithms1` and :py:mod:`algorithms2` have the same interface
and provide the algorithm for the same decision problems.

Additional we describe here the used forbidden pattern. These pattern is taken from _[Schm00].

Each forbidden pattern is defined as conjunction of constraints over an DFA
:math:`\mathcal A = (Q, \Sigma, \delta, s_0, F)`. You should consider, that if an DFA :math:`\dea A`
satisfied a forbidden pattern iff. :math:`L(\dea A) \not in \mathbb C`.
Forbidden can be shown graphical in an similiar way to transition diagrams.

Straubing-Therien
--------------------------------------------------------------

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

          \begin{align}
           \mathbb{L}_{1/2}  \mathdef
                & \quad \exists{ p,q \in Q} \colon \\
                & \qquad \exists{ x,z,w \in \Sigma^* }  \colon\\
                & \qquad ~ \quad\, \hat \delta (q_0, x) = p\\
                & \qquad ~ \wedge \hat \delta (p, w) = q \\
                & \qquad ~ \wedge \hat \delta (p, z) = + \\
                & \qquad ~ \wedge \hat \delta (q, z) = -
           \end{align}

.. graphviz::

   digraph G {
     graph [rankdir=LR];
     start [color=white, shape=none, label=""];
     F [label="+"];
     G [label="-"];
     start -> q0;
     q0 -> p [label=x]
     p -> q [label=w]
     p->F;
     q -> G;
   }


.. math::
          \begin{align}
            \mathbb{L}^1_{1} \mathdef
               & \quad \exists{ p,q \in Q} \colon \\
               & \qquad \exists{ x,v,w,z \in \Sigma^* } \colon\\
               & \qquad ~ \quad\, \hat \delta (q_0, x) = p \\
               & \qquad ~ \wedge \hat \delta (p, w) = q \\
               & \qquad ~ \wedge \hat \delta (q, v) = p \\
               & \qquad ~ \wedge \hat \delta (p, z) \in F
               \nLeftrightarrow  \hat \delta (q, z) \in F\\
            \mathbb{L}^2_{1} \mathdef
              & \quad \exists{ p,q \in Q} \colon \\
              & \qquad \exists{ x,v,w,z \in \Sigma^* } \colon\\
              & \qquad ~ \quad\,\hat \delta (q_0, x) = p \\
              & \qquad ~ \wedge \hat \delta (q, v) = s \\
              & \qquad ~ \wedge \hat \delta (q, u) = p \\
                \nonumber \\
              & \qquad ~ \wedge \hat \delta (p, v) = r \\
              & \qquad ~ \wedge \hat \delta (r, u) = p \\
                    \nonumber \\
              & \qquad ~ \wedge \hat \delta (s, u) = t \\
              & \qquad ~ \wedge \hat \delta (t, v) = s \\
                    \nonumber \\
              & \qquad ~ \wedge \hat \delta (p, z) \in F
                \nLeftrightarrow  \hat \delta (t, z) \in F
          \end{align}

.. graphviz::

   digraph G {
     graph [rankdir=LR];
     start [color=white, shape=none, label=""];
     F [label="+"];
     G [label="-"];
     start -> q0;
     q0 -> p [label=x]
     p -> q [label=w]
     q -> p [label=v]
     p->F;
     q -> G;
   }

.. graphviz::

           digraph G {
             graph [rankdir=dLR];
             start [color=white, shape=none, label=""];
             F [label="+/-"];
             G [label="+/-"];
             start -> q0;
             q0 -> q [label=x]
             q -> p [label=u]
             p -> r [label=v]
             r -> p [label=u]
             q -> s [label=u]
             s -> t [label=v]
             t -> s [label=u]
             p->F;
             t->G;
           }

.. math::
          \begin{align}
            \mathbb B_1 \mathdef   & \quad \exists{ p,q \in Q} \colon \\
                              & \qquad \exists{ x,z \in \Sigma^* } \colon\\
                              & \qquad \exists{ v,w \in \Sigma^+ } \colon\\
                              & \qquad ~ \quad\, \hat \delta (q_0, x) = p \\
                              & \qquad ~ \wedge \hat \delta (p, w) = q \\
                              & \qquad ~ \wedge \hat \delta (p, z) = + \\
                              & \qquad ~ \wedge \hat \delta (q, z) = - \\
                              & \qquad ~ \wedge \hat \delta (q, v) = q \\
                              & \qquad ~ \wedge \hat \delta (p, v) = p \\
                              & \qquad ~ \wedge \alpha(w) \subseteq \alpha(v)
          \end{align}

.. graphviz::

               digraph G {
                 graph [rankdir=LR];
                 start [color=white, shape=none, label=""];
                 F [label="+/-"];
                 G [label="+/-"];
                 start -> q0;
                 q0 -> p [label=x]
                 p -> q [label=w]
                 p->p [label=v];
                 q->q [label=v];
                 q->F;
                 p -> G;
               }

Dot-Depth Hierarchy
------------------------------------

.. math::
  \begin{align}
    \mathbb{B}_{1/2} \mathdef & \quad \exists{ p,q \in Q} \colon \\
                       & \qquad \exists{ x,z \in \Sigma^* } \colon\\
                       & \qquad \exists{ v,w \in \Sigma^+ } \colon\\
                       & \qquad ~ \quad\,\hat \delta (q_0, x) = p  \\
                       & \qquad ~ \wedge \hat \delta (p, w) = q \\
                       & \qquad ~ \wedge \hat \delta (p, z) = + \\
                       & \qquad ~ \wedge \hat \delta (q, z) = - \\
                       & \qquad ~ \wedge \hat \delta (p, v) = p \\
                       & \qquad ~ \wedge \hat \delta (q, v) = q 
  \end{align}


.. graphviz::

   digraph G {
     graph [rankdir=LR];
     start [color=white, shape=none, label=""];
     F [label="+"];
     G [label="-"];
     start -> q0;
     q0 -> p [label=x]
     p -> q [label=w
     p->p [label=v];
     q->q [label=v];
     p->F;
     q -> G;
   }

.. math::
    \begin{align} 
        \mathbb{B}_1 \mathdef   & \quad \exists{ p,q \in Q} \colon \\
                          & \qquad \exists{ x,y,y',u,v,z \in \Sigma^* } \colon\\
                          & \qquad \exists{ w,w' \in \Sigma^+ } \colon\\
                          & \qquad ~ \quad\,\hat \delta (q_0, x) = q_1\\
                          & \qquad ~ \wedge \hat \delta (q_1, y) = q_2 &
                          & \wedge \hat \delta (q_2, y') = q_1  \\
                          & \qquad ~ \wedge \hat \delta (q_1, w) = q_1 &
                          & \wedge  \hat \delta (q_2, w') = q_2   \\ \nonumber \\
                          & \qquad ~ \wedge \hat \delta (q_5, u) = q_3 &
                          & \wedge \hat \delta (q_3, v) = q_5 \\
                          & \qquad ~ \wedge \hat \delta (q_3, w) = q_5 &
                          & \wedge \hat \delta (q_5, w') = q_3 \\
                          \nonumber \\
                          & \qquad ~ \wedge \hat \delta (q_6, v) = q_4 &
                          & \wedge \hat \delta (q_4, u) = q_6 \\
                          & \qquad ~ \wedge \hat \delta (q_4, w) = q_4 &
                          & \wedge \hat \delta (q_6, w') = q_6 \\
                          \nonumber \\
                          & \qquad ~ \wedge \hat \delta (q_6, z) \in F
                          \nLeftrightarrow \hat \delta (q_3, z) \in F
                           \\
                          & \qquad ~ \wedge \hat \delta (q1, u) = q_3 
                          \\
                          & \qquad ~ \wedge \hat \delta (q_2, v) = q_4 
    \end{align}


.. graphviz::

           digraph G {
             graph [rankdir=LR];
             start [color=white, shape=none, label=""];
             F [label="+/-"];
             G [label="+/-"];
             start -> q0;
             q0 -> q1 [label=x]
             q1 -> q2 [label=y]
             q2 -> q1 [label="y'"]

             q1 -> q3 [label=u]
             q3 -> q5 [label=v]
             q5 -> q3 [label=u]

             q2 -> q4 [label=u]
             q4 -> q6 [label=v]
             q6 -> q4 [label=u]

             q1->q1 [label=w]
             q3->q3 [label=w]
             q4->q4 [label=w]

             q1->q2 [label="w'"]
             q6->q5 [label="w'"]
             q6->q6 [label="w'"]

             q3->F;
             q6->G;
           }

algorithms1
---------------------------------------------------

.. automodule:: algorithms1
   :members:
   :undoc-members:

algorithms2
---------------------------------------------------

.. automodule:: algorithms2
   :members:
   :undoc-members:
