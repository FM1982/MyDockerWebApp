//<script>
/*
    Schau dir dieses Script sehr genau an und durchlaufe es Stück für Stück, weil es nämlich nett aus unserer Situation
    heraus funktioniert. Bitte dabei auch die mydockerflaskapp.py dabei in Betracht ziehen und mit anschauen. Irgendwo ist
    hier der Wurm drin!
 */
$(function() {
    $.ajax({
            url: '/retrieve_entries',
            type: 'GET',
            success: function (res){
                //console.log(res);

                let div = $('<div>').attr('class', 'list-group').append($('<a>').attr('class', 'list-group-item active')
                    .append($('<p1>').attr('class', 'list-group-item-text'), $('<p2>').attr('class', 'list-group-item-text'),
                        $('<p3>').attr('class', 'list-group-item-text'), $('<p4>').attr('class', 'list-group-item-text'),
                        $('<p5>').attr('class', 'list-group-item-text'), $('<p6>').attr('class', 'list-group-item-text'),
                        $('<p7>').attr('class', 'list-group-item-text'), $('<p8>').attr('class', 'list-group-item-text'),
                        $('<p9>').attr('class', 'list-group-item-text'))); /*$('<div>').attr('class', 'container').append()*/
                //console.log(div);
                let dataObject = JSON.parse(res);
                //console.log(dataObject);
                let entries = '';
                //console.log(entries);

                $.each(dataObject, function (index, value){
                    entries = $(div).clone();
                    $(entries).find('p1').text(value.Names);
                    $(entries).find('p2').text(value.Surname);
                    $(entries).find('p3').text(value.Age);
                    $(entries).find('p4').text(value.EMails);
                    $(entries).find('p5').text(value.Street);
                    $(entries).find('p6').text(value.HouseNo);
                    $(entries).find('p7').text(value.PostalCode);
                    $(entries).find('p8').text(value.Country);
                    $(entries).find('p9').text(value.PhoneNumber);
                    /*$(entries).find('p1').text(value.inputNames);
                    $(entries).find('p2').text(value.inputSurname);
                    $(entries).find('p3').text(value.inputAge);
                    $(entries).find('p4').text(value.inputEMails);
                    $(entries).find('p5').text(value.inputStreet);
                    $(entries).find('p6').text(value.inputHouseNo);
                    $(entries).find('p7').text(value.inputPostalCode);
                    $(entries).find('p8').text(value.inputCountry);
                    $(entries).find('p9').text(value.inputPhoneNumber);*/
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