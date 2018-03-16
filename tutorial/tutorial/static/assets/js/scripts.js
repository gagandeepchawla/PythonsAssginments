jQuery(document).ready(function() {
	$('.login-form').on('submit', function(e) {
        //Username validation
        var Username = $('#form-username').val()         
        if( (Username.length < 5) || Username.length > 11 ) {
            alert('Username length must be 5 to 10 char');
            $(this).addClass('input-error');
            e.preventDefault();
        }
        else {
           $(this).removeClass('input-error');
       }
        //password validation
        var Password = $('#form-password').val()         
        if( (Password.length < 5) || Password.length > 11 ) {
            alert('Password length must be 5 to 10 char');
            $(this).addClass('input-error');
            e.preventDefault();
        }
        else {
           $(this).removeClass('input-error');
       }
        //Age Validation
        var Age = $('#form-age').val()
        if($.isNumeric(Age)) {        
            if( (Age < 15) || Age> 101 ) {
                alert('Age  must be 15 to 100 char');
                $(this).addClass('input-error');
                e.preventDefault();
            }
            else {
               $(this).removeClass('input-error');
           }
       }
       else{
        alert('Age Must be a Numeric Value');
        $(this).addClass('input-error');
        e.preventDefault();
    }
});



    // $("#form-username").change(function(){

    // })
    
    
});
