var selected = {},
    // pre_selected data has the product listed for each specific pages
    pre_selcted = {
        'product': product_value
    },
    selected_names = {},
    testEmail = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i,
    orientation = 'p';


function get_catalog_data(selected) {
    // The primary function that gets catalog form data from the api
    // @ calls api /api/catalog --> api.views.catalog_api
    // @ uses preselected data that has the product listed

    data = {
        'selected': pre_selcted
    }
    if (selected) {
        data = {
            'selected': selected
        }
    }

    // Ajax request to get form data from api
    $.ajax({
        method: 'POST',
        url: '/api/catalog/',
        contentType: 'application/json',
        data: JSON.stringify(data),
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        },
        success: function (data) {
            // generate forms with the api data

            generate_from(data);
            view_price(data.selected);
        }
    })
}


function view_price(data) {
    priceGross = data.priceGross
    priceNet = data.priceNet
    shippingNet = data.shippingNet
    shippingGross = data.shippingGross
    $('#price-net-p').html('Price Net: ' + data.priceNet)
    $('#price-gross-p').html('Price Gross: ' + data.priceGross)
    $('#shipping-net-p').html('Shipping Net: ' + data.shippingNet)
    $('#shipping-gross-p').html('Shipping Gross: ' + data.shippingGross)
}


$('.catalog-form').on('change', function (e) {
    selected = pre_selcted;
    $(this).parent().removeClass('caution');
    $(this).parent().removeClass('error');
    $(this).parent().removeClass('valid');
    $(this).parent().addClass('loading');
    $('.catalog-form').each(function () {
        val = $(this).val();
        name = $(this).attr("name");
        selected[name] = val;
    })
    get_catalog_data(selected)
})

function generate_select(e) {
    // This generates single selects
    // @creates option from the api data

    if (e.selectName == 'a_format') {
        // empty the paper size div
        $('#paper-sizes').empty();
    }

    if (e.selectName == 'a_format_dir') {
        // TODO fix orientation
        // this is where the orientation div will function
        $('.orientation-btn').hide()
        e.optionList.forEach(function (opt) {
            if (opt.optionName == "A_panel_format") {

                $('#portrait').show();
                if (opt.selected) {
                    to_portrait()
                }
            }
            if (opt.optionName == "A_landscape_format") {
                $('#landscape').show();
                if (opt.selected) {
                    to_landscape()
                }
            }
        })
    }

    div = document.createElement('div');
    div.className = 'form-group row';
    label = document.createElement('label');
    l = e.selectDescription.split('_');
    a = [];
    l.forEach(function (e) {
        if (e.length > 1) {
            a.push(e.charAt(0).toUpperCase() + e.substring(1));
        }
    })

    label.innerHTML = a.join(' ') + ":";
    $(label).attr('for', e.selectName);
    $(label).addClass('col-sm-2');
    $(div).append(label);
    var second_div = document.createElement('div');
    second_div.className = 'form-with-icon col-sm-10';
    select = document.createElement('select');
    select.className = 'form-control catalog-form';
    select.id = e.selectName;
    $(select).attr('name', e.selectName);
    $(select).click(function (e) {
        $(this).removeClass('caution');
    })
    $(select).on('change', function (e) {
        selected = pre_selcted;
        $(this).parent().removeClass('caution');
        $(this).parent().removeClass('error');
        $(this).parent().removeClass('valid');
        $(this).parent().addClass('loading');
        $('.catalog-form').each(function () {
            val = $(this).val();
            name = $(this).attr("name");
            selected[name] = val;
        })
        get_catalog_data(selected);
    })
    valid = 0;
    e.optionList.forEach(function (opt) {
        option = document.createElement('option');
        option.value = opt.optionName;
        text = opt.optionTranslations.join(" ");
        if (text == '') {
            text = opt.optionName;
        }
        if (selected[e.selectName] == opt.optionName) {
            valid = 1;
            $(option).attr('selected', 'true');
        } else {

        }
        option.innerHTML = text;
        $(select).append(option);
        if (e.selectName == 'a_format') {
            if (opt.optionTranslations.length == 3) {
                w = opt.optionTranslations[0].split(' ')[0] * .7;
                h = opt.optionTranslations[1].split(' ')[0] * .7;
                name = opt.optionTranslations[2];

                var paperSize = document.createElement('div');
                paperSize.className = 'paper-size';
                if (opt.selected) {
                    paperSize.className += ' selected';
                }

                $(paperSize).data('w', w);
                $(paperSize).data('h', h);
                $(paperSize).data('option', opt.optionName);
                $(paperSize).html(name)
                $(paperSize).css({
                    'width': w + 'px',
                    'height': h + 'px'
                })
                $(paperSize).click(function () {
                    paper_size_event(this);
                    console.log($(this).data());
                })
                $('#paper-sizes').append(paperSize);
            }
        }
    })

    if (valid) {
        $(second_div).addClass('valid');
    } else {
        $(second_div).addClass('caution');
    }

    $(second_div).append(select)

    var loading_img = document.createElement('img');
    loading_img.src = '/static/assets/images/loader.gif';
    loading_img.className = 'form-icons loading-icon';
    $(second_div).append(loading_img);

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
        if (e.selectName != 'product') {
            // this will generate selects
            select = generate_select(e)
            // add any html edit to selects here
            // .........
            $('#catalog-form').append(select)
        }
    })
}

$('.paper-size').click(function () {
    paper_size_event(this)
})


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
            selected_names[name] = $(this).find(":selected").text();
        })
    })

    data = {
        'selected': selected,
        'selected_names': selected_names,
        'slug': slug,
        'prices': {
            'priceNet': priceNet,
            'priceGross': priceGross,
            'shippingNet': shippingNet,
            'shippingGross': shippingGross
        }
    }

    console.log(data)

    $.ajax({
        url: '/api/add_to_cart/',
        method: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success: function (e) {
            new_item = e.new_item;
            console.log(new_item.data_name);
            $('#product-cart-detail').empty();

            for (x in new_item.data_name) {
                propertyDiv = document.createElement('div');
                propertyDiv.className = 'property';

                fieldDiv = document.createElement('div');
                fieldDiv.className = 'field';

                l = x.split('_');
                a = [];
                l.forEach(function (e) {
                    if (e.length > 1) {
                        a.push(e.charAt(0).toUpperCase() + e.substring(1));
                    }
                })
                fieldDiv.innerHTML = a.join(' ') + ":";
                $(propertyDiv).append(fieldDiv);
                valueDiv = document.createElement('div');
                valueDiv.className = 'value';
                valueDiv.innerHTML = new_item.data_name[x];
                $(propertyDiv).append(valueDiv);
                $('#product-cart-detail').append(propertyDiv);
            }

            $('#new-cart-modal').modal('show');

        }
    })
})

$('#portrait').click(function () {
    to_portrait();
    $('#a_format_dir').val('A_panel_format')
    start_catalog_fetch()
})

$('#landscape').click(function () {
    to_landscape();
    $('#a_format_dir').val('A_landscape_format')
    start_catalog_fetch()
})

function to_portrait() {
    orientation = 'p';
    $('.orientation-btn').removeClass('oreintaiton__active');
    $('#portrait').addClass('oreintaiton__active');

    $('.paper-size').each(function () {
        $(this).css({
            'width': $(this).data('w') + 'px',
            'height': $(this).data('h') + 'px'
        })
    })
}

function to_landscape() {
    orientation = 'l';

    $('.orientation-btn').removeClass('oreintaiton__active');
    $('#landscape').addClass('oreintaiton__active');

    $('.paper-size').each(function () {
        $(this).css({
            'width': $(this).data('h') + 'px',
            'height': $(this).data('w') + 'px'
        })
    })
}

function paper_size_event(elem) {
    opt = $(elem).data('option');
    $('#a_format').val(opt);
    start_catalog_fetch()
}


function start_catalog_fetch(){
    selected = pre_selcted;
    $('.catalog-form').each(function () {
        val = $(this).val();
        name = $(this).attr("name");
        selected[name] = val;
    })
    get_catalog_data(selected);
}
