// window.onload = function () {
$('.basket_list').on('click', 'input[type="number"]', function () {
    let t_href = event.target;

    $.ajax({
        url: '/baskets/edit/' + t_href.name + '/' + t_href.value + '/',
        success: function (data) {
            $('.basket_list').html(data.result)
        },
    });
    event.preventDefault();
});


$(document).on('click', '.product_add', (e) => {

    let t_href = e.target;
    let csrf = $('meta[name="csrf-token"]').attr('content');
    let page_id = t_href.value;

    $.ajax({
        type: 'POST',
        headers: {"X-CSRFToken": csrf},
        url: '/baskets/add/' + t_href.name + '/',
        data: {'page_id': page_id},
        success: (data) => {
            if (data) {
                $('.product_items').html(data.result);
            }
        },
    });

    e.preventDefault();
});

// };
