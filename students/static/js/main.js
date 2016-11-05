const mainTitle = $('#title');
const mainHeader = $('#header');
const mainSubHeader = $('#sub-header');
const mainContent = $('#content-column');
const mainSpinner = $('#spinner');

const modal = $('#myModal');
const modalCloseBtn = $('#modalCloseBtn');
const modalTitle = $('#modalTitle');
const modalBody = $('#modalBody');
const modalSpinner = $('#modalSpinner');


// WORK FUNCTIONS

function alertAjaxError() {alert(gettext('There was an error on the server. Please, try again a bit later.'))}

function createForm(form, url, urlPrev, saveHistory, updLev, showReply) {
    initDateFields();
    modalCloseBtn.off('click').click(function() {
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
            modal.find(':input').prop("disabled", true);
        },
        'complete': function () {
            modal.find(':input').prop("disabled", false);
            modalSpinner.hide();
        },
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data),
                msg = html.find('#block-body .alert'),
                newform = html.find('#block-content form');
            if (newform.length > 0) {
                if (!newform.prop('action')) {newform.prop('action', url)}
                modalBody.html(msg).append(newform);
                createForm(newform, url, urlPrev, saveHistory, updLev, showReply);
            } else {
                if (showReply) {
                    //modalTitle.html(html.find('#block-title').text());
                    modalTitle.html(html.find('#block-title').addClass('alert alert-warning'));
                    modalBody.html(html.find('#block-content').addClass('alert alert-info'));
                    setTimeout(function() {modalCloseBtn.click()}, 1500);
                } else {
                    if (msg.hasClass('alert')) {setTimeout(function() {modalCloseBtn.click()},
                        msg.hasClass('alert-danger') ? 2500 : 500)}
                    else {modalCloseBtn.click()}
                }
            }
        }
    });
    return false;
}

function modalForm(url, urlPrev, saveHistory, updLev, showReply) {
    $.ajax(url, {
        'dataType': 'html',
        'type': 'GET',
        'beforeSend': function() {mainSpinner.show()},
        'complete': function() {mainSpinner.hide()},
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data),
                form = html.find('#block-content form');
            if (form.length > 0) {
                modalTitle.html(html.find('#block-title').text());
                if (!form.prop('action')) {form.prop('action', url)}
                modalBody.html(form);
                createForm(form, url, urlPrev, saveHistory, updLev, showReply);
            }
            else {
                modalTitle.text('Bad request');
                modalBody.html($('<p/>').text('This object no longer exist.').addClass('alert alert-danger'));
                modalCloseBtn.off('click').click(function() {
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

function modalInfo(url, urlPrev) {
    $.ajax(url, {
        'dataType': 'html',
        'type': 'GET',
        'beforeSend': function() {mainSpinner.show()},
        'complete': function() {mainSpinner.hide()},
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data);
            modalTitle.html(html.find('#block-title').text());
            modalBody.html(html.find('#block-body').html());
            modalCloseBtn.off('click').click(function() {
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
        'beforeSend': function() {mainSpinner.show()},
        'complete': function() {mainSpinner.hide()},
        'error': function() {alertAjaxError()},
        'success': function(data) {
            var html = $(data);
            mainTitle.text(html.find('#mainTitle').text());
            if (updLev == 'header') {mainHeader.html(html.find('#header').html())}
            if (updLev != 'content') {mainSubHeader.html(html.find('#sub-header').html())}
            mainContent.html(html.find('#content-column').html());
            if (saveHistory) {history.pushState({'urlPrev': false}, document.title, url)}
        }
    });
    return false;
}


// INITIALS

function initDateFields() {
    $('input.dateinput')
        .datetimepicker({'format': 'YYYY-MM-DD'})
        .on('dp.hide', function() {$(this).blur()})
}

function initEventHandlers() {
    // login form, registration form, profile form, group select, lang select
    mainHeader
        .on('click', 'a.user-link', function() {
            modalForm(this.href, location.href, false, 'header', false);
            return false;
        })
        .on('click', 'a.reply-link', function() {
            modalForm(this.href, location.href, false, 'header', true);
            return false;
        })
        .on('click', 'a.prof-link', function() {
            modalForm(this.href, location.href, true, 'header', false);
            return false;
        })
        .on('change', '#group-selector select', function() {
            console.log('#group-selector select is changed!');
            var group = $(this).val();
            if (group) {$.cookie('current_group', group, {'path': '/', 'expires': 365})}
            else {$.removeCookie('current_group', {'path': '/'})}
            updatePage(location.href, false, 'content');
            return false;
        })
        .on('change', '#lang-selector select', function() {
            var lang = $(this).val();
            $.cookie('django_language', lang, {'path': '/', 'expires': 365});
            updatePage(location.href, false, 'header');
            return false;
        });
    // tabs navigation links
    mainSubHeader
        .on('click', 'ul.nav-tabs a', function() {
            updatePage(this.href, true, 'sub-header');
            return false;
        });
    // student/group add/edit forms, send letter form, ordering/reversing links, journal marking
    mainContent
        .on('click', 'a.form-link', function() {
            modalForm(this.href, location.href, true, 'content', false);
            return false;
        })
        .on('click', 'a.content-link', function() {
            updatePage(this.href, true, 'content');
            return false;
        })
        .on('click', '.day-box input[type="checkbox"]', function(e) {
            var box = $(this),
                errorMsg = $('#errJournalSave');
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
                'beforeSend': function() {mainSpinner.show()},
                'complete': function() {mainSpinner.hide()},
                'error': function() {errorMsg.show()},
                'success': function() {errorMsg.hide()}
            });
        });
    // forgot password reset form
    modal
        .on('click', 'a.modal-link', function() {
            modalForm(this.href, location.href, false, 'header', true);
            return false;
        });
}

function initHistory() {
    window.onpopstate = function(e) {
        var url = e.target.document.URL,
            urlPrev = e.state.urlPrev;
        if (urlPrev) {modalForm(url, urlPrev, false, 'sub-header', false)}
        else {
            if (modal.is(':visible')) {modal.modal('hide')}
            updatePage(url, false, 'sub-header');
        }
        return false;
    }
}

// forgot password reset confirm
function CheckRedirectForm() {
    var urlForm = $('#form_action').data('form-url');
    if (urlForm) {modalForm(urlForm, location.origin, false, 'header', true)}
}


// MAIN

$(function() {
    initDateFields();
    initEventHandlers();
    initHistory();
    history.replaceState({'urlPrev': false}, document.title, location.origin);
    CheckRedirectForm();
});
