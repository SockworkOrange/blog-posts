; The Basics
(defmulti make-sound (fn [x] (:type x)))
(defmethod make-sound "Dog" [x] "Woof Woof")
(defmethod make-sound "Cat" [x] "Miauuu")

(make-sound {:type "Dog"})
(make-sound {:type "Cat"})

; Abstracting away Sorting
(def QUICK-SORT-THRESHOLD 5)
(defmulti my-sort (fn [arr]
                    (if (every? integer? arr)
                      :counting-sort
                      (when (< (count arr) QUICK-SORT-THRESHOLD)
                        :quick-sort))))

(defmethod my-sort :counting-sort [arr] "Counting for the win!")
(defmethod my-sort :quick-sort [arr] "Quick Sort it is")
(defmethod my-sort :default [arr] "Good ol' Merge Sort")

(my-sort [1 2 3])
(my-sort [1 2 3 "a"])
(my-sort [1 2 3 4 "a"])

; New and Improved + Operator
(defmulti ++ (fn [x y] [(class x) (class y)]))

(defmethod ++ [Number Number] [x y] (+ x y))

(derive clojure.lang.PersistentVector ::collection)
(derive clojure.lang.PersistentList ::collection)
(derive clojure.lang.PersistentHashSet ::collection)

(defmethod ++ [::collection ::collection] [x y] (concat x y))
(defmethod ++ [::collection java.lang.Object] [x y] (conj x y))
(defmethod ++ [java.lang.Object ::collection] [x y] (++ y x))

(prefer-method ++ [::collection ::collection] [::collection java.lang.Object])
(prefer-method ++ [::collection ::collection] [java.lang.Object ::collection])
(prefer-method ++ [::collection java.lang.Object] [java.lang.Object ::collection])

(defmethod ++ :default [x y] (str x y))

(println (++ 2 3))
(println (++ [1 2] '(3 4)))
(println (++ [1 2] "3"))
(println (++ 1 ["2" "3"]))
(println (++ 3.5 " is a float"))