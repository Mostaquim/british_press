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
            start_loader()
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (data) {
            hide_loader()
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

function generate_select(e) {
    div = document.createElement('div')
    div.className = 'form-group'
    label = document.createElement('label')
    label.innerHTML = e.selectDescription
    $(label).attr('for', e.selectName)
    $(div).append(label)
    select = document.createElement('select')
    select.className = 'form-control catalog-form'
    select.id = e.selectName
    $(select).attr('name', e.selectName)
    $(select).on('change', function (e) {
        selected = pre_selcted

        $('.catalog-form').each(function () {
            val = $(this).val()
            name = $(this).attr("name")
            selected[name] = val
        })
        get_catalog_data(selected)
    })

    e.optionList.forEach(function (opt) {
        option = document.createElement('option')
        option.value = opt.optionName
        text = opt.optionTranslations.join(" ")
        if (text == '') {
            text = opt.optionName
        }
        if (selected[e.selectName] == opt.optionName) {
            $(option).attr('selected', 'true')
        }
        option.innerHTML = text
        $(select).append(option)
    })
    $(div).append(select)
    return div
}

function generate_from(data) {
    var odd_div = document.createElement('div')
    odd_div.id = 'odd_div'
    odd_div.className = 'col-md-6'
    var even_div = document.createElement('div')
    even_div.className = 'col-md-6'
    even_div.id = 'even_div'
    i = 0;
    data.selectGroupList.forEach(function (e) {
        if (e.selectName != 'product') {
            select = generate_select(e)
            if (i % 2) {
                $(even_div).append(select)
            } else {
                $(odd_div).append(select)
            }
            i++;
        }
    })
    $('#catalog-form').empty()
    $('#catalog-form').append(odd_div)
    $('#catalog-form').append(even_div)
}

get_catalog_data()

$('.first-modal-form').on('change', function (e) {
    $(this).parent().removeClass('error')
})

$('#next-1').click(function () {
    error = 0
    $('.first-modal-form').each(function () {

        if ($(this).val() == '') {
            error = 1

            $(this).parent().addClass('error')
        } else {
            $(this).parent().removeClass('error')
            if ($(this).attr('name') == 'email') {
                if (!testEmail.test($(this).val())) {
                    $(this).parent().addClass('error')
                    error = 1
                }
            }
        }

    })

    if (!error) {
        email = $('#email').val()
        company = $('#company').val()
        salutation = $('#salutation').val()
        firstName = $('#first-name').val()
        lastName = $('#last-name').val()
        street = $('#street').val()
        houseNumber = $('#house-number').val()
        city = $('#city').val()
        zipCode = $('#zip-code').val()
        phonePrefix = $('#phone-prefix').val()
        phoneNumber = $('#phone-number').val()
        comment = $('#comment').val()

        formData = {
            'email': email,
            'company': company,
            'salutation': salutation,
            'firstName': firstName,
            'lastName': lastName,
            'street': street,
            'houseNumber': houseNumber,
            'zipCode': zipCode,
            'city': city,
            'phonePrefix': phonePrefix,
            'phoneNumber': phoneNumber,
            'comment': comment
        }

        vals = pre_selcted
        $('.catalog-form').each(function () {
            val = $(this).val()
            name = $(this).attr("name")
            vals[name] = val
        })

        data = {
            'formData': formData,
            'selected': vals
        }

        $.ajax({
            method: 'POST',
            url: '/api/create_product/',
            contentType: 'application/json',
            data: JSON.stringify(data),
            beforeSend: function (xhr, settings) {
                start_loader()
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                }
            },
            success: function (e) {
                console.log(e)
            }
        });
    }
});
