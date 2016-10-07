function initDateFields() {
    $('input.dateinput')
        .datetimepicker({'format': 'YYYY-MM-DD'})
        .on('dp.hide', function() {$(this).blur()});
}

function createForm(form, modal, urlPrev) {
    var modal_spinner = $('#ajax-loader-modal'),
        close_button = modal.find('button.close');
    initDateFields();
    close_button.off('click').click(function() {
        modal.modal('hide');
        updateContent(urlPrev, true);
        return false;
    });
    form.find('input[name="cancel_button"]').click(function() {
        modal.modal('hide');
        updateContent(urlPrev, true);
        return false;
    });
    form.ajaxForm({
        'dataType': 'html',
        'beforeSend': function() {
            modal_spinner.show();
            $('button, fieldset, input').prop("disabled", true);
        },
        'complete': function () {
            $('button, fieldset, input').prop("disabled", false);
            modal_spinner.hide();
        },
        'error': function() {alert(gettext('There was an error on the server. Please, try again a bit later.'))},
        'success': function(data) {
            var html = $(data),
                newform = html.find('#content-column form'),
                msg = html.find('.alert');
            modal.find('.modal-body').html(msg);
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);
                createForm(newform, modal, urlPrev);
            } else {
                var msg_time = 500;
                if (msg.hasClass('alert-danger')) {msg_time = 2500}
                setTimeout(function() {close_button.trigger('click')}, msg_time);
            }
        }
    });
    return false;
}

function showModal(url, urlPrev, saveHistory) {
    var spinner = $('#ajax-loader');
    $.ajax({
        'url': url,
        'dataType': 'html',
        'type': 'get',
        'beforeSend': function() {spinner.show()},
        'complete': function() {spinner.hide()},
        'error': function() {alert(gettext('There was an error on the server. Please, try again a bit later.'))},
        'success': function(data) {
            var html = $(data),
                form = html.find('#content-column form'),
                modal = $('#myModal');
            modal.find('.modal-title').html(html.find('#content-column h2').text());
            modal.find('.modal-body').html(form);
            createForm(form, modal, urlPrev);
            modal.modal({
                'keyboard': false,
                'backdrop': false,
                'show': true
            });
            if (saveHistory) {history.pushState({'urlPrev': urlPrev}, document.title, url)}
        }
    });
}

function initModal() {
    $('#content-columns').on('click', 'a.form-link', function() {
        var urlPrev = location.href,
            url = this.href;
        showModal(url, urlPrev, true);
        return false;
    });
}

function updateContent(url, saveHistory) {
    var spinner = $('#ajax-loader');
    $.ajax({
        'url': url,
        'dataType': 'html',
        'type': 'get',
        'beforeSend': function() {spinner.show()},
        'complete': function() {spinner.hide()},
        'error': function() {alert(gettext('There was an error on the server. Please, try again a bit later.'))},
        'success': function(data) {
            var html = $(data);
            $('title').text(html.filter('title').text());
            $('#sub-header').html(html.find('#sub-header').html());
            $('#content-column').html(html.find('#content-column').html());
            if (saveHistory) {history.pushState({'urlPrev': false}, document.title, url)}
        }
    });
}

function initGroupSelector() {
    $('#header').on('change', '#group-selector select', function() {
        var url = location.href,
            group = $(this).val();
        if (group) {$.cookie('current_group', group, {'path': '/', 'expires': 365})}
        else {$.removeCookie('current_group', {'path': '/'})}
        updateContent(url, false);
        return false;
    });
}

function initLangSelector() {
    $('#header').on('change', '#lang-selector select', function() {
        var curr_lang = $(this).val(),
            curr_path = location.href;
        $.cookie('django_language', curr_lang, {'path': curr_path, 'expires': 365});
        document.location.reload(true);
        return false;
    });
}

function initTabs() {
    $('#sub-header').on('click', 'ul.nav-tabs a', function() {
        var url = this.href;
        updateContent(url, true);
        return false;
    });
}

function initNavs() {
    $('#content-columns').on('click', 'a.content-link', function() {
        var url = this.href;
        updateContent(url, true);
        return false;
    });
}

function initJournal() {
    $('#content-columns').on('click', '.day-box input[type="checkbox"]', function() {
        var box = $(this),
            err_mess = $('#ajax-error'),
            spinner = $('#ajax-loader');
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': box.data('student-id'),
                'date': box.data('date'),
                'present': box.is(':checked') ? '1': '',
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function() {
                err_mess.hide();
                spinner.show();
            },
            'complete': function() {spinner.hide()},
            'error': function() {err_mess.show()}
        });
    });
}

function initHistory() {
    window.onpopstate = function(e) {
        var url = e.target.document.URL,
            urlPrev = e.state['urlPrev'];
        if (urlPrev) {showModal(url, urlPrev, false)}
        else {
            var modal = $('#myModal');
            if (modal.is(':visible')) {modal.modal('hide')}
            updateContent(url, false);
        }
        return false;
    }
}

$(function() {
    initDateFields();
    initTabs();
    initNavs();
    initJournal();
    initLangSelector();
    initGroupSelector();
    initModal();
    initHistory();
    history.replaceState({'urlPrev': false}, document.title, location.href);
});
