function initDateFields() {
    $('input.dateinput').datetimepicker({
        'format': 'YYYY-MM-DD'
    }).on('dp.hide', function(event) {
        $(this).blur();
    });
}

function initGroupSelector() {
    // look up select element with groups and attach our even handler
    // on field "change" event
    $('#group-selector select').change(function(event) {
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

function initJournal(){
    var err_mess = $('#ajax-error');
    var indicator = $('#ajax-progress-indicator');
    $('.day-box input[type="checkbox"]').click(function(event){
        var box = $(this);
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
                'beforeSend': function (xhr, settings) {
                    err_mess.hide();
                    indicator.show();
                },
                'error': function(xhr, status, error) {
                    indicator.hide();
                    err_mess[0].innerHTML = 'Виникла помилка збереження: ' + xhr.responseText.split('\n')[1];
                    err_mess.show();
                },
                'success': function(data, status, xhr) {
                    indicator.hide();
                }
            }
        );
    });
}

$(document).ready(function () {
    initJournal();
    initGroupSelector();
    initDateFields();
});
