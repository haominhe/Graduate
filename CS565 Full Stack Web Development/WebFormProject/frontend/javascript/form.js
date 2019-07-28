// create init

function initial() {
    $('#add_guest').click(function () {
        add_person();
    });
    $('#submit_form').click(function () {
        send_form();
    });
}

function add_person() {
    var form = `
    <li>
    <form  style="background-color: rgba(255, 255, 255, 0.5); padding: 10px; border-radius: 5px; margin-bottom: 10px;">
    <div class="form-group">
        <label for="name">FIRST NAME & LAST NAME</label>
        <i style="margin-left:270px" class="fa fa-window-close remove_guest"></i>
        <input class="form-control" id="name" placeholder="ENTER FIRST NAME & LAST NAME">
    </div>
    <div class="form-check">
        <input type="checkbox" class="form-check-input" id="vegetarian">
        <label class="form-check-label" for="vegetarian">VEGETARIAN</label>
    </div>
    <div class="form-check">
        <input type="checkbox" class="form-check-input" id="kid">
        <label class="form-check-label" for="kid">SIT AT KIDS TABLE</label>
    </div>
</form>
</li>
    `

    $('#outer_form_group').append($(form));

    $('.remove_guest').click(function () {
        remove_guest(this);
    });
}

function remove_guest(element) {
    $(element).parent().parent().parent().remove();
}

function send_form() {
    var forms = $('form');

    var inputs =  get_input(forms[0]);
    // use email as the primary key
    var email = inputs.email;
    delete inputs.email;
    var data =  {
        [email]: inputs
    };


    data[email].familyMembers = [];

    Object.keys(forms).forEach(function (key) {
        if(key !='0' && key!= 'length' && key !='prevObject') {
            data[email].familyMembers.push(get_input(forms[key]));
        }
    });

    send_request(data);
}

function get_input(form) {
    var inputs = {};
    inputs.name = $(form).find('input[id="name"]').val();
    inputs.email = $(form).find('input[id="email"]').val();
    inputs.vegetarian = $(form).find('input[id="vegetarian"]').is(":checked");
    inputs.kid = $(form).find('input[id="kid"]').is(":checked");
    return inputs;
}

function send_request(formdata) {
    $.ajax({
        type: "POST",
        url: "http://localhost:8080/register",
        data: JSON.stringify(formdata),
        contentType: "application/json; charset=utf-8",
        success: function () {
            console.log("success");
            window.location.replace("./confirmation.html");
        }
    })
}
initial();