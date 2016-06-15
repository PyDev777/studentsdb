function createForm(form, modal, urlPrev, updateHistory) {
    console.log('(ENTER) createForm: <- urlPrev=', urlPrev, ', updateHistory=', updateHistory);
    var modal_spinner = $('#ajax-loader-modal'),
        close_button = modal.find('button.close');
    initDateFields();
    // close button handler
    close_button.off('click').click(function() {
        console.log('(EVENT) createForm.close_button');
        modal.modal('hide');
        console.log('createForm.close_button: -> updateContent(urlPrev=', urlPrev, 'updateHistory=', updateHistory, ')');
        updateContent(urlPrev, updateHistory);
        console.log('createForm.close_button: done.');
        return false;
    });
    // cancel button handler
    form.find('input[name="cancel_button"]').click(function() {
        console.log('(EVENT) createForm.cancel_button');
        modal.modal('hide');
        console.log('createForm.cancel_button: -> updateContent(urlPrev=', urlPrev, 'updateHistory=', updateHistory, ')');
        updateContent(urlPrev, updateHistory);
        console.log('createForm.cancel_button: done.');
        return false;
    });
    // ajax form
    console.log('createForm: AJAX-FORM request started...');
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
                console.log('createForm: -> newform.length > 0');
                modal.find('.modal-body').append(newform);
                console.log('createForm: -> again createForm(newform, modal, urlPrev=', urlPrev, 'updateHistory=false)');
                createForm(newform, modal, urlPrev, false);
                console.log('createForm: again createForm done.');
            } else {
                console.log('createForm: prepare to exit');
                if (msg.hasClass('alert-warning')) {
                    console.log('createForm: trigger to exit');
                    setTimeout(function() {close_button.trigger('click')}, 500);
                }
            }
            console.log('createForm: AJAX-FORM request done.');
        }
    });
    return false;
}

function showModal(url, urlPrev, updateHistory) {
    var spinner = $('#ajax-loader');
    console.log('(ENTER) showModal: <- url=', url, ', updateHistory=', updateHistory);
    console.log('showModal: AJAX request started...');
    $.ajax({
        'url': url,
        'dataType': 'html',
        'type': 'get',
        'beforeSend': function() {spinner.show()},
        'complete': function() {spinner.hide()},
        'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
        'success': function(data) {
            var html = $(data),
                form = html.find('#content-column form'),
                modal = $('#myModal');
            modal.find('.modal-title').html(html.find('#content-column h2').text());
            modal.find('.modal-body').html(form);
            console.log('showModal: modal title and body created.');
            console.log('showModal: -> createForm(form, modal, urlPrev=', urlPrev, ', updateHistory=', updateHistory, ')');
            createForm(form, modal, urlPrev, updateHistory);
            modal.modal({
                'keyboard': false,
                'backdrop': false,
                'show': true
            });
            console.log('showModal: modal.modal created.');
            if (updateHistory) {
                console.log('showModal: --> pushState({urlPrev:', urlPrev, '}, title=', document.title, ', url=', url, ')');
                history.pushState({'urlPrev': urlPrev}, document.title, url);
            }
            console.log('showModal: AJAX request done.');
        }
    });
}

function updateContent(url, updateHistory) {
    var spinner = $('#ajax-loader');
    console.log('(ENTER) updateContent: <- url=', url, ', updateHistory=', updateHistory);
    $.ajax({
        'url': url,
        'dataType': 'html',
        'type': 'get',
        'beforeSend': function() {spinner.show()},
        'complete': function() {spinner.hide()},
        'error': function() {alert('Помилка на сервері. Спробуйте, будь-ласка, пізніше.')},
        'success': function(data) {
            var html = $(data);
            $('title').text(html.filter('title').text());
            $('#sub-header').html(html.find('#sub-header').html());
            $('#content-column').html(html.find('#content-column').html());
            console.log('updateContent: content updated.');
            if (updateHistory) {
                console.log('updateContent: --> pushState({urlPrev: false}, title=', document.title, ', url=', url, ')');
                history.pushState({'urlPrev': false}, document.title, url);
            }
        }
    });
}

function initDateFields() {
    $('input.dateinput')
        .datetimepicker({'format': 'YYYY-MM-DD'})
        .on('dp.hide', function() {
            console.log('(EVENT) input.dateinput: -> dp.hide');
            $(this).blur();
        });
}

function initModal() {
    $('#content-columns').on('click', 'a.form-link', function() {
        console.log('(EVENT) a.form-link');
        var urlPrev = location.href,
            url = this.href;
        console.log('a.form-link: -> showModal(url=', url, ', urlPrev=', urlPrev, ', updateHistory=true');
        showModal(url, urlPrev, true);
        return false;
    });
}

function initTabs() {
    $('#sub-header').on('click', 'ul.nav-tabs a', function() {
        console.log('(EVENT) ul.nav-tabs a');
        var url = this.href;
        console.log('ul.nav-tabs a: -> updateContent(url=', url, ', updateHistory=true)');
        updateContent(url, true);
        return false;
    });
}

function initNavs() {
    $('#content-columns').on('click', 'a.content-link', function() {
        console.log('(EVENT) a.content-link');
        var url = this.href;
        console.log('a.content-link: -> updateContent(url=', url, ', updateHistory=true)');
        updateContent(url, true);
        return false;
    });
}

function initJournal() {
    $('#content-columns').on('click', '.day-box input[type="checkbox"]', function() {
        console.log('(EVENT) Journal');
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

function initGroupSelector() {
    $('#header').on('change', '#group-selector select', function() {
        var url = location.href;
        console.log('(EVENT) #group-selector select: <- url=', url);
        var group = $(this).val();
        if (group) {$.cookie('current_group', group, {'path': '/', 'expires': 365})}
        else {$.removeCookie('current_group', {'path': '/'})}
        console.log('#group-selector select: -> updateContent(url=', url, ', updateHistory=false');
        updateContent(url, false);
        return false;
    });
}

function initHistory() {
    window.onpopstate = function(e) {
        var url = e.target.document.URL,
            urlPrev = e.state['urlPrev'];
        console.log('(EVENT) onpopstate: <- url=', url, ', urlPrev=', urlPrev);
        if (urlPrev) {
            console.log('onpopstate: -> showModal(url=', url, ', urlPrev=', urlPrev, ', updateHistory=false');
            showModal(url, urlPrev, false);
        }
        else {
            var modal = $('#myModal');
            if (modal.hasClass('in')) {
                console.log('onpopstate: -> showModal force to close');
                modal.find('button.close').trigger('click');
            }
            else {
                console.log('onpopstate: -> updateContent(url=', url, ', updateHistory=false)');
                updateContent(url, false)
            }
        }
        return false;
    }
}

$(function() {
    initDateFields();
    initTabs();
    initNavs();
    initJournal();
    initGroupSelector();
    initModal();
    initHistory();
    history.replaceState({'urlPrev': false}, document.title, location.href);
});


//function closeModal() {
//    $('#myModal').on('hidden.bs.modal', function() {
//        console.log('createForm: CLOSE');
//        return false;
//    });
//
//}
