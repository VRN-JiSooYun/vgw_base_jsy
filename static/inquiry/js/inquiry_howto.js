// $('.inquiry-add-visualization-btn').click(e => {
$(document).on('click', '.inquiry-add-visualization-btn', e => {
    e.preventDefault();
    console.log('inquiry-add-visualization-btn');
    $('.inquiry-add-description-section').css('display', 'none');
    $('.inquiry-add-description-input').val('');

    $('.inquiry-add-description-' + $(e.target).attr('value') + '-section').css('display', '');
    $('#inquiry-description-' + $(e.target).attr('value')).prop('required', true);
    
});

$(document).on('click', '.add-how-to-slide', e => {
    e.preventDefault();
    console.log('add-how-to-slide');
    $('.inquiry-slide-form-action').val($(e.target).attr('value'));
    $('.inquiry-slide-id').val($(e.target).attr('id'));
    $('.inquiry-slide-parent-id').val($(e.target).attr('parent'));
    $('.inquiry-slide-form').css('display', '');
    window.scrollTo(0, 0);
});

$(document).on('click', '.modify-how-to-slide', e => {
    e.preventDefault();
    console.log('add-how-to-slide');
    $('.inquiry-slide-form-action').val($(e.target).attr('value'));
    $('.inquiry-slide-id').val($(e.target).attr('id'));
    $('.inquiry-slide-parent-id').val($(e.target).attr('parent'));
    $('.inquiry-slide-form').css('display', '');

    var clickedId = $(e.target).attr('index');

    var clickedTitle = how_tos[clickedId]['title'];
    var clickedContent = how_tos[clickedId]['content'];
    $('.inquiry-slide-title-input').val(clickedTitle);
    $('.ql-editor').html(clickedContent);
    window.scrollTo(0, 0);
});

$(document).on('click', '.inquiry-slide-form-cancel-btn', e => {
    e.preventDefault();
    $('.inquiry-slide-form-action').val('');
    $('.inquiry-slide-form').css('display', 'none');

    $('.inquiry-slide-title-input').val('');
    $('.ql-editor').html('');
});

$(document).on('click', '.delete-how-to-slide,.reset-how-to-slides', e => {
// $('.delete-how-to-slide,.reset-how-to-slides').click(e => {
    e.preventDefault();
    var actionToRequest = $(e.target).attr('value');
    console.log("actionToRequest:", actionToRequest === "reset");
    if (actionToRequest === "delete") {
        if (!confirm('현재 선택된 슬라이드와 부연설명를 삭제합니다.')) return;
    }
    else if (actionToRequest === "reset"){
        if (!confirm('이 페이지에 대한 모든 슬라이드와 부연설명를 삭제합니다.')) return;
    }
    var url_string = new URL(window.location.href);
    var page = url_string.searchParams.get("page");
    var slideIndex = $(e.target).attr('id');
    var urlToRequest = '/inquiry/inquiries/' + actionToRequest + '-how-to-use?page=' + page + '&slide=' + slideIndex;;

    console.log('urlToRequest:' + urlToRequest);

    $.ajax({
        url: urlToRequest,
        type:'GET',
        dataType: "JSON",
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            location.reload();
        }
    });
})

$(document).on('submit', '.inquiry-slide-form', e => {
// $('.inquiry-slide-form').submit(e => {
    e.preventDefault();

    var actionToRequest = $('.inquiry-slide-form-action').val();
    var url_string = new URL(window.location.href);
    var page = url_string.searchParams.get("page");
    
    var slideIndex = $('.inquiry-slide-id').val();
    var parentSlideIndex = $('.inquiry-slide-parent-id').val();
    var urlToRequest = '/inquiry/inquiries/' + actionToRequest + '-how-to-use?page=' + page + '&slide=' + slideIndex + '&parent=' + parentSlideIndex;

    console.log('urlToRequest:' + urlToRequest);

    $.ajax({
        url: urlToRequest,
        type:'POST',
        dataType: "JSON",
        data: new FormData($(e.target).get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            location.reload();
        }
    });
});

$(document).on('click', '.up-how-to-slide', e => {
    var clickedIndex = $(e.target).attr('index');
    var clickedSlideId = $(e.target).attr('id');
    var parentSlideId = $(e.target).attr('parent');

    if (clickedIndex - 1 < 0 || how_tos[clickedIndex]['parent_how_to_id'] != how_tos[clickedIndex - 1]['parent_how_to_id']) return;

    var temp = how_tos[clickedIndex];
    how_tos[clickedIndex] = how_tos[clickedIndex - 1];
    how_tos[clickedIndex - 1] = temp;

    $('.inquiry-howto-cot-div').html(createInquiryHowtoSection(is_d, how_tos, 'cot'));
});

$(document).on('click', '.down-how-to-slide', e => {
    var clickedIndex = parseInt($(e.target).attr('index'));
    var clickedSlideId = $(e.target).attr('id');
    var parentSlideId = $(e.target).attr('parent');

    if (clickedIndex + 1 >= how_tos.length || how_tos[clickedIndex]['parent_how_to_id'] != how_tos[clickedIndex + 1]['parent_how_to_id']) return;

    var temp = how_tos[clickedIndex];
    how_tos[clickedIndex] = how_tos[clickedIndex + 1];
    how_tos[clickedIndex + 1] = temp;

    $('.inquiry-howto-cot-div').html(createInquiryHowtoSection(is_d, how_tos, 'cot'));
});

$(document).on('click', '.left-how-to-slide', e => {
    var clickedIndex = $(e.target).attr('index');
    var clickedSlideId = $(e.target).attr('id');
    var parentSlideId = $(e.target).attr('parent');
    
    for(var i = clickedIndex; i - 1 >= 0; i--) {
        if (how_tos[i - 1]['parent_how_to_id'] != how_tos[clickedIndex]['parent_how_to_id']) {
            how_tos[clickedIndex]['parent_how_to_id'] = how_tos[i - 1]['parent_how_to_id'];
            break;
        }
    }

    how_tos.sort( compare );

    $('.inquiry-howto-cot-div').html(createInquiryHowtoSection(is_d, how_tos, 'cot'));

});

$(document).on('click', '.right-how-to-slide', e => {
    var clickedIndex = $(e.target).attr('index');
    var clickedSlideId = $(e.target).attr('id');
    var parentSlideId = $(e.target).attr('parent');

    if (clickedIndex - 1 < 0 || how_tos[clickedIndex]['parent_how_to_id'] != how_tos[clickedIndex - 1]['parent_how_to_id']) return;

    how_tos[clickedIndex]['parent_how_to_id'] = how_tos[clickedIndex - 1]['id'];

    how_tos.sort( compare );

    for (var a = 0; a < how_tos.length; a++) {
        for (var i = 0; i < how_tos.length; i++) {
            if (how_tos[i]['parent_how_to_id'] == null) continue;
            var p = false;
            for (var j = 0; j < i; j++) if (how_tos[i]['parent_how_to_id'] == how_tos[j]['id']) p = true;
            if (!p) how_tos.splice(i + 1, 0, how_tos.splice(i, 1)[0]);
        }
    }

    $('.inquiry-howto-cot-div').html(createInquiryHowtoSection(is_d, how_tos, 'cot'));

});

function compare( a, b ) {
    if ( a['parent_how_to_id'] < b['parent_how_to_id'] ) return -1;
    if ( a['parent_how_to_id'] > b['parent_how_to_id'] ) return 1;

    return 0;
};

$(document).on('click', '.inquiry-howto-modified-cot-save-btn', e => {
    e.preventDefault();

    var idList = [];
    var parentList = [];
    var sortingIndexList = [];

    $(how_tos).each((i, elem) => {
        idList.push(elem['id']);
        parentList.push(elem['parent_how_to_id']);
        sortingIndexList.push(i);
    });

    var actionToRequest = $('.inquiry-slide-form-action').val();
    var url_string = new URL(window.location.href);
    var page = url_string.searchParams.get("page"); 

    var urlToRequest = '/inquiry/inquiries/sort-how-to-use?page=' + page;

    console.log('urlToRequest:' + urlToRequest);

    var cookie = getCookie("csrftoken");
    console.log('cookie:', cookie);

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                // xhr.setRequestHeader("X-CSRFToken", csrftoken);
                xhr.setRequestHeader("X-CSRFToken", cookie);
            }
        }
    });

    $.ajax({
        url: urlToRequest,
        type:'POST',
        dataType: "JSON",
        data: {
            'id-list': JSON.stringify(idList),
            'parent-list': JSON.stringify(parentList),
            'sorting-index-list': JSON.stringify(sortingIndexList)
        },
        success: function (data, status) {
            console.log("data:", data);

            // $('.inquiry-slide-form').css('display', 'none');
            // $('.inquiry-slide-form-action').val('');
            location.reload();
        }
    });
});

$(document).on('click', '.inquiry-cot-title-scroll-btn', e => {
    e.preventDefault();
    $([document.documentElement, document.body]).animate({
        scrollTop: $(".inquiry-block-slide-to." + $(e.target).attr('value')).offset().top
    }, 500);
});


$(document).on('click', '.inquiry-how-to-move-to-top-btn', e => {
    e.preventDefault();
    window.scrollTo(0, 0);
});