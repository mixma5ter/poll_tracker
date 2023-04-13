$(function() {
    var message = $('.alert');
    if (message.length) {
        setTimeout(function() {
            message.alert('close');
        }, 5000);
    }
});