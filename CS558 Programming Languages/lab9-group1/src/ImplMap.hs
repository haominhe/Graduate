{-# LANGUAGE FlexibleInstances #-}
{-# LANGUAGE TupleSections #-}

module ImplMap (
  IOMap,
) where

import qualified Data.Map as M
import Data.IORef

import Dict

newtype IOMap k v = IOMap { unIOMap :: IORef (M.Map k v) }

instance Dict (IOMap String) where
  empty = IOMap <$> newIORef M.empty
  insert (IOMap r) k v = atomicModifyIORef' r $ (,()) . M.insert k v
  lookup (IOMap r) k = M.lookup k <$> readIORef r
  fold (IOMap r) z f = foldr (\(k,v) z -> f z k v) z . M.toList <$> readIORef r
