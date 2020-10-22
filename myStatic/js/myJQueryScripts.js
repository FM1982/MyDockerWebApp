//<script>
$(function() {
    $.ajax({url: '/retrieve_entries',
            type: 'GET',
            success: function (res){
                console.log(res);

                var div = $('<div>').attr('class', 'list-group').append($('<a>').attr('class', 'list-group-item active')
                    .append($('<p>').attr('class', 'list-group-item-text'), $('<p>').attr('class', 'list-group-item-text'),
                        $('<p>').attr('class', 'list-group-item-text'), $('<p>').attr('class', 'list-group-item-text'),
                        $('<p>').attr('class', 'list-group-item-text'), $('<p>').attr('class', 'list-group-item-text'),
                        $('<p>').attr('class', 'list-group-item-text'), $('<p>').attr('class', 'list-group-item-text'),
                        $('<p>').attr('class', 'list-group-item-text'))); /**/
                //console.log(div);
                var dataObject = JSON.parse(res);
                //console.log(dataObject);
                var entries = '';

                $.each(dataObject, function (index, value){
                    entries = $(div).clone();
                    $(entries).find('p').text(value.inputNames);
                    $(entries).find('p').text(value.inputSurname);
                    $(entries).find('p').text(value.inputAge);
                    $(entries).find('p').text(value.inputEMails);
                    $(entries).find('p').text(value.inputStreet);
                    $(entries).find('p').text(value.inputHouseNo);
                    $(entries).find('p').text(value.inputPostalCode);
                    $(entries).find('p').text(value.inputCountry);
                    $(entries).find('p').text(value.inputPhoneNumber);
                    //console.log(entries);
                    $('.jumbotron').append(entries);
                });
            },
            error: function (error){
                console.log(error);
            }
    });
});
//</script>