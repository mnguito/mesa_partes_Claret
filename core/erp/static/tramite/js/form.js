var user = {
    items: {
        first_name: '',
        last_name: '',
        email: '',
        rol: '',
        document_number: ''
    }
};

$(function () {

    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es',
    });

    // event submit
    $('#frmSale').on('submit', function (e) {
        e.preventDefault();

        user.items.first_name = $('input[name="first_name"]').val();
        user.items.last_name = $('input[name="last_name"]').val();
        user.items.email = $('input[name="email"]').val();
        user.items.document_number = $('input[name="document_number"]').val();
        user.items.rol = $('select[name="rol"]').val();

        // if (user.items.products.length === 0) {
        //     message_error('Debe al menos tener un item en su detalle de alquiler');
        //     return false;
        // }
        let parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('user', JSON.stringify(user.items));
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de realizar la siguiente acción?', parameters, function (response) {
                location.href = '/user/list/';
            });
    });

});

