function initDateFields() {
    $('input.dateinput')
        .datetimepicker({
            'format': 'YYYY-MM-DD'
        })
        .on('dp.hide', function() {
            $(this).blur();
        });
}

function initForm(form, modal) {
    var modal_spinner = $('#ajax-loader-modal');

    // attach datepicker
    initDateFields();

    // close modal window on Cancel button click
    form.find('input[name="cancel_button"]')
        .on('click', function () {
            modal.modal('hide');
            return false;
        });

    // make form work in AJAX mode
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
        'error': function() {
            alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.');
        },
        'success': function(data) {
            var html = $(data),
                newform = html.find('#content-column form'),
                msg = html.find('.alert');

            // copy alert to modal window
            modal.find('.modal-body').html(msg);

            // copy form to modal if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);

                // initialize form fields and buttons
                initForm(newform, modal);
            } else {
                if (msg.hasClass('alert-warning')) {
                    setTimeout(function() { modal.find('button').trigger('click') }, 500);
                }
                $('#sub-header ul.nav-tabs > li.active > a').trigger('click');
            }
        }
    });
    return false;
}

function initModal(data) {
    var html = $(data),
        form = html.find('#content-column form'),
        modal = $('#myModal');
    // update modal window with arrived content from the server
    modal.find('.modal-title').html(html.find('#content-column h2').text());
    modal.find('.modal-body').html(form);
    // init our edit form
    initForm(form, modal);
    // setup and show modal window finally
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
                'beforeSend': function() {
                    spinner.show();
                },
                'complete': function () {
                    spinner.hide();
                },
                'error': function () {
                    alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.');
                },
                'success': function(data) {
                    initModal(data);
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
            $.ajax(
                box.data('url'),
                {
                    'type': 'POST',
                    'async': true,
                    'dataType': 'json',
                    'data': {
                        'pk': box.data('student-id'),
                        'date': box.data('date'),
                        'present': box.is(':checked') ? '1': '',
                        'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
                    },
                    'beforeSend': function () {
                        err_mess.hide();
                        spinner.show();
                    },
                    'complete': function() {
                        spinner.hide();
                    },
                    'error': function() {
                        err_mess.show();
                    }
                }
            );
        });
}

function handlerNav(e) {
    var spinner = $('#ajax-loader'),
        url = e.target.href;
    $.ajax({
        'url': url,
        'dataType': 'html',
        'type': 'get',
        'beforeSend': function() {
            spinner.show();
        },
        'complete': function() {
            spinner.hide();
        },
        'error': function () {
            alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.');
        },
        'success' : function(data) {
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
            'beforeSend': function() {
                spinner.show();
            },
            'complete': function() {
                spinner.hide();
            },
            'error': function () {
                alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.');
            },
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
            'beforeSend': function () {
                spinner.show();
            },
            'complete': function () {
                spinner.hide();
            },
            'error': function () {
                alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.');
            },
            'success': function (data) {
                if (e.state['modal']) {
                    initModal(data);
                } else {
                    var modal = $('#myModal');
                    if (modal.hasClass('in')) {
                        modal.find('button').trigger('click');
                    }
                    updateTabs(data);
                }
            }
        });
        return false;
    }
}

function initGroupSelector() {
    // look up select element with groups and attach our even handler
    // on field "change" event
    $('#header').on('change', '#group-selector select', function(e) {
        // get value of currently selected group option
        var group = $(this).val();
        if (group) {
            // set cookie with expiration date 1 year since now;
            // cookie creation function takes period in days
            $.cookie('current_group', group, {'path': '/', 'expires': 365});
        } else {
            // otherwise we delete the cookie
            $.removeCookie('current_group', {'path': '/'});
        }
        // and reload a page
        $('#sub-header ul.nav-tabs > li.active > a').trigger('click');
        return false;
    });
}

$(function() {
    initGroupSelector();
    initTabs();
    initPage();
    initJournal();
    initHistory();
    history.replaceState({'modal': false}, document.title, window.location.href);
});
