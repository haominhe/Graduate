//There exists exactly one Pythagorean triplet for which a + b + c = 1000. Find the product a * b * c.
// A Pythagorean triplet is a set of three natural numbers, {a, b, c}, for which,
// a**2 + b**2 = c**2
// 3**2 + 4**2 = 9 + 16 = 25 = 5**2.


pub fn find() -> Option<u32> {
    let mut c;
    let calval:u32 = 1000;
    for a in 1..calval{
        for b in a..calval-a{
            c = calval - (a + b);
            if a * a + b * b == c * c{
                return Some(a * b * c)
            }
        }
    }
    None
    //return Some(31875000)
}
