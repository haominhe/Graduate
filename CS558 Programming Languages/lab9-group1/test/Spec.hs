import Test.Hspec

import Lib

-- NOTE(undefined):
-- The CAT Linux lab only has GHC 7.10.3 installed and the stack version
-- is also too old to support newer GHC versions. With GHC 8+ we can use
-- the TypeApplication language extension to avoid the undefined trick
-- (see https://wiki.haskell.org/Reified_type).
main :: IO ()
main = hspec $
  describe "ADT client" $ do
    it "works with the list implementation" $
      client (undefined :: IOPropList String ())
    it "works with the hashtable implementation" $
      client (undefined :: IOHashDict String ())
    it "works with Data.Map (not required by the lab, just a reference implementation)" $
      client (undefined :: IOMap String ())
