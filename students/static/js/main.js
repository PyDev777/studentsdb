const modal = $('#myModal');
const ajaxSpinner = $('#ajax-loader');
const modalSpinner = $('#ajax-loader-modal');
const modalTitle = modal.find('.modal-title');
const modalBody = modal.find('.modal-body');
const modalCloseButton = modal.find('button.close');

function alertAjaxError() {alert(gettext('There was an error on the server. Please, try again a bit later.'))}

function createForm(form, urlPrev, saveHistory, updLev) {
    initDateFields();
    modalCloseButton.off('click').click(function() {
        modal.modal('hide');
        updatePage(urlPrev, saveHistory, updLev);
        return false;
    });
    form.find('input[name="cancel_button"]').click(function() {
        modal.modal('hide');
        updatePage(urlPrev, saveHistory, updLev);
        return false;
    });
    form.ajaxForm({
        'dataType': 'html',
        'beforeSend': function() {
            modalSpinner.show();
            $('#myModal:input').prop("disabled", true);
        },
        'complete': function () {
            $('#myModal:input').prop("disabled", false);
            modalSpinner.hide();
        },
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data),
                msg = html.find('.alert'),
                newform = html.find('#content-column form');
            modalBody.html(msg);
            if (newform.length > 0) {
                modalBody.append(newform);
                createForm(newform, urlPrev, saveHistory, updLev);
            } else {
                if (msg.hasClass('alert')) {setTimeout(function() {modalCloseButton.click()},
                    msg.hasClass('alert-danger') ? 2500 : 500)}
                else {modalCloseButton.click()}
            }
        }
    });
    return false;
}

function modalForm(url, urlPrev, saveHistory, updLev) {
    $.ajax(url, {
        'dataType': 'html',
        'type': 'GET',
        'beforeSend': function() {ajaxSpinner.show()},
        'complete': function() {ajaxSpinner.hide()},
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data),
                form = html.find('#content-column form');
            if (form.length > 0) {
                modalTitle.html(html.find('#content-column h2').text());
                modalBody.html(form);
                createForm(form, urlPrev, saveHistory, updLev);
                modal.modal({'keyboard': false, 'backdrop': false, 'show': true});
                if (saveHistory) {history.pushState({'urlPrev': urlPrev}, document.title, url)}
            }
        }
    });
    return false;
}

// Show modal with info.
// url: target url
// urlPrev: if present then history must be save
function modalInfo(url, urlPrev) {
    $.ajax(url, {
        'dataType': 'html',
        'type': 'GET',
        'beforeSend': function() {ajaxSpinner.show()},
        'complete': function() {ajaxSpinner.hide()},
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data);
            modalTitle.html(html.find('#block-title').text());
            modalBody.html(html.find('#block-body').html());
            modalCloseButton.off('click').click(function() {
                modal.modal('hide');
                if (urlPrev) {updatePage(urlPrev, true, 'header')}
                return false;
            });
            if (urlPrev) {history.pushState({'urlPrev': urlPrev}, document.title, url)}
            modal.modal({'keyboard': false, 'backdrop': false, 'show': true});
        }
    });
    return false;
}

function updatePage(url, saveHistory, updLev) {
    $.ajax(url, {
        'dataType': 'html',
        'type': 'GET',
        'beforeSend': function() {ajaxSpinner.show()},
        'complete': function() {ajaxSpinner.hide()},
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data);
            $('title').text(html.filter('title').text());
            $('#content-column').html(html.find('#content-column').html());
            if (updLev != 'content') {$('#sub-header').html(html.find('#sub-header').html())}
            if (updLev == 'header') {$('#header').html(html.find('#header').html())}
            if (saveHistory) {history.pushState({'urlPrev': false}, document.title, url)}
        }
    });
    return false;
}

function initDateFields() {
    $('input.dateinput')
        .datetimepicker({'format': 'YYYY-MM-DD'})
        .on('dp.hide', function() {$(this).blur()});
}

function initEventHandlers() {
    $('#header')
        // login form
        .on('click', 'a.user-link', function() {
            var urlPrev = location.href,
                url = this.href;
            modalForm(url, urlPrev, false, 'header');
            return false;
        })
        // registration form
        .on('click', 'a.reg-link', function() {
            var urlPrev = location.href,
                url = this.href;
            modalForm(url, urlPrev, false, 'header');
            return false;
        })
        // profile info
        .on('click', 'a.prof-link', function() {
            var urlPrev = location.href,
                url = this.href;
            modalInfo(url, urlPrev);
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
            modalForm(url, urlPrev, true, 'content');
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
                errorMsg = $('#ajax-error');
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
                'beforeSend': function() {ajaxSpinner.show()},
                'complete': function() {ajaxSpinner.hide()},
                'error': function() {errorMsg.show()},
                'success': function() {errorMsg.hide()}
            });
        });
}

function initHistory() {
    // AJAX History
    window.onpopstate = function(e) {
        var url = e.target.document.URL,
            urlPrev = e.state.urlPrev;
        if (urlPrev) {modalForm(url, urlPrev, false, 'sub-header')}
        else {
            if (modal.is(':visible')) {modal.modal('hide')}
            updatePage(url, false, 'sub-header');
        }
        return false;
    }
}

$(function() {
    initDateFields();
    initEventHandlers();
    initHistory();
    history.replaceState({'urlPrev': false}, document.title, location.href);
});
