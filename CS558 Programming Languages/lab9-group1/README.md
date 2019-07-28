### Synopsis

CS 558 Fall 2017, week 9 lab submission.

### Authors

- zhan li
- Haomin He
- Yuxiang Jiang

### Running

`cd` into the directory that contains this file (`README.md`), then run
`stack test` to run the test cases.
If `stack` says something about missing GHC, run `stack setup` first before
`stack test`.

### Implementation Details

The solution is implemented in Haskell and has been tested on GHC 7.10.3
on the CAT Linux machines.

The `Dict` ADT is implemented in Haskell typeclass. For mutability we use
`IORef` and `IOArray`.
