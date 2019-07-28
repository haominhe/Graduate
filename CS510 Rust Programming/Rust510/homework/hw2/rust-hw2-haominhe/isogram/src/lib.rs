//An isogram (also known as a "nonpattern word") is a word or phrase without a repeating letter, however spaces 
//and hyphens are allowed to appear multiple times.



pub fn check(candidate: &str) -> bool {
    let lowcase = candidate.to_lowercase();
    let mut output: Vec<char> = vec![];
    for eachchar in lowcase.chars(){
        if eachchar.is_alphabetic() {
            output.push(eachchar)
        }
    }
    output.sort();
    let originallen = output.len();
    let mut temp = output.clone();
    temp.dedup();
    let templen = temp.len();
    //println!("{:?}               {:?}    {:?}", output, temp, originallen);
    return originallen == templen
}