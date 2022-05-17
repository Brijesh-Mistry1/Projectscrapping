$('form[id="form2"] button').click(function(){
    $('body').append('<div style="" id="loadingDiv"><div class="loader">Loading...</div></div>');
    setTimeout(function() {
        $('#loadingDiv').remove();
    }, 2000);
});