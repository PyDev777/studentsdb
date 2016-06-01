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
        var spinner = $('#ajax-loader');
        $.ajax({
            'url': this.href,
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

    var field_set = form.find('fieldset'),
        save_btn = form.find('input[name="save_button"]'),
        cancel_btn = form.find('input[name="cancel_button"]'),
        close_btn = $('#myModal .modal-header button'),
        modal_spinner = $('#ajax-loader-modal');

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
            $.each([field_set, save_btn, cancel_btn, close_btn], function() {
                this.prop("disabled", true);
            });
        },
        'complete': function () {
            $.each([field_set, save_btn, cancel_btn, close_btn], function() {
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
        var spinner = $('#ajax-loader');
        $.ajax({
            'url': this.href,
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

function initJournalNav() {
    $('#journal-nav a').on('click', function(e) {
        var spinner = $('#ajax-loader');
        $.ajax({
            'url': this.href,
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
                initJournalNav();
                initPagination();
            }
        });
        return false;
    });
}

function initTabs() {
    $('#sub-header ul.nav-tabs').on('click', 'a', function() {
        var url = this.href,
            spinner = $('#ajax-loader');
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
                var title = $('title');
                $('#sub-header ul.nav-tabs a').each(function(k, v) {
                    if (v.href === url) {
                        title.text(title.text().split('-')[0] + '- ' + v.text);
                        $(v).parent().addClass('active');
                        $('#content-columns').html($(data).find('#content-column'));
                        initJournalNav();
                        initSorting();
                        initPagination();
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

function initSorting() {
    $('#content-column > table > thead > tr > th > a').click(function() {
        var spinner = $('#ajax-loader');
        $.ajax({
            'url': this.href,
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
                initSorting();
                initPagination();
            }
        });
        return false;
    });
}

function initPagination() {
    $('#content-column > nav > ul.pagination > li > a').click(function() {
        var li_a = $(this).parent(),
            spinner = $('#ajax-loader');
        $.ajax({
            'url': this.href,
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
                $('#content-column table > tbody').html($(data).find('#content-column table > tbody').html());
                li_a.siblings().removeClass('active');
                li_a.addClass('active');
            }
        });
        return false;
    });
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
        location.reload(true);
        return true;
    });
}


$(function() {
    initGroupSelector();
    initAddEditStudentGroupPage();
    initJournal();
    initJournalNav();
    initContactAdminPage();
    initTabs();
    initSorting();
    initPagination();
});
