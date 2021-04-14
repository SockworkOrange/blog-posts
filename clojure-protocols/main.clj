(defprotocol Dog
  (bark [dog] [dog x] "dog barks")
  (eat [dog] "dog eats"))

(defrecord Pitbull [name]
  Dog
  (bark [dog] (println (str name " goes 'RRRooof! Woof woof!'")))
  (bark [dog x] (repeatedly x #(bark dog)))
  (eat [dog] (println (str name " eats and grunts"))))

;(bark (Pitbull. "Pete"))

(defprotocol Playful
  (play [dog] "plays"))

(extend-type Pitbull
  Playful
  (play [e] (println (str name " is chasing the ball"))))

;(play (Pitbull. "Pete"))

(defprotocol Bird
  (fly [bird] "flying")
  (nest [bird] "nesting"))

(defrecord Dove []
  Bird
  (fly [bird] "flying and bringing peace all around")
  (nest [bird] "nesting with my little baby doves"))

(defrecord Raven []
  Bird
  (fly [bird] "flying in bleak December")
  (nest [bird] "nesting weak and weary"))

(defrecord Birdperson [])

(extend-type Birdperson
  Bird
  (fly [bird] "flying to my wedding with Tammy")
  (nest [bird] "nesting baby humans and birds alike"))

(defprotocol Musician
  (play-music [dog] "playing music"))

(extend-protocol Musician
  Dove
  (play-music [m] "making dove sounds incoherently but peacefully")
  Raven
  (play-music [m] "rapping in bleak December")
  Birdperson
  (play-music [m] "sings an unjustified love song for Tammy"))

;(println (fly (Birdperson.)))
;(println (play-music (Dove.)))
;(println (play-music (Birdperson.)))

(extend-protocol Musician
 java.lang.Object
  (play-music [o] "anyone can make music"))

;; (println (play-music {:x 1}))

(extend-protocol Musician
  clojure.lang.IEditableCollection
   (play-music [o] "music editable")
  clojure.lang.IMapIterable
   (play-music [o] "music iterable"))

;(println (play-music {:a 1}))

(defprotocol Painter
  (paint [this]))

(defrecord Impressionist []
  Painter
  (paint [p] "impressionist painting"))

(defn paint
  [x]
  (if (satisfies? Painter x)
    (paint x)
    "default painting"))

;; (println (paint (Impressionist.)))
;; (println (paint (Dove.)))

(defprotocol Saving
  (get-payload [this] "saving obj"))

(defn save [obj] (get-payload obj))

(defrecord DBObject []
  Saving
   (get-payload [this] "generating a db object"))

(println (save (DBObject.)))