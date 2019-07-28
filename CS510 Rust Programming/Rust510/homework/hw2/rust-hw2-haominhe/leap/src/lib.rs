// on every year that is evenly divisible by 4
//   except every year that is evenly divisible by 100
//     unless the year is also evenly divisible by 400


pub fn is_leap_year(year: i32) -> bool {
    let resultval = true;
    if (year % 4 == 0 && year % 100 != 0 || year % 400 == 0){
        return resultval
    } else { return false; }
        
    // unimplemented!("true if {} is a leap year", year)
}
