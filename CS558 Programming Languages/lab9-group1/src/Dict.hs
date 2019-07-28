{-# LANGUAGE KindSignatures #-}

module Dict where

-- From our research there are at least three ways to do ADTs in Haskell:
-- 1. Typeclasses. This is the mostly widely used one: Monads are implemented
-- in typeclasses for instance.
-- 2. [Backpack](https://ghc.haskell.org/trac/ghc/wiki/Backpack).
-- This is a very new addition to GHC 8.2 that brings mixin-style
-- modules. An example can be found at
-- https://github.com/haskell-backpack/backpack-str. Unfortunately the CAT
-- linux lab only has GHC 7.10.3 and stack currently doesn't support Backpack
-- either.
-- 3. Records. This is just like the C implementation - we store the ADT
-- interface implementation in records and pass them around. It's also the
-- exact way that typeclasses are implemented in GHC.
--
class Dict (d :: * -> *) where
  empty :: IO (d v)
  insert :: d v -> String -> v -> IO ()
  lookup :: d v -> String -> IO (Maybe v)
  fold :: d v -> t -> (t -> String -> v -> t) -> IO t
