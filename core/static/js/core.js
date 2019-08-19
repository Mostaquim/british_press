var item, instance;
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$('.remove-cart').click(function (e) {
    item = $(this).data('item')
    $('#remove-confirm-modal').modal('show')
    instance = $(this).closest('.cart-product')
    console.log(instance)
})

$('#remove-confirm').click(function (e) {
    csrftoken = $(this).data('csrf')
    $.ajax({
        url: '/api/remove_cart/',
        method: 'POST',
        data: { 'item': item },
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (e) {
            console.log(e)
            $(instance).fadeOut()
        }
    })
})

$('#confirm-order-btn').click(function () {
    $('#confirm-order-modal').modal('show')
})

$(document).ajaxStart(function () {
    $('#ajax-loader').fadeIn()
});
$(document).ajaxStop(function () {
    $('#ajax-loader').fadeOut()
})