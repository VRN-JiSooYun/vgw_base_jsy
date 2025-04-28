function refreshInquiryPage(data) {
    var user_id = data['user_id'];
    var post = undefined;
    if (data['pagesToLoad'].includes('inquiry-post')) {
        post = data['post'][0];
        var comments = data['comments'];

        // console.log(comments);
        console.log("refreshInquiryPage:", data);

        let richText = $(".inquiry-rich-text-form").detach();
        // var postStr = displayPostPanel(user_id, post, categories, comments, data['is_p'], data['is_r'], data['is_v'], data['is_d']);
        // $('.inquiry-post-panel').html(postStr);

        console.log("post.member_id:", post.member_id);
        console.log("user_id:", user_id);

        if (data['is_r'] || data['is_v'] || data['is_d'] || post.check_hide == 0 || (post.check_hide == 1 && post.member_id == user_id)) $('.inquiry-post-panel').html(displayPostPanel(user_id, post, categories, comments, data['is_p'], data['is_r'], data['is_v'], data['is_d']));
        else $('.inquiry-post-panel').html(`
            <div style="position:absolute; width:95%; height:90%;">
                <div style="margin: auto; width: 200px; height: 200px;">
                    비공개 게시글입니다.
                </div>
            </div>
        `);

        $(richText).appendTo(".inquiry-rich-text-form-to-post");
        $('.ql-editor').html(post['content']);
        $('.ql-blank').css('min-height', '500px');

        $(".inquiry-post-panel").css('display', '');
        $(".inquiry-post-form-panel").css('display', 'none');

        createQuillEditor('write-inquiry-post-comment');

        for (var i = 0; i < comments.length; i++) {
            createQuillEditor('inquiry-comment-editor' + comments[i]['id']);
            createQuillEditor('inquiry-comment-modify-editor' + comments[i]['id']);
            $('.inquiry-comment-modify-editor' + comments[i]['id'] + ' .ql-editor').html(comments[i]['content']);
        }

    }
    else if (data['pagesToLoad'].includes('inquiry-post-form')) {
        var categories = data['categories'];

        $(".inquiry-post-form-panel").css('display', '');
        $(".inquiry-post-panel").css('display', 'none');
        $(".inquiry-rich-text-form").detach().appendTo(".inquiry-rich-text-form-to-post-form");
        $('.ql-editor').html('');
        $('.ql-blank').css('min-height', '500px');
    }

    var body = "";

    console.log('post:', post);

    displayInquiryPostList(data, post);
}

$('.inquiry-post-table-sort').click((e) => {
    e.preventDefault();

    var name = $(e.target).attr('value');
    var toggle = parseInt($(e.target).attr('toggle'));
    $(e.target).attr('toggle', toggle * -1);

    var urlToRequest = $(e.target).attr('href') == null ? $(e.target).parent().attr('href') : $(e.target).attr('href');

    var url = new URL(window.location.href);
    var on = url.searchParams.get("on");
    var page = url.searchParams.get("page");

    if (page != null) urlToRequest += '?page=' + page;
    if (on != null) urlToRequest += '&on=' + on;

    urlToRequest += '&order_by=' + (toggle == 1 ? '' : '-') + name;

    console.log("urlToRequest:", urlToRequest);

    $.ajax({
        url: urlToRequest,
        type:'GET',
        dataType: "JSON",
        success: function (data, status) {
            console.log("data6:", data);

            refreshInquiryPage(data);
        }
    });
});

$(document).on("click", ".inquiry-comments-sorting-btn", e => {

    var toggle = $(e.target).attr('toggle');
    $(e.target).attr('toggle', toggle * -1);

    let ulList = $('.ul-inquiry-parent-comment');

    var sortList = Array.prototype.sort.bind(ulList);

    sortList(( a, b ) => {

        var aText = $(a).attr('value');
        var bText = $(b).attr('value');
    
        if ( aText < bText ) {
            return -1 * toggle;
        }

        if ( aText > bText ) {
            return 1 * toggle;
        }

        return 0;
    });

    $('.inquiry-post-comment-list-section').append(ulList);
});
