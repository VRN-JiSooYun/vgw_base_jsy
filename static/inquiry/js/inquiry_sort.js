function refreshInquiryPage(data) {
    var user_id = data['user_id'];
    var post = undefined;
    if (data['pagesToLoad'].includes('inquiry-post')) {
        post = data['post'][0];
        var comments = data['comments'];

        console.log(comments);

        let richText = $(".inquiry-rich-text-form").detach();
        var postStr = displayPostPanel(user_id, post, categories, comments, data['is_p'], data['is_r'], data['is_v'], data['is_d']);
        $('.inquiry-post-panel').html(postStr);
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

    // $.each(data['data'], (i, elem) => {

    //     var redOrBlue =  (elem['best_comments'] != '0') ? 'style="background-color:red;"' : '';

    //     body += `
    //         <tr class="inquiry-post inquiry-post-${elem['id']}">
    //             <th scope="row" style="text-align: center;">${data['paginator']['start_index'] + i}</th>
    //             <td style="width: 12%; text-align: center;">${elem['member_name']}</td>
    //             <td style="width: 68%;">
    //                 <a href="#" style="font-size: 15px; margin-bottom: 5px; margin-right: 5px; background-color: whitesmoke; color:black; font-weight:normal; border: solid 1px; border-color:gray;" class="badge badge-primary badge-pill">
    //                     ${elem['category_name'] == 'general' ? '일반' : elem['category_name'] == 'notice' ? '공지' : elem['category_name']}
    //                 </a>
    //                 <a href="/inquiry/inquiries/get-post-list?post=${elem['id']}" class="inquiry-post-title" post="${elem['id']}" style="color:black;">
    //                     ${typeof post !== 'undefined' && post['id'] == elem['id'] ? `<b>` : ``} ${elem['title']} ${typeof post !== 'undefined' && post['id'] == elem['id'] ? `</b>` : ``}
    //                     ${elem['comments'] > 0 ? `<span class="badge badge-primary badge-pill" ${redOrBlue}>` + elem['comments'] + `</span>`:``}
    //                 </a>
    //             </td>
    //             <td style="width:20%; text-align: center;">${elem['create_date']}</td>
    //         </tr>
    //     `;
    // });

    // $('.inquiry-post-table').html(body);
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
            console.log("data:", data);

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
