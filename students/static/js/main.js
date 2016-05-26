function initContactAdminForm(form) {
    var save_btn = form.find('input[name="save_button"]');

    // make form work in AJAX mode
    form.ajaxForm({
        'dataType': 'html',
        'beforeSend': function() {
            save_btn.prop("disabled", true);
        },
        'complete': function () {
            save_btn.prop("disabled", false);
        },
        'error': function() {
            alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.');
        },
        'success': function(data) {
            var html = $(data),
                newform = html.find('#content-column form');

            // copy alert to modal window
            modal.find('.modal-body').html(html.find('.alert'));

            // copy form to modal if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);

                // initialize form fields and buttons
                initContactAdminForm(newform);
            } else {
                setTimeout(function(){location.reload(true);}, 500);
            }
        }
    });
    return false;
}

function initContactAdminPage() {
    $('#content-columns').on('click', 'a.contact-link', function(e) {
        var link = $(this),
            spinner = $('.ajax-loader');
        $.ajax({
            'url': link.attr('href'),
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
                // update modal window with arrived content from the server
                var html = $(data),
                    form = html.find('#content-column form');

                // init our edit form
                initContactAdminForm(form);

                // setup and show modal window finally
                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true
                });
            }
        });
        return false;
    });
}

function initDateFields() {
    $('input.dateinput').datetimepicker({
        'format': 'YYYY-MM-DD'
    }).on('dp.hide', function() {
        $(this).blur();
    });
}

function initAddEditStudentGroupForm(form, modal) {

    // attach datepicker
    initDateFields();

    var cancel_btn = form.find('input[name="cancel_button"]'),
        save_btn = form.find('input[name="save_button"]'),
        field_set = form.find('fieldset'),
        close_btn = $('#myModal button'),
        modal_spinner = $('.ajax-loader-modal');

    // close modal window on Cancel button click
    cancel_btn.on('click', function () {
        modal.modal('hide');
        return false;
    });

    // make form work in AJAX mode
    form.ajaxForm({
        'dataType': 'html',
        'beforeSend': function() {
            modal_spinner.show();
            $([field_set, save_btn, cancel_btn, close_btn]).each(function() {
                this.prop("disabled", true);
            });
        },
        'complete': function () {
            $([field_set, save_btn, cancel_btn, close_btn]).each(function() {
                this.prop("disabled", false);
            });
            modal_spinner.hide();
        },
        'error': function() {
            alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.');
        },
        'success': function(data) {
            var html = $(data),
                newform = html.find('#content-column form');

            // copy alert to modal window
            modal.find('.modal-body').html(html.find('.alert'));

            // copy form to modal if we found it in server response
            if (newform.length > 0) {
                modal.find('.modal-body').append(newform);

                // initialize form fields and buttons
                initAddEditStudentGroupForm(newform, modal);
            } else {
                // if no form, it means success and we need to reload page
                // to get updated students list;
                // reload after 2 seconds, so that user can read
                // success message
                setTimeout(function() { location.reload(true); }, 500);
            }
        }
    });
    return false;
}

function initAddEditStudentGroupPage() {
    $('#content-columns').on('click', 'a.form-link', function() {
        var link = $(this),
            spinner = $('.ajax-loader');
        $.ajax({
            'url': link.attr('href'),
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
                var modal = $('#myModal'),
                    html = $(data),
                    form = html.find('#content-column form');

                // update modal window with arrived content from the server
                modal.find('.modal-title').html(html.find('#content-column h2').text());
                modal.find('.modal-body').html(form);

                // init our edit form
                initAddEditStudentGroupForm(form, modal);

                // setup and show modal window finally
                modal.modal({
                    'keyboard': false,
                    'backdrop': false,
                    'show': true
                });
            }
        });
        return false;
    });
}

function initJournal() {
    $('#content-columns').on('click', '.day-box input[type="checkbox"]', function(e) {
        var box = $(this),
            err_mess = $('#ajax-error'),
            indicator = $('#ajax-progress-indicator');
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
                    indicator.show();
                },
                'complete': function() {
                    indicator.hide();
                },
                'error': function() {
                    err_mess.show();
                }
            }
        );
    });
}

function initTabs() {
    var tabs = $('.nav-tabs a');
    $('#sub-header').on('click', '.nav-tabs a', function() {
        var url = this.href,
            spinner = $('.ajax-loader');
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
                var html = $(data),
                    title = $('title');
                tabs.each(function(k, v) {
                    if (v.href === url) {
                        $(v).parent().addClass('active');
                        $('#content-columns').html(html.find('#content-column'));
                        title.text(title.text().split('-')[0] + '- ' + v.text);
                    } else {
                        $(v).parent().removeClass('active');
                    }
                });
                // history
            }
        });
        return false;
    });
}

function initGroupSelector() {
    // look up select element with groups and attach our even handler
    // on field "change" event
    $(document).on('change', '#group-selector select', function(e) {

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
        location.reload(true);
        return true;
    });
}


$(function() {
    initGroupSelector();
    initAddEditStudentGroupPage();
    initJournal();
    initContactAdminPage();
    initTabs();
});
