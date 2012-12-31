
(ns trapclj.core)

(defn quintpl [a]
  (list 
   (map str (states a))
   (map (fn [x] (first (str x))) (sigma a))
   (map (fn [x] 
	    (list (str (first x))
		  (first (str (second x)))
		  (str (nth x 2))))
	(transitions a))
   (str (start-state a))
   (map str (acceptable-states a))))


(defn python-construct [a]
  (with-out-str
    (print "[ {")
    (doseq [s (states a)]
      (print (str "'"  s "',")))
    (print "},\n {")
    (doseq [c (sigma a)]
      (print (str "'" c "',")))
    (print "},\n {")
    (doseq [[a c b]  (transitions a)]
      (print (str "('" a  "','" c "'): '" b "',")))
    (print "},")
    (print  (str "'"  (start-state a) "', {"))
    (doseq [f (acceptable-states a)]
      (print (str "'" f "',")))
    (println "}]")))
      

(use 'clojure.java.io)   
(defn save-dfa-list [l name]  
  (spit name "")
  (doseq [a l]	 
	 (spit name (quintpl a) :append true)))
