// For want of a horseshoe nail, a kingdom was lost, or so the saying goes.

// Given a list of inputs, generate the relevant proverb. For example, given the list ["nail", "shoe", "horse", "rider", "message", "battle", "kingdom"], you will output the full text of this proverbial rhyme:

// For want of a nail the shoe was lost.
// For want of a shoe the horse was lost.
// For want of a horse the rider was lost.
// For want of a rider the message was lost.
// For want of a message the battle was lost.
// For want of a battle the kingdom was lost.
// And all for the want of a nail.



pub fn build_proverb(list: Vec<&str>) -> String {
    let mut resultv = Vec::new();
    let emptyv = "";
    if list.is_empty(){
        return emptyv.to_string()
    }

    let first = &list[0];
    for counter in 0..list.len()-1{
        resultv.push(format!("For want of a {} the {} was lost.", list[counter], list[counter + 1]))
    }
    resultv.push(format!("And all for the want of a {}.", first));
    resultv.join("\n")
}
