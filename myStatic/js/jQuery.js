//<script>
$(function() {

    $('#btnSignUp').click(function() {

        $.ajax({
            url: '/sign_ups',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });

    });

});
//</script>