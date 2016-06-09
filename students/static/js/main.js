function initDateFields() {
    $('input.dateinput')
        .datetimepicker({'format': 'YYYY-MM-DD'})
        .on('dp.hide', function() {$(this).blur()});
}

function createForm(form, modal) {
    var modal_spinner = $('#ajax-loader-modal');
    initDateFields();
    form.find('input[name="cancel_button"]').on('click', function() {
        modal.modal('hide');
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
        'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
        'success': function(data) {
            var html = $(data),
                newform = html.find('#content-column form'),
                msg = html.find('.alert');
            modal.find('.modal-body').html(msg);
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);
                createForm(newform, modal);
            } else {
                if (msg.hasClass('alert-warning')) {
                    setTimeout(function() {modal.find('button.close').trigger('click')}, 500);
                }
            }
        }
    });
    return false;
}

function createModal(data) {
    var html = $(data),
        form = html.find('#content-column form'),
        modal = $('#myModal');
    modal.find('.modal-title').html(html.find('#content-column h2').text());
    modal.find('.modal-body').html(form);
    createForm(form, modal);
    modal.modal({
        'keyboard': false,
        'backdrop': false,
        'show': true
    });
}

function initPage() {
    $('#content-columns')
        .on('click', 'ul.pagination a, table th > a', handlerNav)
        .on('click', 'a.form-link', function() {
            var spinner = $('#ajax-loader'),
                url = this.href;
            $.ajax({
                'url': url,
                'dataType': 'html',
                'type': 'get',
                'beforeSend': function() {spinner.show()},
                'complete': function() {spinner.hide()},
                'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
                'success': function(data) {
                    createModal(data);
                    history.pushState({'modal': true}, document.title, url);
                }
            });
            return false;
        });
}

function initJournal() {
    $('#content-columns')
        .on('click', '#journal-nav a, a#journal-one-man', handlerNav)
        .on('click', '.day-box input[type="checkbox"]', function() {
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

function handlerNav(e) {
    var spinner = $('#ajax-loader'),
        url = e.target.href;
    $.ajax({
        'url': url,
        'dataType': 'html',
        'type': 'get',
        'beforeSend': function() {spinner.show()},
        'complete': function() {spinner.hide()},
        'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
        'success': function(data) {
            $('#content-column').html($(data).find('#content-column').html());
            history.pushState({'modal': false}, document.title, url);
        }
    });
    return false;
}

function updateTabs(data) {
    var html = $(data);
    $('title').text(html.filter('title').text());
    $('#sub-header').html(html.find('#sub-header').html());
    $('#content-column').html(html.find('#content-column').html());
}

function initTabs() {
    $('#sub-header').on('click', 'ul.nav-tabs a, a#journal-one-man', function() {
        var spinner = $('#ajax-loader'),
            url = this.href;
        $.ajax({
            'url': url,
            'dataType': 'html',
            'type': 'get',
            'beforeSend': function() {spinner.show()},
            'complete': function() {spinner.hide()},
            'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
            'success': function(data) {
                updateTabs(data);
                history.pushState({'modal': false}, document.title, url);
            }
        });
        return false;
    });
}

function initHistory() {
    window.onpopstate = function(e) {
        var spinner = $('#ajax-loader');
        $.ajax({
            'url': e.target.document.URL,
            'dataType': 'html',
            'type': 'get',
            'beforeSend': function() {spinner.show()},
            'complete': function() {spinner.hide()},
            'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
            'success': function (data) {
                if (e.state['modal']) {createModal(data)}
                else {
                    var modal = $('#myModal');
                    if (modal.hasClass('in')) {modal.find('button.close').trigger('click')}
                    updateTabs(data);
                }
            }
        });
        return false;
    }
}

function initGroupSelector() {
    $('#header').on('change', '#group-selector select', function() {
        var group = $(this).val(),
            spinner = $('#ajax-loader');
        if (group) {$.cookie('current_group', group, {'path': '/', 'expires': 365})}
        else {$.removeCookie('current_group', {'path': '/'})}
        $.ajax({
            'url': location,
            'dataType': 'html',
            'type': 'get',
            'beforeSend': function() {spinner.show()},
            'complete': function() {spinner.hide()},
            'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
            'success': function(data) {updateTabs(data)}
        });
        return false;
    });
}

$(function() {
    initGroupSelector();
    initTabs();
    initPage();
    initJournal();
    initHistory();
    history.replaceState({'modal': false}, document.title, location);
});
