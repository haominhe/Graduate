// The Collatz Conjecture or 3x+1 problem can be summarized as follows:

// Take any positive integer n. If n is even, divide n by 2 to get n / 2. If n is odd, multiply n by 3 and add 1 to get 3n + 1. Repeat the process indefinitely. The conjecture states that no matter which number you start with, you will always reach 1 eventually.

// Given a number n, return the number of steps required to reach 1.




pub fn collatz(n: u64) -> Option<u64> {
    let counter = 0;
    if n == 0 {
        None
    } else {
        helper(n, counter)
    } //else
}

fn helper(n: u64, counter: u64) -> Option<u64> {
    let mut nn = n;
    if nn == 1 {
            Some(counter)
        } else if nn % 2 == 0 {
            nn = nn / 2;
            let counter2 = counter + 1;
            helper(nn, counter2)
        } else if nn % 2 == 1{
            let counter3 = counter + 1;
            helper(nn * 3 + 1, counter3)
        } else {
            None
        }
}


