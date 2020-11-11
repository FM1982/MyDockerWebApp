//<script>
$(function() {
    $.ajax({
            url: '/retrieve_entries',
            type: 'GET',
            success: function (res){

                let br1 = document.createElement('br');
                let br2 = document.createElement('br');
                let br3 = document.createElement('br');
                let br4 = document.createElement('br');
                let br5 = document.createElement('br');
                let br6 = document.createElement('br');
                let br7 = document.createElement('br');
                let br8 = document.createElement('br');
                let br9 = document.createElement('br');

                let div = $('<div>').attr('class', 'list-group').append($('<a>').attr('class', 'list-group-item active')
                    .append($('<p1>').attr('class', 'list-group-item-text').add(br1), $('<p2>').attr('class', 'list-group-item-text').add(br2),
                        $('<p3>').attr('class', 'list-group-item-text').add(br3), $('<p4>').attr('class', 'list-group-item-text').add(br4),
                        $('<p5>').attr('class', 'list-group-item-text').add(br5), $('<p6>').attr('class', 'list-group-item-text').add(br6),
                        $('<p7>').attr('class', 'list-group-item-text').add(br7), $('<p8>').attr('class', 'list-group-item-text').add(br8),
                        $('<p9>').attr('class', 'list-group-item-text').add(br9))); /*$('<div>').attr('class', 'container').append()*/

                let dataObject = JSON.parse(res);

                let entries = '';

                $.each(dataObject, function (index, value){
                    entries = $(div).clone();
                    $(entries).find('p1').text('Vorname: ' + value.Names);
                    $(entries).find('p2').text('Nachname: ' + value.Surname);
                    $(entries).find('p3').text('Alter: ' + value.Age);
                    $(entries).find('p4').text('E-mail: ' + value.EMails);
                    $(entries).find('p5').text('Strasse: ' + value.Street);
                    $(entries).find('p6').text('Hausnummer: ' + value.HouseNo);
                    $(entries).find('p7').text('Postleitzahl: ' + value.PostalCode);
                    $(entries).find('p8').text('Land: ' + value.Country);
                    $(entries).find('p9').text('Telefonnummer: ' + value.PhoneNumber);
                    $('.jumbotron').append(entries);
                });
            },
            error: function (error){
                console.log(error);
            }
    });
});
//</script>