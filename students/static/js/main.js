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
});
