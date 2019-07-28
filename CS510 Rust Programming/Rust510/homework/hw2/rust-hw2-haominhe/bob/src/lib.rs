// Bob is a lackadaisical teenager. In conversation, his responses are very limited.

// Bob answers 'Sure.' if you ask him a question.

// He answers 'Whoa, chill out!' if you yell at him.

// He answers 'Calm down, I know what I'm doing!' if you yell a question at him.

// He says 'Fine. Be that way!' if you address him without actually saying anything.

// He answers 'Whatever.' to anything else.

#![allow(unused)]
pub fn reply(message: &str) -> &str {
    let messageresult:&str = message.trim();
    let yell:bool = messageresult.chars().any(char::is_alphabetic) && messageresult.chars().all(|c| c.is_uppercase() || !c.is_alphabetic());
    if messageresult.is_empty(){
        return "Fine. Be that way!"
    } else if messageresult.ends_with("?") && messageresult == messageresult.to_uppercase() && yell{
        return "Calm down, I know what I'm doing!"
    } else if messageresult.ends_with("?"){
        return "Sure."
    } else if messageresult == messageresult.to_uppercase() && yell{
        return "Whoa, chill out!"
    } else{
        return "Whatever."
    }  
}
