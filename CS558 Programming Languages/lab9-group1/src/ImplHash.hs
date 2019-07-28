{-# LANGUAGE PatternSynonyms #-}
{-# LANGUAGE FlexibleContexts #-}
{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE ViewPatterns #-}
{-# LANGUAGE LambdaCase #-}

module ImplHash (
  IOHashDict,
) where

import Data.IORef
import qualified Data.Array.IO as A
import Data.Maybe (catMaybes)

import Dict

pattern BUCKETS = 1000

data IOHashDict k a = IOHashDict {
  dEntries :: A.IOArray Int (Maybe (k, a))
}

simpleHash = sum . map fromEnum

data Lookup a
  -- | Found at index with value
  = Found Int a
  -- | Not found with last empty slot (or nothing if the table is full)
  | NotFound (Maybe Int)

lookupEntry arr k hash probe
  | probe >= BUCKETS = pure (NotFound Nothing)
  | otherwise = do
    let ix = (hash + probe) `mod` BUCKETS
    e <- A.readArray arr ix
    case e of
      Nothing -> pure (NotFound (Just ix))
      Just (k', v) -> if k == k'
        then pure (Found ix v)
        else lookupEntry arr k hash (probe + 1)

instance Dict (IOHashDict String) where
  empty = IOHashDict <$> A.newArray (0, BUCKETS) Nothing
  lookup (dEntries -> arr) k@(simpleHash -> hash) = do
    e <- lookupEntry arr k hash 0
    pure $ case e of
      Found _ v -> Just v
      NotFound _ -> Nothing
      
  insert (dEntries -> arr) k@(simpleHash -> hash) v = do
    ix <- e2Ix <$> lookupEntry arr k hash 0
    A.writeArray arr ix (Just (k, v))
   where
    e2Ix = \case
      Found ix _ -> ix
      NotFound (Just ix) -> ix
      NotFound Nothing -> error "insert: full"
  fold (dEntries -> arr) z f = fold' <$> A.getElems arr
   where
    fold' = foldr (\(k, v) z -> f z k v) z . catMaybes

