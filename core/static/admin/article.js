var selected_syns = Array();
var new_syns = Array();
var selected_id;
var activeBtn;
var new_id = 0;


function add_id(text, id, i) {
    var newid = id.replace(/[0-9]/g, '');
    var newtext = text.split(id).join(newid + i)

    return newtext;
}
function spin_content(content) {
    content = $.base64Encode(content);
    $.ajax({
        url: base_url + 'ajax/spin_content',
        method: 'POST',
        data: {
            ajax: 'spin_content',
            content: content,

        },
        success: function (e) {
            $('#preview-body').html(e);
            $('#preview-modal').modal('show')
        }
    })

}
function edit_syns_btn(c_btn) {

    selected_syns = Array();
    activeBtn = c_btn;
    var t = $(c_btn).data('text');
    $('#edit-modal-save').data('text', t)
    var t_arr = t.split('|');
    t_arr.forEach(function (e) {
        e = e.trim();
        selected_syns.push(e);
    })

    selected_id = $(c_btn).data('id')
    $('#edit-modal-save').data('id', selected_id)


    $('div#edit-modal-syns').show();

    $('#current-ones').empty();
    selected_syns.forEach(function (e) {
        var div = document.createElement('div')
        div.innerHTML = e
        div.className = 'current-one-single'
        div.contentEditable = true
        $(div).blur(function () {
            if ($(c_btn).html().trim() == '') {
                $(c_btn).remove();
            }
        })

        document.getElementById('current-ones').appendChild(div);

    })

}


var no_err = 0;
function progress_bar(max, now) {
    now = now / max * 100

    if (now == 0) {
        $('#progress').hide();
    } else {
        $('#progress').show();
    }
    $('#progress').css({ width: now + '%' });
    $('#progress').attr('aria-valuenow', now);
    $('#progress').attr('aria-valuemax', 100);
    $('#progress').html(now + '%');
}
function generation_confirm_single(id) {
    data = {
        ajax: 'generate_page',
        id: id,
        batch: batch_id,
        prog: progress,
        log_id: log_id
    }
    if (no_err == 0 && id !== undefined) {

        $.ajax({

            url: base_url + 'ajax/generate_single/' + id,
            method: 'POST',
            data: data,
            async: false,
            success: function (e) {

                if (!isNaN(e)) {
                    progress = e;
                    progress_bar(total, progress)
                    allid.shift();
                    setTimeout(function () {
                        generation_confirm_single(allid[0]);
                    }, 100)
                } else {
                    no_err = 1;
                    console.log(e);
                    alert('Error Occured: ' + e);
                }

            }
        })

    }


}
function get_postcode_text(id) {

    $.ajax({

        url: base_url + 'ajax/get_asa_direct_text/' + id,
        method: 'POST',
        data: {
            ajax: 'asa_direct_text'
        },
        success: function (e) {
            console.log(e)
            tinyMCE.activeEditor.setContent(e)
        }
    })
}
function save_postcode_text(id, text) {
    if (id) {
        $.ajax({
            url: base_url + 'ajax/save_asa_direct_text/' + id,
            method: 'POST',
            data: {
                ajax: 'save_direct_text',
                text: text
            },
            success: function (e) {

            }
        })
    } else {
        console.log('finished')
    }
}
function arrange_id(n) {
    n = parseInt(n);
    $('.elemClose').each(function () {

        var id = $(this).data('id');
        id = parseInt(id);
        if (id > n) {
            $(this).data('id', id - 1);
            console.log($(this).data('id'), n)
        }

    })
}
function pagetype_addelement(elems, type, name) {


    elems = document.getElementById(elems);

    var li = document.createElement('li');

    li.innerHTML = name + ' Type: ' + type;

    var btn = document.createElement('button')

    btn.innerHTML = '&times;';

    btn.className = 'close fixClose elemClose';


    $(btn).data('id', elements.length);

    $(btn).click(function () {

        console.log($(this).data('id'));

        elements.splice($(this).data('id'), 1);
        arrange_id($(this).data('id'))
        $(this).parent().remove();
    })

    li.appendChild(btn);

    elems.appendChild(li);

    elements.push({
        type: type,
        name: name
    })

    $('#inp-hid-data').val(JSON.stringify(elements));
}
$(document).ready(function(){

$('#save-images').click(function () {
    var arr = [];
    var div = $($(this).data('div'));
    div.empty();
    $($(this).data('input')).html('');
    $('.added').each(function () {
        arr.push($(this).data('path'));
        var img = document.createElement('img')
        $(img).attr('src', website + 'images/' + $(this).data('path'));
        div.append(img);

    })
    $($(this).data('input')).val(arr.join(','));

    $('#imageModal').modal('hide');
})



$('.elemClose').click(function () {
    elements.splice($(this).data('id'), 1);
    arrange_id($(this).data('id'));
    $('#inp-hid-data').val(JSON.stringify(elements));
})

$('#add-elem').click(function () {
    var type = $('#pagetype_edit_type').val();
    var name = $('#pagetype_edit_name').val();
    pagetype_addelement('pagetype_elements', type, name);
})

$('#text-save').click(function () {
    console.log($('#text-select').find(":selected").val(), tinyMCE.activeEditor.getContent())
    save_postcode_text($('#text-select').find(":selected").val(), tinyMCE.activeEditor.getContent())
})

$('#text-select').change(function () {
    get_postcode_text($(this).find(":selected").val());
})


$('#Generation-confirm').click(function () {
    var log = $(this).data('log');

    for (i = 0; i < progress; i++) {
        allid.shift();
    }
    progress_bar(total, progress)
    generation_confirm_single(allid[0]);
})

$('#article_content_preview').click(function () {
    spin_content(tinyMCE.activeEditor.getContent());

})
$('#article_content_add_synoms').click(function () {
    $('#edit-modal-add-init').show();
})

$('#add-target-word').click(function () {

    var val = $('#target-word-inp').val().trim();
    if (tinyMCE.activeEditor.getContent().indexOf(val) !== -1) {
        $('#edit-modal-add-init-alert').hide();
        tinyMCE.activeEditor.setContent(
            tinyMCE.activeEditor.getContent().split(val).join('{{' + val + '}}')
        )
        var ul = document.createElement('ul');
        ul.className = "article-synoms"
        ul.id = 'ul-new-' + new_id;
        $(ul).data('syns', val);

        var li = document.createElement('li');
        li.className = 'syn-word';
        li.innerHTML = val;
        ul.appendChild(li)

        var addLi = document.createElement('li')
        addLi.className = 'edit-syns';
        var button = document.createElement('button');
        button.className = 'edit_synoms_btn';
        button.innerHTML = '+';
        $(button).data('id', 'new-' + new_id);
        $(button).data('text', val);
        activeBtn = button;
        $(activeBtn).click(function () {
            edit_syns_btn(this)
        })
        addLi.appendChild(activeBtn);
        ul.appendChild(addLi)
        document.getElementById('article-synoms-div').appendChild(ul)
        edit_syns_btn(activeBtn)
        $('#edit-modal-add-init').hide();
        new_id++;

    } else {
        $('#edit-modal-add-init-alert').show();
    }
})
    
$('.edit_synoms_btn').click(function () {
    
    edit_syns_btn(this)
    $('.current-one-single').blur(function () {
        if ($(this).html().trim() == '') {
            $(this).remove();
        }
    })
})

$('.close').click(function () {
    $(this).parent().remove()
})

$('#input-modal-add').click(function () {
    var inp = $('#edit-modal-input').val();
    var div = document.createElement('div')
    div.innerHTML = inp
    div.className = 'current-one-single'
    div.contentEditable = true
    $(div).blur(function () {
        if ($(this).html().trim() == '') {
            $(this).remove();
        }
    })

    document.getElementById('current-ones').appendChild(div);
})
$('#edit-modal-cancel').click(function () {
    $('#edit-modal-syns').hide();
})
$('#edit-modal-save').click(function () {
    new_syns = Array();

    $('#ul-' + selected_id + ' .syn-word').remove();

    $('.current-one-single').each(function () {

        new_syns.push($(this).html().trim())
        var li = document.createElement('li');
        li.innerHTML = $(this).html().trim();
        li.className = 'syn-word';

        document.getElementById('ul-' + selected_id).appendChild(li)
    })
    new_syns_text = new_syns.join('| ');

    var old = $(this).data('text')

    tinyMCE.activeEditor.setContent(
        tinyMCE.activeEditor.getContent().split(old).join(new_syns_text)
    )
    document.getElementById('ul-' + selected_id).className += ' just-edited'


    var topPos = document.getElementById('ul-' + selected_id).offsetTop - 162;
    document.getElementById('article-synoms-div').scrollTop = topPos;

    console.log(topPos)
    $(activeBtn).data('text', new_syns_text)
    $('#edit-modal-syns').hide()

})


/* -------------------------------------------------- */
$('.close-btn').click(function () {
    $(this).parent().hide()
})

$('button.btn.btn-sm.btn-danger.select-remove-btn').click(function () {
    $($(this).data('remove')).remove()
})

$('#add-css-page-setting').click(function () {

    $('#css-select').append(add_id(css_Text, css_old_id, css_iter));
    css_iter++;
    $('button.btn.btn-sm.btn-danger.select-remove-btn').click(function () {
        $($(this).data('remove')).remove()
    })
})

$('#add-js-page-setting').click(function () {
    $('#js-select').append(add_id(js_Text, js_old_id, js_iter))
    js_iter++;
    $('button.btn.btn-sm.btn-danger.select-remove-btn').click(function () {
        $($(this).data('remove')).remove()
    })
})

})

console.log('asd')
tinymce.init({
    selector: 'textarea',
    height: 500,
    theme: 'modern',
    plugins: [

    ],
    image_advtab: true,
    templates: [
        { title: 'Test template 1', content: 'Test 1' },
        { title: 'Test template 2', content: 'Test 2' }
    ],
    content_css: [
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.1.3/css/bootstrap.min.css',
    ],
    plugin_preview_height: 800,
    plugin_preview_width: 1300
});
