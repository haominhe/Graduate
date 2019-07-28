{-# LANGUAGE ScopedTypeVariables #-}
{-# LANGUAGE AllowAmbiguousTypes #-}

module Client (
  client
) where

import Control.Monad (forM_)

import qualified Dict as D

type Item = (Int, Bool)

assertM :: String -> IO Bool -> IO ()
assertM msg mb = do
  b <- mb
  if not b
    then fail msg
    else pure ()

mkKey :: Int -> String
mkKey n = replicate n 'a'

mkValue :: Int -> Item
mkValue i = (i, even i)

-- d must be explicitly quantified so that we can refer to it in the
-- function body.
-- The argument `d a` is just used for the concrete type of `d` -
-- its value is simply ignored.
client :: forall d a. D.Dict d => d a -> IO ()
client _ = do
  -- Step 1: create a new empty dict.
  d <- D.empty :: IO (d Item)

  -- Step 2: insert.
  -- Note that enumFromTo is Inclusive on both the start and the end.
  forM_ [1..499] $ \i -> do
    let k = mkKey (2 * i)
        v = mkValue i
    D.insert d k v
    assertM "check insert" $ (Just v ==) <$> D.lookup d k

  -- Step 3: lookup.
  forM_ [1..332] $ \i -> do
    let k = mkKey (3 * i)
    v <- D.lookup d k
    assertM "check lookup" $ pure $
      if even i
        then v == Just (mkValue (floor $ fromIntegral (i * 3) / 2))
        else v == Nothing

  -- Step 4: fold.
  numTrue <- D.fold d 0 (\z _ (_, b) -> z + if b then 1 else 0)
  assertM "check fold" $ pure $ numTrue == 249

