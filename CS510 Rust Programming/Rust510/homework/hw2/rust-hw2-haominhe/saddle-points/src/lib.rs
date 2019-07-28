// It's called a "saddle point" because it is greater than or equal to every element in its row and less than or equal to every element in its column.

// A matrix may have zero or more saddle points.

// Your code should be able to provide the (possibly empty) list of all the saddle points for any given matrix.



pub fn find_saddle_points(input: &[Vec<u64>]) -> Vec<(usize, usize)> {
    let mut output: Vec<(usize, usize)> = Vec::new();
    if input.len() == 0 {
        return output
    } else {
        let row1: Option<&Vec<u64>> = input.iter().next();
        //println!("Hello, world!        {:?}             ", row1);
        let row1len: usize = row1.unwrap().len();
        //greater than or equal to every element in its row
        let mut maxrowelement: Vec<u64> = Vec::new();
        //less than or equal to every element in its column
        let mut mincolelement: Vec<u64> = Vec::new();

        if row1len == 0{
            return output
        }
        for eachrow in input {
            let temp1 = *eachrow.iter().max().unwrap();
            maxrowelement.push(temp1);
        }

        for eachcol in 0..row1len {
            let mut temp2: u64 = 0;
            for eachrow2 in input{
                let temp3: u64 = *eachrow2.iter().skip(eachcol).next().unwrap();
                if temp2 == 0 {
                    temp2 = temp3;
                } else {
                    if temp3 < temp2 {
                        temp2 = temp3;
                    } 
                } //else
            }//for
            mincolelement.push(temp2);
        }//for

        for (colindex, colnum) in mincolelement.iter().enumerate() {
            for (rowindex, rownum) in maxrowelement.iter().enumerate() {
                if colnum == rownum {
                    output.push((rowindex, colindex));
            }
        }
    }
    return output
    } // outer else
}
