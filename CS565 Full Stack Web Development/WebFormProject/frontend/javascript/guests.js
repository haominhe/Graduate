// count how many guests are coming
var total_counter = 0;

function get_guests() {
    $.ajax({
        type: "GET",
        url: "http://localhost:8080/registered",
        success: function (data) {
            display_data(data);
        },
        dataType: 'json'
    })
}

function display_data(data) {
    Object.keys(data).forEach(function (key) {
        var this_email = key;
        var this_guest_name = data[key].name;
        var this_vegetarian = data[key].vegetarian;
        var this_kid = data[key].kid;
        var this_familyMembers = data[key].familyMembers;

        var this_members = [];
        var head = { name: this_guest_name, vegetarian: this_vegetarian, kid: this_kid };
        this_members.push(head);
        var total_members = [];
        total_members = this_members.concat(this_familyMembers);

        display_member(this_email, total_members);
    });

    $('#total').html(`<p style="color:white; font-size:20px;">TOTAL NUMBERS OF GUESTS: ${total_counter}</p>`);
}

function display_member(email, member_list) {
    var each_member_row ='';
    var counter = 0;
    member_list.forEach(function (element) {
        total_counter++;
        counter++;
    });

    member_list.forEach(function (element, index) {
        each_member_row +=
        `
         ${is_head_of_house(email, counter, index)}
         <td>${element.name}</td>
         <td>${element.vegetarian}</td>
         <td>${element.kid}</td>
         </tr>
        `
    });

    $('#guest_table').append($(each_member_row));
}

function is_head_of_house(email, counter, index) {
    return index === 0 ? `<tr><td rowspan="${counter}">${email}</td>` : '<tr>'
}

get_guests();