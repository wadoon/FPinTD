(ns trapclj.core)

(load-file "combinatorics.clj")

(import '(de.fhtrier.trap.algorithms.implementation.deaalgorithms
           DeaComplement
           DeaDecideEmptiness
           DeaDecideFiniteness
           DeaDecidePermutationFree
           DeaDecidePermutationFreeHelp
           DeaDeleteNotReachable
           DeaDeleteUnnecessaryStates
           DeaDeterministicCompletion
           DeaDotDepthB05
           DeaDotDepthL05
           DeaIntersection
           DeaInverseHomomorphism
           DeaMinimization
           DeaMirror
           DeaToNea
           DeaToRegEx
           DeaUnion
           ValidateDea))

(import '(de.fhtrier.trap.algorithms.implementation.eneaalgorithms
           ENeaConcatenation
           ENeaConcatenationN
           ENeaDeleteNotReachable
           ENeaIntersection
           ENeaIteration
           ENeaMirror
           ENeaToNea
           ENeaUnion))

(import '(de.fhtrier.trap.algorithms.implementation.neaalgorithms
           NeaConcatenation
           NeaConcatenationN
           NeaDeleteNotReachable
           NeaIntersection
           NeaIteration
           NeaMirror
           NeaToDea
           NeaToENea
           NeaUnion))

(import '(de.fhtrier.trap.algorithms.implementation.regExp
           CachedRegExMatcher
           RegExHomomorphism
           RegExMatcher
           RegExMirror
           RegExToENea
           RegExToNea))

(import '(de.fhtrier.trap.models.regExp.mathmodel RegExParser))
(import '(de.fhtrier.trap.models.automata.mathmodel State Dea Nea ENea))
(import '(de.fhtrier.trap.utils LoadModel SaveModel))
(import '(de.fhtrier.trap.models.utilities CharToken))
(import de.fhtrier.trap.models.automata.visualmodel.VisualEA)


(defn alpha-list-n [n]
  (map symbol (map str (take n "abcdefghijklmnopqrstuvwxyz"))))

(defmacro generate-operation [cls arity]
  (let [alg-sym (gensym)]
    `(fn [~@(alpha-list-n arity)]
       (let [~alg-sym (new ~cls)]
         ~@(map
             (fn [n a] `(.setParameter ~alg-sym ~a ~n))
             (range arity) (alpha-list-n arity))
         (.run ~alg-sym)
         (first (.getResult ~alg-sym))))))

(defn dfa? [automaton]
  (instance? Dea automaton))

(defn nfa? [automaton]
  (instance? Nea automaton))

(defn enfa? [automaton]
  (instance? ENea automaton))

(defn get-alphabet [string]
  (char-array
    (remove (fn [x] (or
                      (= x \))
                      (= x \()
                      (= x \*)
                      (= x \+)
                      (= x \€)))
      (distinct string))))

(defn regex [input]
  (.parse (new RegExParser) input (get-alphabet input)))






(def dfa-complement (generate-operation DeaComplement 1))
(def dfa-decide-emptiness (generate-operation DeaDecideEmptiness 1))
(def dfa-decide-finiteness (generate-operation DeaDecideFiniteness 1))
(def dfa-decide-permutationfree (generate-operation DeaDecidePermutationFree 1))
(def dfa-delete-not-reachable (generate-operation DeaDeleteNotReachable 1))
(def dfa-delete-unnecessary-states (generate-operation DeaDeleteUnnecessaryStates 1))
(def dfa-ddh-12 (generate-operation DeaDotDepthB05 1))
(def dfa-sth-12 (generate-operation DeaDotDepthL05 1))
(def dfa-intersection (generate-operation DeaIntersection 2))
(def dfa-inverse-homorphism (generate-operation DeaInverseHomomorphism 1))
(def dfa-minimization (generate-operation DeaMinimization 1))
(def dfa-mirror (generate-operation DeaMirror 1))
(def dfa->nfa (generate-operation DeaToNea 1))
(def dfa->regex (generate-operation DeaToRegEx 1))
(def dfa-union (generate-operation DeaUnion 2))
(def dfa-validate (generate-operation ValidateDea 1))


(def enfa-concat (generate-operation ENeaConcatenation 2))
(def enfa-concat-3 (generate-operation ENeaConcatenationN 3))
(def enfa-concat-4 (generate-operation ENeaConcatenationN 4))
(def enfa-concat-5 (generate-operation ENeaConcatenationN 5))
(def enfa-concat-6 (generate-operation ENeaConcatenationN 6))
(def enfa-delete-not-reachable (generate-operation ENeaDeleteNotReachable 1))
(def enfa-intersection (generate-operation ENeaIntersection 2))
(def enfa-iteration (generate-operation ENeaIteration 1))
(def enfa-mirror (generate-operation ENeaMirror 1))
(def enfa->nea (generate-operation ENeaToNea 1))
(def enfa-union (generate-operation ENeaUnion 2))

(def nfa-concat (generate-operation NeaConcatenation 2))
(def nfa-concat-3 (generate-operation NeaConcatenationN 3))
(def nfa-concat-4 (generate-operation NeaConcatenationN 4))
(def nfa-concat-5 (generate-operation NeaConcatenationN 5))
(def nfa-concat-6 (generate-operation NeaConcatenationN 6))
(def nfa-delete-not-reachable (generate-operation NeaDeleteNotReachable 1))
(def nfa-intersection (generate-operation NeaIntersection 1))
(def nfa-iteration (generate-operation NeaIteration 1))
(def nfa-mirror (generate-operation NeaMirror 1))
(def nfa->dfa (generate-operation NeaToDea 1))
(def nfa->enea (generate-operation NeaToENea 1))
(def nfa-union (generate-operation NeaUnion 1))


(def regex-mirror (generate-operation RegExMirror 1))
(def regex->enea (generate-operation RegExToENea 1))
(def regex->nea (generate-operation RegExToNea 1))



(defn dfa-from-file [filename]
  (. LoadModel loadFile (new java.io.File filename) nil))

(defn char-token? [obj]
  (instance? CharToken obj))

(defn state? [s]
  (instance? State s))

(defn state [obj]
  (if (state? obj)
    obj
    (new State (str obj))))


(defn char-token [char]
  (if (char-token? char) char
    (new CharToken char)))


(defn dfa-from-regex [regx]
  (nfa->dfa (regex->nea (regex regx))))

(defn states [automaton]
  (map (fn [x] x)
       (.getAllStates automaton)))

(defn sigma [dfa]
  (map (fn [x] x)
       (.getSigma dfa)))
  
(defn acceptable-states [dfa]
  (filter (fn [x] (.isAccepting dfa x))
	  (states dfa)))

(defn transitions [automaton]
  (map (fn [t]
         (list (.getStartState t)
               (.getToken t)
               (.getEndState t)))
       (.getAllTransitions automaton)))

(defn add-state [fa s]
  (.addState fa (state s)))

(defn add-char [fa c]
  (.addCharToken fa (char-token c)))

(defn add-transition [fa from sym to]
  (.addTransition fa
    (state from) (char-token sym) (state to)))

(defn start-state [a]
  (.getStartState a))

(defn start-state! [fa s]
  (.setStartState fa (state s)))

(defn save-fa [fa name]
  (let [model (new VisualEA name fa)
        filename (new java.io.File (str name ".xml"))]
    (. SaveModel saveAutomata model filename)))
  

(defn dfa
  ([filename]
    (println "load from file " filename)
    (dfa-from-file filename))  
  ([Q A delta start acceptable]
    (let [dea (new Dea)]
      (doseq [s Q] (add-state dea s))
      (doseq [c A] (add-char dea c))
      (doseq [d delta]
        (try
          (add-transition dea (nth d 0) (nth d 1) (nth d 2))
          (catch java.lang.IllegalArgumentException e                      
            (println dea (nth d 0) (nth d 1) (nth d 2))
            (println (states dea)))))
      (let [oldstart (start-state dea)]
        (start-state! dea start)
        (.removeState dea oldstart))
      (doseq [f acceptable] (.addAcceptingState dea (state f)))
      dea)))

(defn read-from-file-safely [filename]
  (with-open [r (java.io.PushbackReader.
                 (clojure.java.io/reader filename))]
    (binding [*read-eval* false]
      (loop [cnt 0]
        (let [raw-dfa (read r)]
          (let [d (dfa-minimization (apply dfa raw-dfa))]
            (save-fa d (str "dfa_" cnt))))          
        (recur (+ 1 cnt))))))

(defn rewrite-to-python [filename]
  (with-open [r (java.io.PushbackReader.
                 (clojure.java.io/reader filename))]
    (binding [*read-eval* false]
      (loop [cnt 0]
        (let [raw-dfa (read r)]
          (let [d (dfa-minimization (apply dfa raw-dfa))]
            (spit d (str "dfa_" cnt))))        
        (recur (+ 1 cnt))))))



;;(def pg (dfa '(p q) '(\a \b) '( (p \a p) (q \a q) (p \b q) (q \b p) ) 'p '(q)))

(defn enumerate 
  ([s]   (enumerate s 0))
  ([s n] 
    (if (not (empty? s))
      (cons (list (first s) n)
            (enumerate (rest s) (+ 1 n)))
      nil)))
  

(defn dfa-concat-n [& rest]  
  (let [automaton (map dfa->nfa rest)
        alg (new NeaConcatenation)]
    (nfa->dfa (reduce (fn [x y]              
                        (.setParameter alg x 0)
                        (.setParameter alg y 1)              
                        (.run alg)  
                        (first (.getResult alg)))
                      automaton))))
    
    
    
    
;==============================================================================
;=== Hierachies
;===
;==============================================================================

(defn gensyms [amount]
  (map (fn [x] (gensym)) (range amount)))

(defn boolean-closure [languages]
  (let [ l (concat
             languages
             (map dfa-complement languages)) ]
    (concat l
            (map (fn [t] 
                   (dfa-intersection (first t) (second t)))                                    
                 (trapclj.combinatorics/combinations l 2))
            (map (fn [t] 
                   (dfa-union (first t) (second t)))
                 (trapclj.combinatorics/combinations l 2)))))


(defn concat-closure-length [languages amount]  
  (flatten 
    (map (fn [x] (apply dfa-concat-n x)) 
         (trapclj.combinatorics/combinations languages amount))))
  
(defn concat-closure-until-length [languages amount]
  (concat languages (mapcat (fn [i] (concat-closure-length languages i))
                            (range 2 amount))))

(defn co-language-class [languages] 
  (map dfa-complement languages))

(def S "(a+b+c)")
(def sth-base (map dfa-minimization 
		   (map dfa-from-regex
			(list (str S \a S \b S \c S)
			      ;; (str S \b S \a S \c S)
			      (str S \c S \a S \b S)
			      ;; (str S \b S \c S \a S)
			      (str S \c S \b S \a S)
			      (str S \a S \c S \b S)))))
     
(def ddh-base (map dfa-minimization 
		   (map dfa-from-regex 
			(list 
			 (str \a \a S \b S \c)
			 (str \b \a S \b S \c)
			 (str \c \a S \b S \c)
			 (str \a \b S \b S \c)
			 (str \a \c S \b S \c)
			 (str \b \b S \b S \c)
			 (str \c \c S \b S \c)
			 (str \b \c S \b S \c)
			 (str \c \b S \a S \b)
			 (str \a \b S \c S \b)
			 (str \a \c S \a S \c)
			 (str \a \c S \c S \c)))))
     
(defn level1 [lc]
  (boolean-closure lc))

(defn level32 [lc]
  (concat-closure-until-length (level1 lc) 2))

(defn level2 [lc]
 (boolean-closure (level32 lc)))

(defn level52 [lc]
  (concat-closure-until-length (level2 lc) 2))
 


