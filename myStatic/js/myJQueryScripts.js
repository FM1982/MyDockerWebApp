$(function() {
    $.ajax({url: '/retrieve_entries',
            type: 'GET',
            success: function (res){
                console.log(res);
            },
            error: function (error){
                console.log(error);
            }
    });
});