-- TYPES IN HASKELL: An Introduction
-- Haomin He

-- References: 
-- https://stackoverflow.com
-- https://github.com/zirrostig
-- This is an executable Haskell script, suitable
-- for loading into a Haskell interpreter

-- This is a one-line comment, because it follows dash-dash

{- This is also a comment, because 
   it is enclosed by curly-dash and dash-curly 
   {- incidentally, these nest -} -}

{- To work with this file, you will need the Glasgow Haskell 
   interpreter (ghci). This is installed on the 
   linux lab machines. To download to your own machine, visit
   www.haskell.org/ghc.

   Run the interpreter in a separate window.
   (Try to keep an editor window for this file and the
   interpreter window on your screen at the same time.)
   For example:

   $ ghci 
   GHCi, version 7.10.3: http://www.haskell.org/ghc/  :? for help
   Prelude> 
   
   Then load the script using the ":l" command:

   Prelude> :l TypesInHaskell.hs
   [1 of 1] Compiling Main             ( TypesInHaskell.hs, interpreted )
   Ok, modules loaded: Main.
   *Main> 

   You can then explore the definitions in the script by
   typing expressions at the prompt.

   If you want to change a definition, you need to edit the
   script file, and then use the ":r" command to reload it:

   *Main> :r
   [1 of 1] Compiling Main             ( Types.hs, interpreted )
   Ok, modules loaded: Main.
   *Main> 

   To exit from the interpreter, use the ":q" command:

   *Main> :q
   Leaving GHCi.

   WARNING: All functions and constants defined at top-level of
   a Haskell script are (potentially) _mutually recursive_; i.e.,
   they can refer to each other no matter what order they appear
   in the file.  Also, no name can be defined twice in the same
   file.  This means you have to be careful when making additions
   to this file: don't accidentally re-use a name already defined
   above or below where you're editing!

-}   
-----------------------------------------------------------------------------
{-  INTRODUCTION
    Haskell is a _functional_ language, where the word 
    "functional" has at least two meanings:
    
    - The language is designed to make it convenient 
      to define and manipulate functions (we sometimes 
      say functions are "first class values").

    - The language is (almost) free of side-effects, so 
      computations can be structured as applications of
      functions to arguments, just as in mathematics.

    Haskell is one of several full-featured functional 
    languages.  Other languages with a strong functional
    flavor include Lisp, Scheme, ML, Scala, F#, Clojure, etc. 
    
    Our main interest is in Haskell's _type system_, which 
    has a particularly clean design, which is largely
    independent of the language's functional character.
    Haskell is statically typed, which distinguishes it
    from Lisp, Scheme, and other dynamically typed languages.

    Much of Haskell's type system is shared by the ML language
    and its descendents, although Haskell offers some
    features that ML lacks.

    A distinctive characteristic of Haskell is that it uses
    _lazy evaluation_ (expressions are not computed unless 
    and until their values are needed). But we won't be relying 
    on this feature.

    Indeed, there are many aspects of Haskell that are not
    covered in this file: our attention is very much just on types.

    If you are intrigued by what you see here, you may want to know
    that PSU offers a course specifically on functional programming
    (using Haskell).
-}
    
-----------------------------------------------------------------------------
{- PRIMITIVE ATOMIC TYPES

   Some primitive atomic types:

   Char
   Int       -- fit in a machine-word
   Integer   -- unbounded
   Float
   Double
   
   Some important non-primitive types that are defined in the
   standard library (called the Prelude):

   Bool	
   String    -- special parsing support for literals
   [t]       -- lists with elements of type t; more special parsing
   
   We will see later how these types are defined.

   All of these types are _immutable_: once a value has been
   constructed, its contents never change.
-}
-----------------------------------------------------------------------------
{- CONSTANTS

Some simple constants (must start with a lower-case letter) -}

x :: Int
x = 32768

normal :: Float
normal = 98.6

y :: Char
y = 'B'

w5 :: String
w5 = "Hello"

ns :: [Int]
ns = [1,2,3] -- a list

ms :: [Int]
ms = []      -- an empty list

{- After loading this file, 
   try typing these at top level in the interpreter: 

x                              -- evaluates a variable
x + 1                          -- or an arbitrary expression
21 * 2
:t x                           -- :t displays the type of a variable
:t x + 1                       -- or an arbitrary expression
(normal * 3 + 1) / (2 - normal)  -- we have usual arithmetic operators
(x + 1) `div` 2                -- `div` is integer division operator
10 `div` 0                     -- generates checked runtime error
if y == 'B' then 10 else 42    -- if-then-else is an expression form
let y = 100 in y + 1           -- let is a binding expression form
w5 ++ w5                       -- concatenation
head ns                        -- returns first element of a list
tail ns                        -- returns all but first element of a list
head ms                        -- generates checked runtime error
['b',True]                     -- static error: all list elements must 
                               --     have the same type
-}

-----------------------------------------------------------------------------
{-  FUNCTIONS

   Functions are also a primitive type in Haskell.

   A function that expects an argument of type t1
   and returns a result of type t2 is described by the 
   _arrow_ type  t1 -> t2 

   Simple function definitions (names must also begin with 
   a lower-case letter).  
   Notice the lack of parentheses around parameters. 
-}

faren :: Float -> Float
faren c = 32.0 + c * (9/5)

cap :: Char -> Bool
cap c = c >= 'A' && c <= 'Z'  -- usual ordering

bookend :: String -> String -> String    -- function w/ two parameters
bookend a b = a ++ b ++ a          

inc :: Int -> Int
inc = \x -> x + 1  -- RHS is lambda expression defining anonymous function

{- Try evaluating these expressions at top level: 

faren (100)            -- parentheses are ok
faren 100              -- but not needed (so best omitted!)
faren (50 + 50)        -- unless for grouping
faren 50 + 50          -- function application binds tighter than + 
cap 'y'            
cap y                  -- top-level values are available
cap y y                -- static error: too many arguments
bookend "hello" "goodbye"  -- multiple arguments are space-separated
bookend "hello" 'a'    -- static error: wrong argument types
bookend "hello"        -- static error: not enough arguments =>
                       --   a mysterious error message (don't worry for now)
:t bookend             -- functions have types just like everything else
(+) 2 3                -- operators are just functions in infix position
div 3 2                -- `foo` is just the infix version of foo
-}

{- EXERCISE:
  
   Write and test a function
   
   secondi :: [Int] -> Int

   that returns the second element of its (integer list) argument.

   The best way to do this is to edit this file, adding the function
   right below this comment.  Then use the :r command to reload
   this file into the interpreter.  If your definition generates
   static errors, edit it and try :r again.

   Once your definition has been accepted by the interpreter, 
   you can test it by typing an expression at top level, as usual.

-}

secondi :: [Int] -> Int
secondi ns  = head(tail(ns))

-----------------------------------------------------------------------------
{- TYPE CONSTRUCTORS: TUPLES

   The simplest constructor builds tuples.

   A tuple type is simply a cartesian product of arbitrary types.
   The same syntax is used for both type construction and 
   value construction.                                            -}

p :: (Int,Bool)
p = (42,True)

q :: (String,Int,[Float])
q = ("Hello",99,[2.81828,3.141592])

r :: (Float -> Float, Float)
r = (faren,-273.0)

{- The elements of tuples are extracted by _pattern matching_.
   A pair pattern looks like
     (x,y) 
   where x and y are new variable names that are to be bound
   to the first and second elements of the pair, respectively.
 -}

s :: (Bool,Int) 
s = let (p1,p2) = p in         -- pattern match in let binding
    (not p2, p1 + 5)

swapib :: (Int,Bool) -> (Bool,Int)
swapib (x,y) = (y,x)           -- pattern match in function definition

{- Try evaluating these expressions at top level:

s
swapib p
swapib q                -- static error: wrong tuple size
swapib r                -- static error: wrong tuple types
let (f,x) = r in f x 
(1+2,3+4) == (3,7)      -- equality on tuples is structural
(77,78,79) < (77,78,78) -- order is lexicographic                -}

{- EXERCISE

Write and test a function 

first'n'third :: [Int] -> (Int,Int)

that returns a pair containing 
the first and third elements of its (list) argument.  -}

first'n'third :: [Int] -> (Int,Int)
first'n'third ns = ((head ns), (secondi(tail ns)))

-----------------------------------------------------------------------------
{- POLYMORPHISM

Often, functions that manipulate constructed types (such as
tuples) don't really care what base types the constructor
is applied to. For example, the following function to
swap (Float,Int) pairs: -}

swapfi :: (Float,Int) -> (Int,Float)
swapfi (x,y) = (y,x)

{- looks exactly like the swapib function, except
for the type declaration. Writing separate versions of
such functions for every instance of pairs we might
want would be verbose and painful! (This is a complaint
that lovers of dynamic typing frequently make about 
statically typed languages.)

In Haskell, we can instead write a function like swap 
just _once_ and give it a _polymorphic_ type that 
allows it be applied to all kinds of pairs.  ("Polymorphic"
means "having many forms.") 

A polymorphic type is written using _type variables_,
which are (lower-case) identifiers that can be _instantiated_
to any type, as long as this is done consistently.

For example, we can define: -}

swap :: (t,u) -> (u,t)
swap (x,y) = (y,x)

{- and then simply write

swap p                     -- t = Int, u = Bool
swap r                     -- t = Float -> Float, u = Float
swap ("Hello","Goodbye")   -- t = String, u = String

etc. 

Much of the Haskell Prelude consists of polymorphic
functions like this.  For example, most functions
on lists (like head, tail, etc.) are polymorphic in the type
of list elements. For example:

head :: [a] -> a
tail :: [a] -> [a]

This form of polymorphism, where the definition of the function
is uniform for all types, is sometimes called "parametric
polymorphism." It also goes under the name "generics" in 
Java and C# and (basic) "templates" in C++.

EXERCISES:

(a) Write and test a polymorphic version of the 'secondi' function. 
    Call the function `second`. 


(b) Write and test a function 

    heads :: [a] -> [b] -> (a,b)

    that returns a pair containing the head of each list argument

(c) Write and test a function 

    foo :: a -> (a,a)

    How much choice do you have about what 'foo' does?

-}

second :: [t] -> t
second ns  = head(tail(ns))

heads :: [a] -> [b] -> (a,b)
heads ns ms = (head(ns), head(ms))

foo :: a -> (a,a)
foo temp = (temp, temp) 


{- OVERLOADING AND TYPE CLASSES

   There is another useful form of polymorphism, sometimes called
   "ad hoc" polymorphism or "overloading," in which the behavior
   of the function _differs_ depending on the type being operated
   on. For example, it is very useful to be able to use an
   equality operator (==) on many different types, but the actual
   implementation of that operator needs to be type-dependent
   and in some cases (e.g. for function types), it shouldn't be
   defined at all. 

   Haskell supports this kind of overloading using a mechanism
   called _type classes_.  Each class specifies a set of operations
   that should be supported by types that are members of the class;
   when we declare a type to be an _instance_ of a class,  we must 
   give an implementation of the class operations.  Class membership
   becomes a _constraint_ on the type of functions that use those
   operations.  For example, the == operator is part of the Eq class,
   so when we use == in a function, we must make sure that the
   type of its operands is an instance of Eq. 
   
   For example:                                                        -}

eqpair :: Eq a => (a,a) -> Bool
eqpair (a,b) = a == b

{- Try typing the following:

eqpair (normal,normal)  -- ok: the type of normal (Float) is an Eq instance
eqpair (True,True)      -- ok: the type of True (Bool) is an Eq instance
eqpair (second,second)  -- static error: the type of second ([a] -> a) 
                                         is not an Eq instance
                                    
  Another useful built-in typeclass is Show, which specifies an
  operation for displaying values as text (this is used implicitly
  by the interpreter to display the results of top-level expressions).

  It is also possible define new instances and new classes, 
  but we won't see those details in this file. 
-}

-----------------------------------------------------------------------------
{- TYPE DECLARATIONS

   New names for old types.

   It is often convenient to give a new name to a constructed
   type by using a _type declaration_.
   
   Note that these names are just abbreviations for existing
   types, not fundamentally new and different types.  Basically,
   the abbreviations just get expanded out before type-checking.
   (Hence, these declarations cannot be recursive.)

   Type declarations can also be parameterized by type variables.

   Note that type names must begin with an upper-case letter.
-}

type MyPair = (Int,Bool)
type YourPair = (Bool,Int)
type OurSwap = MyPair -> YourPair
    
p' :: MyPair
p' = (10,True)

swapib' :: OurSwap
swapib' (x,y) = (y,x)

type PairIntWith a = (Int,a)
type Swap a b = (a,b) -> (b,a)

p'' :: PairIntWith Bool
p'' = (10,True)

p1 :: PairIntWith Float
p1 = (10,3.14) 

swapib'' :: Swap Int Bool
swapib'' (x,y) = (y,x)

{- Try evaluating these expressions:

swapib' p'
swapib p'
swapib' p
swapib' p''
swapib'' p
p == p'
p == p''
p'' == p1     -- static type error
-}

{- The built-in String type is actually defined (in the Prelude) as 

   type String = [Char] 

   EXERCISE: write and test a function 

   secondstr :: String -> Char 

   that returns the second character of a String.                
-}
   
type Stringthis = [Char] 
secondstr :: Stringthis -> Char 
secondstr ns = head(tail(ns))

-----------------------------------------------------------------------------
{- ALGEBRAIC DATA TYPES

   The key mechanism for building genuinely new types in Haskell
   is the _algebraic data type_ definition.

   Algebraic data types combine:

   - disjoint unions 
   - cartesian products 
   - recursion

   into a single unified mechanism for declaring types,
   constructing values, and deconstructing them again.

   As a characteristic example, consider the type of binary
   trees, with integers at the internal nodes.
   In Haskell, we can write:       -}

data ITree = ILeaf
           | INode Int ITree ITree   
     deriving (Eq, Show)

{- This definition does two things:

   - It defines ITree to be a completely new type.

   - It defines two _constructors_ for this type, ILeaf and INode,
     which can be used to create values _and_ to pattern match 
     on values in order to deconstruct them.
   
   (The "deriving" clause makes ITree an instance of the 
    Eq and Show type classes.)

   The list of types after each constructor name specifies
   the number and types of data fields stored in a value 
   created with this constructor.  So Leaf has no fields and
   and Node has three fields (one Int and two ITree's).
   Notice that the Node constructor is _recursive_, since it
   has fields of the same type we're defining!

   When used to create values, Leaf and Node behave just like
   functions.  You can ask the top level for their types:

   :t Leaf
   :t Node

   They behave essentially like case constructors in Scala. They 
   are also very much like constructors in Java or other OO languages, 
   except that they do not execute arbitrary code: they _just_ construct 
   a value from its constituent fields. For example, we can create 
   the small tree

                 2
                / \
               /   \
              1     7
             / \   / \
            /   \ -   -
           4     5
          / \   / \
         -   - -   -              
   thus:
-}

t1 :: ITree
t1 = INode 2 (INode 1 (INode 4 ILeaf ILeaf)
                      (INode 5 ILeaf ILeaf))
             (INode 7 ILeaf ILeaf)                              

{- To inspect an ITree value, we use the same constructor names
   in a multi-way _pattern match_, which can be specified 
   using a _case_ expression. -}

sumITree :: ITree -> Int
sumITree t =
  case t of                   
    ILeaf -> 0
    INode n left right -> n + sumITree left + sumITree right

{- The case expression works by comparing its argument against 
   each pattern in turn, looking for the first one that matches,
   and then evaluating the corresponding expression after the -> 

   Each case arm has the form
   
    C x1 ... xn -> e
   
   where:

     C is a constructor name
     x1,...,xn are fresh variable names to be bound within e to the 
               fields of the constructed value 
     e is an expression giving the value to return if this arm matches.

   WARNING: Haskell syntax is indentation-sensitive, so it is important
   that the two arms of the case start in the same column.

   EXERCISE: write a function 

   decITree :: ITree -> ITree
   
   that produces a copy of its argument in which each node value
   has been decreased by 1.  
-}

decITree :: ITree -> ITree
decITree t =
  case t of                   
    ILeaf -> ILeaf
    INode n left right -> INode(n-1) (decITree left) (decITree right)

-----------------------------------------------------------------------------
{-  PARAMETERIZED TYPES

   Like type abbreviations, algebraic data type definitions can also 
   be parameterized by type variables.
   
   For example, we can readily generalize our binary trees to 
   hold arbitrary kinds of values, and indeed to hold 
   _different_ kinds of values at the internal nodes vs.
   at the leaves.
-}

data Tree a b = Leaf a 
              | Node b (Tree a b) (Tree a b)
     deriving (Eq, Show)

t2 :: Tree Bool Int
t2 = Node 17 (Node 2 (Leaf True)
                     (Node 7 (Leaf False)
                             (Leaf False)))
             (Leaf True)                              

{- EXERCISE: write and test a function

   sizeTree :: Tree a b -> Int
   
   that counts the total number of nodes in its argument.
   Note that this function doesn't depend on the types of
   data stored in the tree's nodes.                         
-}

sizeTree :: Tree a b -> Int
sizeTree t =
  case t of                   
    Leaf a -> 1
    Node b left right -> 1 + sizeTree left + sizeTree right


{- We could also redefine our previous ITree as an instance
   of this more general tree: -}

type ITree' = Tree () Int

{- Here () denotes the built-in _unit_ type, which contains just
a single value, also written ().  Having a value of this type
gives you essentially no information, since it _must_ be the
one value () ! -}

t1' :: ITree'
t1' = Node 2 (Node 1 (Node 4 (Leaf ()) (Leaf ()))
                     (Node 5 (Leaf ()) (Leaf ())))
             (Node 7 (Leaf ()) (Leaf ()))                              

sumITree' :: ITree' -> Int
sumITree' t =
  case t of                   
    Leaf _ -> 0
    Node n left right -> n + sumITree' left + sumITree' right

-----------------------------------------------------------------------------
{- LISTS

   The built-in list type is actually defined (in the Prelude)
   essentially as follows, except for syntactic differences:

data List a = Nil                  -- like []
            | Cons a (List a)      -- like :
     deriving (Eq, Show)

ns :: List Int
ns = Cons 1 (Cons 2 (Cons 3 Nil))  -- like [1,2,3]

This says that a list is either empty (Nil) or
is built by by prepending a new element to
an existing list (Cons). 

Here "Nil" and "Cons" are conventional names inherited from
the LISP language.  Actual Haskell lists use

[t]   for List t
[]    for Nil
x:xs  for Cons x xs

and provide additional "syntactic sugar" for writing
literal lists, e.g.

[1,2,3] for Cons 1 (Cons 2 (Cons 3 Nil))

Functions over lists are defined by pattern matching
and recursion. Notice that patterns can be nested, 
and _ can be used as a "wild-card" in patterns when we 
don't care about a value.

-}

myhead :: [a] -> a
myhead xs =
  case xs of
    [] -> error "head on empty list"
    x:_ -> x

mytail :: [a] -> [a]
mytail xs =
  case xs of
    [] -> error "tail on empty list"
    _:xs' -> xs'

mysecond :: [a] -> a
mysecond xs =
  case xs of
    _:x:_ -> x
    _ -> error "second on short list" 

mylength :: [a] -> Int
mylength xs = 
  case xs of
    [] -> 0
    _:xs' -> 1 + mylength xs'

{- EXERCISE: Write and test a function:

   myzip :: [a] -> [b] -> [(a,b)]

   that "zips" two lists into a corresponding list of pairs.
   For example:

    myzip [1,2,3] [4,5,6] = [(1,4),(2,5),(3,6)]

   Do something sensible if the two argument lists are
   of different lengths.

   Hint: You can case over a _pair_ of values at once.
-}

myzip :: [a] -> [b] -> [(a,b)]
myzip _ [] = []
myzip [] _ = []
myzip (x:xs) (y:ys) = (x,y):(myzip xs ys)

-----------------------------------------------------------------------------
{- ABSTRACT SYNTAX TREES

   As a more elaborate example, here is the algebraic
   data type encoding of the AST of a small integer expression 
   language.
-}

data Exp = NumE Int
         | VarE String
         | LetE String Exp Exp
         | AddE Exp Exp
         | SubE Exp Exp
         | IfnzE Exp Exp Exp
         | MulE Exp Exp
   deriving (Eq, Show)

e1 :: Exp 
e1 = LetE "y" 
          (SubE (NumE 5) 
                (AddE (NumE 2)
                      (NumE 3)))
          (IfnzE (VarE "y")
                 (NumE 10)
                 (LetE "y" 
                       (NumE 21)
                       (AddE (VarE "y")
                             (VarE "y"))))


{- To write an evaluator, we will need to implement
   environments.  One simple way to represent an
   environment is by a list of (key,value) pairs.
-}   

type Env = [(String,Int)]

extendEnv :: Env -> String -> Int -> Env
extendEnv env k v = (k,v):env

-- if a key isn't found, we just return 0 
lookupEnv :: Env -> String -> Int
lookupEnv env k = 
  case env of
    (k',v'):env' -> if k == k' then v' else lookupEnv env' k
    [] -> 0  

emptyEnv :: Env 
emptyEnv = []

{- With environments in place, the actual evaluation function
   is easily written, with the aid of pattern matching.
   (This should look familiar from Scala.)
-}

eval :: Env -> Exp -> Int
eval env e =
  case e of
    NumE n -> n
    VarE x -> lookupEnv env x
    LetE x e1 e2 -> 
      let v1 = eval env e1 in
      eval (extendEnv env x v1) e2
    AddE e1 e2 -> eval env e1 + eval env e2
    SubE e1 e2 -> eval env e1 - eval env e2
    MulE e1 e2 -> eval env e1 * eval env e2
    IfnzE e1 e2 e3 -> 
      let v1 = eval env e1 in
      if v1 /= 0 then eval env e2 else eval env e3

evalProgram :: Exp -> Int
evalProgram exp = eval emptyEnv exp

{- Try evaluating the test tree.

   Try adding a MulE node (for multiplication) to the 
   Exp data type and the evaluator, and test it.

-}           

{- ==================

   EXERCISE (challenging):

   There are many possible ways to represent environments. 
   Suppose we use a different type to represent environments, namely:

-}

type Env' = String -> Int 

{-
   Write corresponding functions:

   extendEnv' : Env' -> String -> Int -> Env'
   lookupEnv' : Env' -> String -> Int
   emptyEnv'  : Env'

   that behave just like the ones above, except that they work on Env' instead of Env.
   Test your answers.
   
   Syntax hint: you can write a lambda expression like this: \x -> x + 1

-}

extendEnv' :: Env' -> String -> Int -> Env'
extendEnv' env k v = env

--lookupEnv' :: Env' -> String -> Int
--lookupEnv' 

emptyEnv'  :: Env'
emptyEnv' k = 0


-----------------------------------------------------------------------------
{- SPECIAL CASES

   The algebraic data type mechanism is very powerful and general,
   but some its most important uses occur in restricted special cases. 

   Optional values:

   The Prelude defines the following data type, which can be thought of
   turning any type t into an "optional" t --- either there really is
   a value of type t present, or there isn't.   
   
   data Maybe a = Nothing
                | Just a

   Among other things, this type is very useful for signalling
   error conditions in the return value of a function, e.g. for
   this function, which looks for a match in a list of (key,value)
   pairs: -}
  
search :: [(Int,a)] -> Int -> Maybe a
search xys x0 =
  case xys of
    [] -> Nothing
    (x,y):xys' -> if x0 == x then Just y else search xys' x0       

example :: Int -> String
example x = 
  case search [(1,"a"),(2,"b")] x of
    Just y -> "Found: " ++ y
    Nothing -> "Not Found"

  {- Try these out!

     The Nothing value often plays a role analogous to the null 
     object value in Java. The difference is that here we can
     _choose_ on a case-by-case basis whether to wrap Maybe around
     an argument or result type. And if we do use Maybe, we are
     forced to do a pattern match to see if we got a value or not. -}

  {- Enumerations.

     A data type whose constructors carry no values is just like
     an enum type in other languages, e.g.                        -}

data Day = Mon | Tue | Wed | Thu | Fri | Sat | Sun
   deriving (Eq,Show)

weekend :: Day -> Bool
weekend d =  
  case d of
    Sat -> True
    Sun -> True
    _ -> False

{- The built-in Boolean type is just a particularly simple form
   of enumeration: 

   data Bool = False | True

   The if-then-else construct is just special syntax for
   a case over Bool expressions.

-} 
  
{- Simplifying in another direction, an algebraic data type with
   just one constructor is essentially just a record. -}

data Emp = MkEmp String Int  -- employee name, age
   deriving (Eq,Show)

emp :: Emp
emp = MkEmp "Andrew" 99

{- RECORDS.
   
   Haskell provides additional syntax to allow record fields to 
   be named; when used, this feature also automatically 
   defines _selector functions_ for extracting fields by name. 
   For example: -}

data Empr = MkEmpr { name :: String, age :: Int }
   deriving (Eq, Show)

{- This generates exactly the same type and constructor as Emp,
   but allows construction using named fields -}

empr :: Empr
empr = MkEmpr {name = "Andrew", age = 99 }

{- and defines selector functions name and age. 

   Try the following in the interpreter:       
   :t name
   :t age   
   name empr

-}

{- An algebraic data type with just one constructor
   can be useful for imposing distinctions on
   structurally equivalent types.   For example: -}

type Fpair = (Float,Float)

data Polar = P Fpair
     deriving (Eq, Show)
data Rect = R Fpair
     deriving (Eq, Show)

polarMul :: Polar -> Polar -> Polar
polarMul (P(r1,th1)) (P(r2,th2)) = P (r1*r1,th1+th2)

rectAdd :: Rect -> Rect -> Rect
rectAdd (R(x1,y1)) (R(x2,y2)) = R (x1+x2,y1+y2)
 
{- Try out these expressions:

   polarMul (P (150.0,30.0)) (P(10.0,20.0))
   rectAdd  (R (150.0,30.0)) (R(10.0,20.0))
   polarMul (P (150.0,30.0)) (R(10.0,20.0))   -- type error
   [P (10.0,20.0), R (20.0,30.0)]             -- type error

  (Notice that this last error is a little sad: we might
   want to be able to mix both kinds of coordinates in a list,
   but this is disallowed because R and P are constructors of
   _different_ types.)

  EXERCISE. 

  Define single-constructor data types for
  Farenheit and Celsius temperatures, and use them to
  write and test a safe version of a conversion function 
  'ftoc' from F to C. 

-}

type Temper = Float

ftoc :: Temper -> Temper
ftoc = (*(5/9)) . ((+) (-32))


{- Finally, the unit type mentioned before is just an
   algebraic data type with one constructor carrying no values. 
   Again, this type has just one value, its (nullary) constructor. 
-}

data MyUnit = U

{- We can even write an algebraic data type with _no_ constructors
   at all.  This describes a type with no values!
-}

data Void

-----------------------------------------------------------------------------
{- TYPE INFERENCE. 
   
   Haskell has a powerful type inference engine, which can
   figure out the types of most expressions and functions 
   automatically, without the aid of programmer declarations.

   This eases the burden for programmers (and addresses another
   of the complaints that dynamic-typing enthusiasts have about
   statically-typed languages).  It is particularly useful for
   local declarations, such as the 'let' declarations we have
   used a few places in this file, since here the type is often
   obvious from context and therefore especially painful to write
   down.

   On the other hand, we have carefully given an explicit type 
   declaration for every top-level definition in this file.  
   For functions, at least, this is often considered good standard
   practice, because it provides a useful form of documentation,
   and can help programmers be sure that they are defining the
   function they think they are!

   Note that Haskell always infers the _most general_ (i.e.
   most polymorphic) type that is valid for an expression.

   Try this out on a bare definition of our favorite function
   on pairs; see what :t says about its type                    -}        

yetAnotherSwap (x,y) = (y,x)












