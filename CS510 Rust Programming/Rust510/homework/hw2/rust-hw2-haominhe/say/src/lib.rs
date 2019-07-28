// Given a number from 0 to 999,999,999,999, spell out that number in English.
// 14 becomes "fourteen".
// 100 becomes "one hundred".
// 120 becomes "one hundred and twenty".
// 1002 becomes "one thousand and two".
// 1323 becomes "one thousand three hundred and twenty-three".

/* The first string is not used, it is to make array indexing simple */
static single_digits: [&'static str; 100] = ["", "one", "two", "three", "four",
                              "five", "six", "seven", "eight", "nine", "ten", "eleven", 
                              "twelve", "thirteen", "fourteen", "fifteen", "sixteen", 
                              "seventeen", "eighteen", "nineteen", 
                              "", "", "", "", "", "", "", "", "", "", 
                              "", "", "", "", "", "", "", "", "", "", 
                              "", "", "", "", "", "", "", "", "", "", 
                              "", "", "", "", "", "", "", "", "", "",
                              "", "", "", "", "", "", "", "", "", "",
                              "", "", "", "", "", "", "", "", "", "",
                              "", "", "", "", "", "", "", "", "", "",
                              "", "", "", "", "", "", "", "", "", "",
                              ];
 
/* The first two string are not used, they are to make array indexing simple*/
static tens_multiple: [&'static str; 10] = ["", "", "twenty", "thirty", "forty", "fifty",
                             "sixty", "seventy", "eighty", "ninety"];
 
static tens_power: [&'static str; 7] = ["", " thousand", " million", " billion", " trillion",
    " quadrillion", " quintillion",];

pub fn encode(n: u64) -> String {
    if n == 0 {
        return "zero".to_string();
    }
    if n == 100 {
        return "one hundred".to_string();
    }
    let mut output: Vec<String> = vec![];
    for (cal, cal2) in tens_power.iter().enumerate() {
        let out2 = calculate((n / 10u64.pow((cal as u32)*3)) % 1000);
        if out2 != "" { 
            output.insert(0, format!("{}{}", out2, cal2)) 
            }
    }
    output.join(" ")
}

fn calculate(n: u64) -> String {
    let mut outputstring = String::new();
    let hundred = single_digits[(n/100) as usize].to_string();
    // println!("{:?}          {:?}      {:?} ", n, (n/100) as usize, hundred);
    let tensingle = single_digits[(n%100) as usize].to_string();
        //println!("{:?}          {:?}      {:?} ", n, (n%100) as usize, tensingle);

    if hundred != "" { 
        outputstring = format!("{}{} hundred ", outputstring, hundred) 
        }
    if tensingle != "" { 
        return format!("{}{}", outputstring, tensingle) 
        }

    let temp1 = ((n%100)/10)%10;
    let ten = tens_multiple[(temp1) as usize].to_string();
    //println!("{:?}          {:?}      {:?} ", n, (temp1) as usize, ten);
    let one = single_digits[(n%10) as usize].to_string();


    if ten != "" && one != ""{
        outputstring = format!("{}{}-{}", outputstring, ten, one)
    } else if ten != "" {
        outputstring = format!("{}{}", outputstring, ten)
    } else{
        outputstring = format!("{}{}", outputstring, one)
    }
    outputstring
}