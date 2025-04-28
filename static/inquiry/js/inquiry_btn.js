function getCommentStr(csrftoken, user_id, postElem, CommentElem, marginLeft, isBest, index) {

    var replyAndSelect = '';

    //================================================================================================================
    // Best Comment
    //================================================================================================================
    if (isBest) {
        replyAndSelect = `
            <button class="inquiry-comment-best-reply-btn" value="${ CommentElem['id'] }" style="float:left; margin-left:-5px; font-size: 14px; color:silver; border: none; background-color:transparent;">대댓글 쓰기</button>
            ${ postElem['member_id'] == user_id
                ? `<a class="inquiry-cancel-best-comment" href="/inquiry/inquiries/cancel-best-comment?post=${ postElem['id'] }&comment=${ CommentElem['id'] }" style="float:left; margin-left:10px; font-size: 14px; color:silver;">채택 취소</a>`
                : ''
            }
            <div style="clear: both;"></div>
        `;
    }
    //================================================================================================================
    // 대댓글 쓰기 & 채택 하기
    //================================================================================================================
    else {
        replyAndSelect = `
            <button class="inquiry-comment-reply-btn" value="${ CommentElem['id'] }" style="float:left; margin-left:10px; font-size: 14px; color:silver; border: none; background-color:white;">대댓글 쓰기</button>
            ${ postElem['member_id'] == user_id
                ? `<button class="inquiry-comment-check-btn" link="/inquiry/inquiries/check-best-comment?post=${ postElem['id'] }" value="${ CommentElem['id'] }" style="float:left; margin-left:10px; font-size: 14px; color:silver; border: none; background-color:white;">채택 하기</button>`
                : ''
            }
            <div style="clear: both;"></div>
            <form method="POST" action="/inquiry/inquiries/write-reply" class="inquiry-write-reply-form ${ CommentElem['id'] }" style="display:none;">
                <input type="text" name="csrfmiddlewaretoken" value="${ csrftoken }" style="display:none;">
                <textarea rows="5" name="write-inquiry-comment-reply" style="display:none;"></textarea>
                <div class="inquiry-comment-editor inquiry-comment-editor${ CommentElem['id'] }"></div>
                <input type="text" name="inquiry-post-id" value="${ postElem['id'] }" style="display:none;">
                <input type="text" name="inquiry-parent-comment-id" value="${ CommentElem['id'] }" style="display:none;">
                <button class="inquiry-write-reply-cancel-btn" value="${ CommentElem['id'] }" style="float: right; margin-right:10px;">취소</button>
                <button style="float: right; margin-right:10px;">완료</button>
            </form>
            <div style="clear: both;"></div>
            <hr>
        `;
    }

    //================================================================================================================
    // comment content
    //================================================================================================================
    return `
        <div style="margin:8px; margin-left:${marginLeft}px; background-color:rgba(255, 255, 255, 0.9); border-left: rgba(255, 255, 255, 0.75) solid 8px; border-top: rgba(255, 255, 255, 0.75) solid 8px; border-right: rgba(255, 255, 255, 0.9) solid 8px">
            <div>
                <div>
                    <b>${ CommentElem['member_name'] }</b>
                    <span style="float: right; display: inline-block; text-align:center;">${ CommentElem['create_date'] }</span>
                    ${ CommentElem['member_id'] == user_id && !isBest
                        ? `<button class="inquiry-comment-delete-btn" href="/inquiry/inquiries/delete-comment?post=${ postElem['id'] }&comment=${ CommentElem['id'] }" style="float: right; border: solid 1px; margin-right:10px; font-size: 14px;">Delete</button>`
                        + `<button class="inquiry-comment-modify-btn" value="${ CommentElem['id'] }" style="float: right; margin-right:10px; font-size: 14px; border: solid 1px;">Modify</button>`
                        : ''
                    }
                </div>
                <div style="clear:both;"></div>
                <div class="inquiry-comment-content ${ CommentElem['id'] }" style="margin: 10px; width: 97%; overflow:scroll;">${ CommentElem['content'] }</div>
                <form class="inquiry-modify-comment-form ${ CommentElem['id'] }" method="POST" action="/inquiry/inquiries/modify-comment" style="display:none;">
                    <input type="text" name="csrfmiddlewaretoken" value="${ csrftoken }" style="display:none;">
                    <input type="text" name="inquiry-post-id" value="${ postElem['id'] }" style="display:none;">
                    <input type="text" name="inquiry-comment-id" value="${ CommentElem['id'] }" style="display:none;">
                    <textarea name="inquiry-comment-content" style="width:97%; margin:15px; display:none;" rows="8"></textarea>
                    <div class="inquiry-comment-editor inquiry-comment-modify-editor${ CommentElem['id'] }"></div>
                    <button class="inquiry-modify-comment-form-submit ${ CommentElem['id'] }" style="display:none;"></button>
                </form>
            </div>
            <button class="inquiry-comment-cancel-btn ${ CommentElem['id'] }" value="${ CommentElem['id'] }" style="float: right; font-size: 14px; display:none;">Cancel</button>
            <button class="inquiry-comment-complete-btn ${ CommentElem['id'] }" value="${ CommentElem['id'] }" style="float: right; margin-right:10px; font-size: 14px; display:none;">Complete</button>
            <div style="clear:both;"></div>
            ${ replyAndSelect }
        </div>
    `;
}

function displayPostPanel(user_id, inquiry_post, categories, comments, is_p, is_r, is_v, is_d) {

    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    var categoriesStr = '';
    // var commentsStr = '<ul>';
    var commentsStr = document.createElement("div");
    var bestCommentSection = '';
    var bestCommentStr = '';

    $.each(categories, (i, elem) => {
        if (elem['category'] != 'general' && elem['category'] != 'notice') {
            categoriesStr += `<option value="${ elem['category'] }" ${ elem['category_name'] == elem['category'] ? 'selected' : ''} >${ elem['category'] }</option>`
        }
    });

    $.each(comments, (i, elem) => {
        //================================================================================================================
        // Best Comment
        //================================================================================================================
        if (elem['check_best_comment'] == true) {

            bestCommentStr = getCommentStr(csrftoken, user_id, inquiry_post, elem, 0, true, i);

            bestCommentSection = `
                <div class="row" style="background-color:honeydew;">
                    <div class="col-sm-1"><div style="margin-left:15px;"><b style="color:green; font-size:30px;">&#10003;</b><br><i>Best<br>답변</i></div></div>
                    <div class="col-sm-11">
                        ${ bestCommentStr }
                    </div>
                </div>
                <div style="clear:both;"></div>
                <button class="inquiry-comments-sorting-btn" style="width:100px; margin: 0 auto; border: solid 1px; margin-top:8px; border-color:grey;" toggle=-1>댓글 시간순 정렬</button>
                <hr style="margin-top:8px;">
            `;
        }

        //================================================================================================================
        // Comments
        //================================================================================================================
        // parent comment
        if (elem['parent_comment_id'] == null) {
            var replyStr = `<ul class="ul-inquiry-parent-comment reply ${elem['id']}" value="${elem['create_date']}" style="padding:0;">` + getCommentStr(csrftoken, user_id, inquiry_post, elem, 10, false, i) + '</ul>';
            $(commentsStr).append(replyStr);
        }
        // child reply
        else {
            var replyPrefix = `<div style="float:left;"><span style='font-size:20px; color:silver;'>&#8627;</span></div>`;
            var replyStr = `<ul class="reply ${elem['id']}">` + replyPrefix + getCommentStr(csrftoken, user_id, inquiry_post, elem, 28, false, i) + '</ul>';
            $(commentsStr).find('.reply.' + elem['parent_comment_id']).append(replyStr);
        }
    });

    commentsStr = commentsStr.outerHTML;

    var noticeOptionStr = '';

    if (is_d) noticeOptionStr = `<option value="notice" ${ inquiry_post['category_name'] == 'notice' ? 'selected' : ''}> 공지 </option>`;

    return `
        <div>
            <div>
                질문과 답변
                <a href="/inquiry/inquiries" style="float:right;"><button class="inquiry-question-btn" style="border: solid 1px gray;">&#9999;&nbsp;&nbsp;글쓰기</button></a>
            </div>
            <hr>
            <div class="inquiry-title">
                <div style="float:left; font-size:22px;"><b>[${ inquiry_post['category_name'] == 'general' ? '일반' : inquiry_post['category_name'] == 'notice'? '공지' : inquiry_post['category_name']}] ${ inquiry_post['title'] }</b></div>
                <div style="float:right;">${ inquiry_post['create_date'] }&nbsp;&nbsp;&nbsp;</div>
                <div style="float:right;">${ inquiry_post['member_name'] }&nbsp;&nbsp;&nbsp;</div>
            </div>
            <div style="clear:both;"></div>
            <input class="inquiry-title" style="width:100%; display:none;" value="${ inquiry_post['title'] }">
            <hr>
            <form class="inquiry-modify-post-content-form" method="POST" action="/inquiry/inquiries/modify-question" style="width:100%;">
                <input type="text" name="csrfmiddlewaretoken" value="${ csrftoken }" style="display:none;">
                <select name="inquiry-category" class="inquiry-category" style="display: none;">
                    <option value="general" ${ inquiry_post['category_name'] == 'general' ? 'selected' : ''}> 일반 </option>
                    ${ noticeOptionStr }
                    ${ categoriesStr }
                </select>
                <div class="inquiry-content" style="width: 100%; padding-bottom: 150px; padding-left:15px; padding-right:15px; border:solid 2px gainsboro; overflow-x: scroll; background-color:rgba(255, 255, 255, 0.9);">${ inquiry_post['content'] }</div>
                <input type="text" name="write-inquiry-post-title-to-modify" value="" class="inquiry-post-title-to-modify-in-form" style="display:none;">
                <input type="text" name="inquiry-post-id" value="${ inquiry_post['id'] }"  style="display:none;">
                
                <div class="inquiry-rich-text-form-to-post inquiry-content" style="background-color:rgba(255, 255, 255, 0.75); display:none;"></div>
                <button class="inquiry-modify-post-form-submit" style="display: none;"></button>
            </form>
            <button class="inquiry-post-modify-cancel-btn" style="float: right; font-size: 14px; display: none;">취소</button>
            <button class="inquiry-post-modify-submit-btn" style="float: right; margin-right:10px; font-size: 14px; display: none;">완료</button>
            <div style="clear:both;"></div>
            <hr>
            <div class="inquiry-post-best-comment-section">
                ${ bestCommentSection }
            </div>
            <div class="inquiry-post-comment-list-section">
                ${ commentsStr }
            </div>
            <div style="margin:20px;">
                <form method="POST" action="/inquiry/inquiries/write-comment">
                    <input type="text" name="csrfmiddlewaretoken" value="${ csrftoken }" style="display:none;">
                    <div><b>댓글 달기:</b></div>
                    <textarea name="write-inquiry-post-comment" style="display:none;"></textarea>
                    <div class="write-inquiry-post-comment inquiry-comment-editor" style="background-color:white;"></div>
                    <input type="text" name="inquiry-post-id" value="${ inquiry_post['id'] }" style="display:none;">
                    <button style="float: right;">완료 <span style="font-size: 12px;">&#11093;</span></button>
                </form>
                <div style="clear: both;"></div>
            </div>
            <hr>
            <div>
                <a href="/inquiry/inquiries"><button class="inquiry-post-to-list-btn" style="float: left;">&#127757;&nbsp;&nbsp;목록</button></a>
                <button class="inquiry-post-delete-btn" href="/inquiry/inquiries/delete-post?post=${ inquiry_post['id'] }" style="float: right;">글 삭제 <span style="font-size: 12px;">&#10060;</span></button>
                <button class="inquiry-post-modify-btn" style="float: right; margin-right:10px;">글 수정&nbsp;&#9999;</i></button>
            </div>
        </div>
    `;
}