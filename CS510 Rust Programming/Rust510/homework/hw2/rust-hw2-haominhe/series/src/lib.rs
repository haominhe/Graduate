// Given a string of digits, output all the contiguous substrings of length n in that string.

// For example, the string "49142" has the following 3-digit series:

// 491
// 914
// 142



pub fn series(digits: &str, len: usize) -> Vec<String> {
    if len == 0 {
        return vec!["".to_string(); digits.len()+1]
    } else {
        let digits2: Vec<char> = digits.chars().collect();
        let d2 = digits2.windows(len);
        let d3: Vec<String> = d2.map(|cha| cha.iter().collect()).collect();
        return d3
    }
}
