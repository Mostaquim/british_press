var selected = {},
    pre_selcted = {
        'product': product_value
    },
    testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;

function start_loader() {
    $('#loader').show()
}

function hide_loader() {
    $('#loader').hide()
}



function get_catalog_data(selected) {
    data = {
        'selected': pre_selcted
    }
    if (selected) {
        data = {
            'selected': selected
        }
    }
    $.ajax({
        method: 'POST',
        url: '/api/catalog/',
        contentType: 'application/json',
        data: JSON.stringify(data),
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            generate_from(data)
            view_price(data.selected)
        }
    })
}

function view_price(data) {
    $('#price-net-p').html('Price Net: ' + data.priceNet)
    $('#price-gross-p').html('Price Gross: ' + data.priceGross)
    $('#shipping-net-p').html('Shipping Net: ' + data.shippingNet)
    $('#shipping-gross-p').html('Shipping Gross: ' + data.shippingGross)
}

$('.catalog-form').on('change', function (e) {
    selected = pre_selcted
    $(this).parent().removeClass('caution')
    $(this).parent().removeClass('error')
    $(this).parent().removeClass('valid')
    $(this).parent().addClass('loading')
    $('.catalog-form').each(function () {
        val = $(this).val()
        name = $(this).attr("name")
        selected[name] = val
    })
    get_catalog_data(selected)
})

function generate_select(e) {
    div = document.createElement('div')
    div.className = 'form-group row'
    label = document.createElement('label')
    l = e.selectDescription.split('_')
    a = []
    l.forEach(function (e) {
        if (e.length > 1) {
            a.push(e.charAt(0).toUpperCase() + e.substring(1));
        }
    })

    label.innerHTML = a.join(' ') + ":"
    $(label).attr('for', e.selectName)
    $(label).addClass('col-sm-2')
    $(div).append(label)
    var second_div = document.createElement('div')
    second_div.className = 'form-with-icon col-sm-10'
    select = document.createElement('select')
    select.className = 'form-control catalog-form'
    select.id = e.selectName
    $(select).attr('name', e.selectName)
    $(select).click(function (e) {
        console.log('asd')
        $(this).removeClass('caution')
    })
    $(select).on('change', function (e) {
        selected = pre_selcted
        $(this).parent().removeClass('caution')
        $(this).parent().removeClass('error')
        $(this).parent().removeClass('valid')
        $(this).parent().addClass('loading')
        $('.catalog-form').each(function () {
            val = $(this).val()
            name = $(this).attr("name")
            selected[name] = val
        })
        get_catalog_data(selected)
    })
    valid = 0
    e.optionList.forEach(function (opt) {
        option = document.createElement('option')
        option.value = opt.optionName
        text = opt.optionTranslations.join(" ")
        if (text == '') {
            text = opt.optionName
        }
        if (selected[e.selectName] == opt.optionName) {
            valid = 1
            $(option).attr('selected', 'true')
        } else {
        }
        option.innerHTML = text
        $(select).append(option)
    })
    if (valid) {
        $(second_div).addClass('valid')
    } else {
        $(second_div).addClass('caution')
    }
    $(second_div).append(select)

    var loading_img = document.createElement('img')
    loading_img.src = '/static/assets/images/loader.gif'
    loading_img.className = 'form-icons loading-icon'
    $(second_div).append(loading_img)

    var error_img = document.createElement('img')
    error_img.src = '/static/assets/images/cross.png'
    error_img.className = 'form-icons error-icon'
    $(second_div).append(error_img)

    var valid_img = document.createElement('img')
    valid_img.src = '/static/assets/images/tick.png'
    valid_img.className = 'form-icons valid-icon'
    $(second_div).append(valid_img)

    var caution_img = document.createElement('img')
    caution_img.src = '/static/assets/images/caution.png'
    caution_img.className = 'form-icons caution-icon'
    $(second_div).append(caution_img)

    $(div).append(second_div)
    return div
}

function generate_from(data) {
    i = 0;
    $('#catalog-form').empty()
    data.selectGroupList.forEach(function (e) {
        console.log(e)
        if (e.selectName != 'product' && e.optionList.length > 1) {
            select = generate_select(e)
            $('#catalog-form').append(select)
        }
    })
}

$('.first-modal-form').on('change', function (e) {
    $(this).parent().removeClass('error')
})


$('#cart-button').click(function () {
    selected = pre_selcted;
    $('.catalog-form').each(function (e) {
        $('.catalog-form').each(function () {
            val = $(this).val();
            name = $(this).attr("name");
            selected[name] = val;
        })
    })
    console.log(selected);
})
