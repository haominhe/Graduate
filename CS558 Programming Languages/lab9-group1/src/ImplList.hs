{-# LANGUAGE TupleSections #-}
{-# LANGUAGE FlexibleInstances #-}

module ImplList (
  IOPropList,
) where

import Data.IORef

import Dict

newtype IOPropList k v = IOPropList { unIOPropList :: IORef [(k, v)] }
  
-- No way to shortcut..
lookupOrInsert k v = orInsert . foldr comb (False, [])
 where
  comb x@(k', _) (found, xs)
    | k' == k = (True, (k, v):xs)
    | otherwise = (found, x:xs)
  orInsert (found, xs) = if found then xs else (k, v):xs

instance Dict (IOPropList String) where
  empty = IOPropList <$> newIORef []
  lookup (IOPropList r) k = Prelude.lookup k <$> readIORef r
  insert (IOPropList r) k v = atomicModifyIORef' r $ (,()) . lookupOrInsert k v
  fold (IOPropList r) z f = foldr (\(k, v) z -> f z k v) z <$> readIORef r
