function createForm(form, modal, urlPrev, saveHistory, updLev) {
    var modal_spinner = $('#ajax-loader-modal'),
        close_button = modal.find('button.close');
    initDateFields();
    close_button.off('click').click(function() {
        updatePage(urlPrev, saveHistory, updLev);
        modal.modal('hide');
        return false;
    });
    form.find('input[name="cancel_button"]').click(function() {
        updatePage(urlPrev, saveHistory, updLev);
        modal.modal('hide');
        return false;
    });
    form.ajaxForm({
        'dataType': 'html',
        'beforeSend': function() {
            modal_spinner.show();
            $(':input').prop("disabled", true);
        },
        'complete': function () {
            $(':input').prop("disabled", false);
            modal_spinner.hide();
        },
        'error': function() {alert(gettext('There was an error on the server. Please, try again a bit later.'))},
        'success': function(data) {
            var html = $(data),
                msg = html.find('.alert'),
                newform = html.find('#content-column form');
            modal.find('.modal-body').html(msg);
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);
                createForm(newform, modal, urlPrev, saveHistory, updLev);
            } else {

                if (msg.hasClass('alert')) {setTimeout(function() {close_button.trigger('click')},
                    msg.hasClass('alert-danger') ? 2500 : 500)}
                else {close_button.trigger('click')}
            }
        }
    });
    return false;
}

function showModal(url, urlPrev, saveHistory, updLev) {
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
            if (form.length > 0) {
                modal.find('.modal-body').html(form);
                createForm(form, modal, urlPrev, saveHistory, updLev);
            } else {
                modal.find('.modal-body').html(html.find('#content-column'));
                modal.find('button.close').off('click').click(function() {
                    modal.modal('hide');
                    updatePage(urlPrev, saveHistory, updLev);
                    return false;
                });
            }
            modal.modal({'keyboard': false, 'backdrop': false, 'show': true});
            if (saveHistory) {history.pushState({'urlPrev': urlPrev}, document.title, url)}
        }
    });
    return false;
}

function updatePage(url, saveHistory, updLev) {
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
            $('#content-column').html(html.find('#content-column').html());
            if (updLev != 'content') {$('#sub-header').html(html.find('#sub-header').html())}
            if (updLev == 'header') {$('#header').html(html.find('#header').html())}
            if (saveHistory) {history.pushState({'urlPrev': false}, document.title, url)}
        }
    });
}

function initDateFields() {
    $('input.dateinput')
        .datetimepicker({'format': 'YYYY-MM-DD'})
        .on('dp.hide', function() {$(this).blur()});
}

function initHandlers() {
    $('#header')
        // login form
        .on('click', 'a.user-link', function() {
            var urlPrev = location.href,
                url = this.href;
            showModal(url, urlPrev, false, 'header');
            return false;
        })
        // registration form
        .on('click', 'a.reg-link', function() {
            var urlPrev = location.href,
                url = this.href;
            showModal(url, urlPrev, false, 'header');
            return false;
        })
        // user profile form
        .on('click', 'a.prof-link', function() {
            var urlPrev = location.href,
                url = this.href;
            showModal(url, urlPrev, true, 'header');
            return false;
        })
        // group select
        .on('change', '#group-selector select', function() {
            var group = $(this).val(),
                url = location.href;
            if (group) {$.cookie('current_group', group, {'path': '/', 'expires': 365})}
            else {$.removeCookie('current_group', {'path': '/'})}
            updatePage(url, false, 'content');
            return false;
        })
        // lang select
        .on('change', '#lang-selector select', function() {
            var lang = $(this).val(),
                url = location.href;
            $.cookie('django_language', lang, {'path': '/', 'expires': 365});
            updatePage(url, false, 'header');
            return false;
        });
    $('#sub-header')
        // tabs navigation links
        .on('click', 'ul.nav-tabs a', function() {
            var url = this.href;
            updatePage(url, true, 'sub-header');
            return false;
        });
    $('#content-columns')
        // student/group add/edit forms
        .on('click', 'a.form-link', function() {
            var urlPrev = location.href,
                url = this.href;
            showModal(url, urlPrev, true, 'content');
            return false;
        })
        // journal month navigation links
        .on('click', 'a.content-link', function() {
            var url = this.href;
            updatePage(url, true, 'content');
            return false;
        })
        // journal marking
        .on('click', '.day-box input[type="checkbox"]', function(e) {
            var box = $(this),
                err_msg = $('#ajax-error'),
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
                    err_msg.hide();
                    spinner.show();
                },
                'complete': function() {spinner.hide()},
                'error': function() {err_msg.show()}
            });
        });
}

function initHistory() {
    window.onpopstate = function(e) {
        var url = e.target.document.URL,
            urlPrev = e.state['urlPrev'];
        if (urlPrev) {showModal(url, urlPrev, false, 'sub-header')}
        else {
            var modal = $('#myModal');
            if (modal.is(':visible')) {modal.modal('hide')}
            updatePage(url, false, 'sub-header');
        }
        return false;
    }
}

$(function() {
    initDateFields();
    initHandlers();
    initHistory();
    history.replaceState({'urlPrev': false}, document.title, location.href);
});
