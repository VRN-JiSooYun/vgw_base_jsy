// $(".inquiry-category-btn").click((e) => {
$(document).on("click", "[href*='get-post-list']:not(.inquiry-post-table-sort)", e => {
    e.preventDefault();

    var urlToRequest = $(e.target).attr('href') == null ? $(e.target).parent().attr('href') : $(e.target).attr('href');

    var val = '';

    if ($(e.target).attr('value')) val = $(e.target).attr('value');
    else val = $('.inquiry-page-value').val();

    if (urlToRequest.includes('?')) urlToRequest += '&page=' + val;
    else urlToRequest += '?page=' + val;

    var url = new URL(window.location.href);
    var on = url.searchParams.get("on");

    if (on != null) urlToRequest += '&on=' + on;
    console.log("urlToRequest:", urlToRequest);

    $.ajax({
        url: urlToRequest,
        type:'GET',
        dataType: "JSON",
        success: function (data, status) {
            console.log("data:", data);

            refreshInquiryPage(data);
        }
    });
});

$(document).on("click", "[href*='inquiries']:not([href*='get-post-list'],.inquiry-cancel-best-comment,.inquiry-comment-delete-btn,.inquiry-post-delete-btn,[href*='callPopup'])", e => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    
    console.log("$(e.target).attr('value'):" + $(e.target).attr('value'));

    console.log("prev: " + $(e.target).attr('href'));

    var url = $(e.target).attr('href') == null ? $(e.target).parent().attr('href') : $(e.target).attr('href');

    var val = '';

    if ($(e.target).attr('value')) var val = $(e.target).attr('value');
    else var val = $('.inquiry-page-value').val();
    // var val = $("[href*='inquiries']").eq(0).attr('value');

    if (url.includes('?')) url += '&page=' + val;
    else url += '?page=' + val;

    var curUrl = window.location.href;
    var url_string = new URL(curUrl);
    var post_id = url_string.searchParams.get("post");
    var category = url_string.searchParams.get("category");

    if (post_id && $(e.target).hasClass("inquiry-category-btn")) {
        url += '&category=' + $(e.target).attr('category');
        url += '&post=' + post_id;
    }
    else if (category && $(e.target).hasClass("inquiry-post-title")) {
        // url += '&post=' + $(e.target).attr('post');
        url += '&category=' + category;
    }

    console.log("url: " + url);

    window.location.href = url;

});

$(document).on("submit", ".inquiry-search-by-keyword", e => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));

    console.log("prev: " + $(e.target).attr('action'));

    var urlToRequest = $(e.target).attr('action');
    // var val = $("[href*='inquiries']").eq(0).attr('value');
    var val = $('.inquiry-page-value').val();

    if (urlToRequest.includes('?')) urlToRequest += '&page=' + val;
    else urlToRequest += '?page=' + val;

    var url = new URL(window.location.href);
    var on = url.searchParams.get("on");

    if (on != null) urlToRequest += '&on=' + on;
    console.log("urlToRequest:", urlToRequest);

    $(e.target).attr('action', urlToRequest);

    $.ajax({
        url: urlToRequest,
        type:'POST',
        dataType: "JSON",
        data: new FormData($(e.target).get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            refreshInquiryPage(data);
        }
    });

});

$(document).on("submit", "form[action*='inquiries']:not(.inquiry-search-by-keyword)", e => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    $(".loadingDiv").show();
    console.log("prev: " + $(e.target).attr('action'));

    var originUrl = window.location.href;
    var url = $(e.target).attr('action');
    // var val = $("[href*='inquiries']").eq(0).attr('value');
    var val = $('.inquiry-page-value').val();

    if (url.includes('?')) url += '&page=' + val;
    else url += '?page=' + val;

    console.log("url: " + url);

    $(e.target).attr('action', url);

    $.each($('.inquiry-comment-editor'), (i, elem) => {
        var content = $(elem).find('.ql-editor').html();
        $(elem).siblings('textarea').val(content);
    });

    $.ajax({
        url: url,
        type:'POST',
        dataType: "JSON",
        data: new FormData($(e.target).get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            var url = data.url;

            // if (data.inquiry_type != '') url += (url.includes('?') ? '&' : '?');
            if (data.pk != '') url += (url.includes('?') ? '&' : '?') + 'post=' + data.pk;
            if (data.page_name != '') url += (url.includes('?') ? '&' : '?') + 'page=' + data.page_name;
            
            console.log("received url: ", url);
            console.log("originUrl: ", originUrl);
            $(".loadingDiv").hide();

            window.location.href = url;
        }
    });

});


$('.inquiry-page-title-kor').html($('.inquiry-page-title-kor').first().html());

$(document).on('click', '.inquiry-post-modify-btn', (e) => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    $('div.inquiry-content').css('display', 'none');
    $('div.inquiry-title').css('display', 'none');
    $('.inquiry-rich-text-form-to-post').css('display', '');
    $('input.inquiry-title').css('display', '');
    $('.inquiry-category').css('display', '');
    
    $('.inquiry-post-modify-cancel-btn').css('display', '');
    $('.inquiry-post-modify-submit-btn').css('display', '');
});

$(document).on('click', '.inquiry-post-modify-cancel-btn', (e) => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    $('div.inquiry-content').css('display', '');
    $('div.inquiry-title').css('display', '');
    $('input.inquiry-title').css('display', 'none');
    $('.inquiry-category').css('display', 'none');
    $('.inquiry-rich-text-form-to-post').css('display', 'none');
    $('.inquiry-post-modify-cancel-btn').css('display', 'none');
    $('.inquiry-post-modify-submit-btn').css('display', 'none');
});

$(document).on('click', '.inquiry-comment-modify-btn', (e) => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    var clickedCommentId = $(e.target).val();

    $('.inquiry-write-reply-form').css('display', 'none');
    $('.inquiry-comment-content.' + clickedCommentId).css('display', 'none');
    // $('textarea.inquiry-comment-content.' + clickedCommentId).css('display', '');
    $('.inquiry-comment-cancel-btn.' + clickedCommentId).css('display', '');
    $('.inquiry-comment-complete-btn.' + clickedCommentId).css('display', '');
    $('.inquiry-modify-comment-form.' + clickedCommentId).css('display', '');
});

$(document).on('click', '.inquiry-comment-cancel-btn', (e) => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    var clickedCommentId = $(e.target).val();
    $('.inquiry-comment-content.' + clickedCommentId).css('display', '');
    // $('textarea.inquiry-comment-content.' + clickedCommentId).css('display', 'none');
    $('.inquiry-comment-cancel-btn.' + clickedCommentId).css('display', 'none');
    $('.inquiry-comment-complete-btn.' + clickedCommentId).css('display', 'none');
    $('.inquiry-modify-comment-form.' + clickedCommentId).css('display', 'none');
});

$(document).on('click', '.inquiry-comment-complete-btn', e => {
    // var formData = new FormData($('.inquiry-modify-comment-form').get(0));
    var clickedCommentId = $(e.target).val();
    e.preventDefault();
    console.log("clicked target:", $(e.target));

    $('.inquiry-modify-comment-form-submit.' + clickedCommentId).click();
});

$(document).on('click', '.inquiry-post-modify-submit-btn', e => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    $('.inquiry-post-title-to-modify-in-form').val($('input.inquiry-title').val());
    $('.inquiry-modify-post-form-submit').click();
});

// $("[href*='inquiries']").attr('href', $("[href*='inquiries']").eq(0).attr('href') + '&page=' + $("[href*='inquiries']").eq(0).attr('value'));
$(document).on('click', '.how-to-carousel-arrow', e => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    $('.carousel-control-' + $(e.target).attr('href')).click();
});

$(document).on('click', '.inquiry-comment-reply-btn', e => {
    e.preventDefault();
    console.log("clicked target:", $(e.target));
    var clickedCommentId = $(e.target).val();

    $('.inquiry-write-reply-form.' + clickedCommentId).css('display', '');
    $('.inquiry-comment-cancel-btn.' + clickedCommentId).css('display', 'none');
    $('.inquiry-comment-complete-btn.' + clickedCommentId).css('display', 'none');
    $('.inquiry-modify-comment-form.' + clickedCommentId).css('display', 'none');
});

$(document).on('click', '.inquiry-write-reply-cancel-btn', e => {
    e.preventDefault();
    $('.inquiry-write-reply-form').css('display', 'none');
});


function encodeImageFileAsURL() {
    var filesSelected = document.getElementsByClassName("inputFileToLoad")[0].files;
    
    if (filesSelected.length > 0) {
        var fileToLoad = filesSelected[0];

        var fileReader = new FileReader();

        fileReader.onload = function(fileLoadedEvent) {
            
            var srcData = fileLoadedEvent.target.result; // <--- data: base64

            
            var newImage = $('<img src=' + srcData + '>');
            // $(newImage).attr('src') = srcData;
            $(newImage).css('width', '100%');
            $(newImage).css('height', 'auto');

            $('.write-inquiry-post-content').append($(newImage));

            // console.log(srcData);
        }
        fileReader.readAsDataURL(fileToLoad);
    }
}

$(document).on('click', '.inquiry-comment-best-reply-btn', e => {
    e.preventDefault();

    var clickedCommentId = $(e.target).val();

    $('.inquiry-write-reply-form.' + clickedCommentId).css('display', '');
    
    $([document.documentElement, document.body]).animate({
        scrollTop: $(".inquiry-write-reply-form." + $(e.target).val()).offset().top - $(window).height()/2
    }, 500);

    $(".write-inquiry-comment-reply." + $(e.target).val()).focus();
});

$(document).on('click', '.inquiry-cancel-best-comment,.inquiry-comment-delete-btn,.inquiry-post-delete-btn', e => {
    e.preventDefault();

    if ($(e.target).attr('class') == 'inquiry-comment-delete-btn') {
        if (!confirm("해당 댓글을 삭제 하시겠습니까?")) return;
    }
    if ($(e.target).attr('class') == 'inquiry-post-delete-btn') {
        if (!confirm("현재 포스트 글을 삭제 하시겠습니까?")) return;
    }

    var url = $(e.target).attr('href');
    var val = $('.inquiry-page-value').val();

    if (url.includes('?')) url += '&page=' + val;
    else url += '?page=' + val;

    $.ajax({
        url: url,
        type:'GET',
        success: function (data, status) {

            console.log("data:", data);
    
            var url = data.url;

            // if (data.inquiry_type != '') url += (url.includes('?') ? '&' : '?');
            if (data.pk != '') url += (url.includes('?') ? '&' : '?') + 'post=' + data.pk;
            if (data.page_name != '') url += (url.includes('?') ? '&' : '?') + 'page=' + data.page_name;

            window.location.href = url;                
        }
    });
});

$(document).on('click', '.inquiry-comment-check-btn', e => {
    e.preventDefault();

    var url = $(e.target).attr('link');
    var val = $('.inquiry-page-value').val();

    if (url.includes('?')) url += '&page=' + val;
    else url += '?page=' + val;

    var comment_id = $(e.target).attr('value');
    
    $.ajax({
        url: url,
        type:'GET',
        success: function (data, status) {
            console.log("data:", data);

            if (data['best_comment'] && !confirm('이미 채택된 답변이 존재합니다. 채택 답변을 변경하시겠습니까?')) return;

            $.ajax({
                url: url = url.replace('check', 'select') + '&comment=' + comment_id,
                type:'GET',
                success: function (data, status) {
                    console.log("data:", data);
            
                    var url = data.url;

                    // if (data.inquiry_type != '') url += (url.includes('?') ? '&' : '?');
                    if (data.pk != '') url += (url.includes('?') ? '&' : '?') + 'post=' + data.pk;
                    if (data.page_name != '') url += (url.includes('?') ? '&' : '?') + 'page=' + data.page_name;

                    window.location.href = url;
                }
            });
        }
    });
});