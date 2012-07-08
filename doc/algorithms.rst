algorithms module
=======================================

Test

.. graphviz::

   digraph G {
     graph [rankdir=LR];
     start [color=white, shape=none, label=""];
     F [label="+"];
     G [label="-"];
     start -> q0;
     q0 -> q1 -> q2;
     q1->q1 [label=v];
     q2->q2 [label=v];
     q1->F;
     q2 -> G;
   }

.. automodule:: algorithms
   :members:
   :undoc-members:
