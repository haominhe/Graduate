/* 

CS510 Rust Programming - HW1
Author: Haomin He

References: 
-“Programming Rust by Jim Blandy and Jason Orendorff (O’Reilly).
Copyright 2018 Jim Blandy and Jason Orendorff, 978-1-491-92728-1.”
-https://github.com/ProgrammingRust/examples
-https://stackoverflow.com/questions/147515/least-common-multiple-for-3-or-more-numbers
-https://doc.rust-lang.org/book/second-edition/ch12-01-accepting-command-line-arguments.html
*/


// The sum of the remaining arguments
fn sum(n: u64, m: u64) -> u64 {
    n + m
}

#[test]
fn test_sum(){
    assert_eq!(sum(2,3), 5);
    assert_eq!(sum(1552,36), 1588);
}

// The product of the remaining arguments
fn product(n: u64, m: u64) -> u64 {
    n * m
}

#[test]
fn test_product(){
    assert_eq!(product(7,8), 56);
    assert_eq!(product(16,6), 96);
}

// The Greatest Common Divisor of the remaining arguments
fn gcd(mut n: u64, mut m: u64) -> u64 {
    assert!(n != 0 && m != 0);
    while m != 0 {
        if m < n {
            let t = m;
            m = n;
            n = t;
        }
        m = m % n;
    }
    n
}

#[test]
fn test_gcd() {
    assert_eq!(gcd(14, 15), 1);

    assert_eq!(gcd(2 * 3 * 5 * 11 * 17,
                   3 * 7 * 11 * 13 * 19),
               3 * 11);
}

// The Least Common Multiple of the remaining arguments
fn lcm(n: u64, m:u64) -> u64 {
    n * m / gcd(n, m)
}

#[test]
fn test_lcm(){
    assert_eq!(lcm(56, 42), 168);
    assert_eq!(lcm(77, 12), 924);
}


use std::io::Write;
use std::str::FromStr;
use std::env;

// apply different functions depending on the first argument passed to it.
fn main() {
    let mut numbers = Vec::new();
    let thisargs: Vec<String> = env::args().collect();
    let functionname = &thisargs[1];

    for arg in std::env::args().skip(2) {
        numbers.push(u64::from_str(&arg)
                     .expect("error parsing argument"));
    }

    if numbers.len() == 0 {
        writeln!(std::io::stderr(), "0").unwrap();
        std::process::exit(1);
    }

    //gcd
    if functionname == "gcd" {
        let mut d = numbers[0];
        for m in &numbers[1..] {
            d = gcd(d, *m);
        }

        println!("The greatest common divisor of {:?} is {}",
                numbers, d);
    }


    //sum
    else if functionname == "sum" {
        let mut sss = numbers[0];
        for m in &numbers[1..] {
            sss = sum(sss, *m);
        }

        println!("The sum of {:?} is {}",
                numbers, sss);
    }



    //product
    else if functionname == "product" {
        let mut ppp = numbers[0];
        for m in &numbers[1..]{
            ppp = product(ppp, *m);
        }

        println!("The product of {:?} is {}",
                numbers, ppp);
    }

    //lcm
    else if functionname == "lcm"{
        let mut lll = numbers[0];
        for m in &numbers[1..]{
            lll = lcm(lll, *m);
        }

        println!("The least common multiple of {:?} is {}",
                numbers, lll);
    }

    else {
        println!(0);
    }
}
