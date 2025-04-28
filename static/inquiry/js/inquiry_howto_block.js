
function createInquiryHowtoBlock(is_d, index, elem, divToLoad, level) {
    if (divToLoad == 'cot') {
        var modificationSection = '';
        if (is_d == 1) {
            modificationSection = `
                <button class="add-how-to-slide" value="add" id="${elem['id']}" parent="${elem['parent_how_to_id']}" style="border: solid 1px; font-size:8px; margin-left:20px;">하위 영역 추가</button>
                <button class="modify-how-to-slide" index="${index}" value="modify" id="${elem['id']}" parent="${elem['parent_how_to_id']}" style="border: solid 1px; font-size:8px;">수정</button>
                <button class="delete-how-to-slide" index="${index}" value="delete" id="${elem['id']}" style="border: solid 1px; font-size:8px;">삭제</button>
                <button class="up-how-to-slide" index="${index}" id="${elem['id']}" parent="${elem['parent_how_to_id']}" style="border: solid 1px; font-size:8px;">&#11014;</button>
                <button class="down-how-to-slide" index="${index}" id="${elem['id']}" parent="${elem['parent_how_to_id']}" style="border: solid 1px; font-size:8px;">&#11015;</button>
                <button class="left-how-to-slide" index="${index}" id="${elem['id']}" parent="${elem['parent_how_to_id']}" style="border: solid 1px; font-size:8px;">&#11013;</button>
                <button class="right-how-to-slide" index="${index}" id="${elem['id']}" parent="${elem['parent_how_to_id']}" style="border: solid 1px; font-size:8px;">&#11157;</button>
            `;
        }

        return `
            <div>
                <a href="#" class="inquiry-cot-title-scroll-btn" style="font-size:16px; text-decoration: underline;" value="${index}">${elem['title']}</a>
                ${modificationSection}
            </div>
        `;
    }
    else
        return `
            <button class="inquiry-how-to-move-to-top-btn" style="float:right; margin-right:10px; margin-top:10px; border:solid 1px;">Top</button>
            <div class="inquiry-block-slide-to ${index}">
                <div><h${ level >= 6 ? 5 : level }>${elem['title']}</h${ level >= 6 ? 5 : level }></div>
                <div">${elem['content']}</div>
            </div>
            <div style="clear:both;"></div>
            <hr>
        `;
}

function createInquiryHowtoSection(is_d, howtos, divToLoad) {
    var howtosStr = document.createElement("ol");
    $(howtosStr).attr('type', '1');

    $(howtos).each((index, elem) => {

        if (elem['parent_how_to_id'] == null) {
            var level = 4;
            var subtitleStr = `<li class="howto-subtitle ${elem['id']} inquiry-${divToLoad}-li-${level}" parent="null"><div style="margin-left: -30px; padding-left: 40px; background-color:rgba(255, 255, 255, 0.65);">` + createInquiryHowtoBlock(is_d, index, elem, divToLoad, level) + '</div></li>';
            $(howtosStr).append(subtitleStr);
        }
        else {
            var level = 5;
            var parent_id = $(howtosStr).find('.howto-subtitle.' + elem['parent_how_to_id']).attr('parent');
            while (parent_id != "null" && parent_id != null) {
                level++;
                parent_id = $(howtosStr).find('.howto-subtitle.' + parent_id).attr('parent');
            }

            var subtitleStr = `<ul class="ul-howto-${divToLoad} howto-subtitle ${elem['id']}" level=${level} parent="${elem['parent_how_to_id']}"><li class="inquiry-${divToLoad}-li-${level}" style=""><div style="margin-left: -30px; padding-left: 40px; background-color:rgba(255, 255, 255, 0.65);">` + createInquiryHowtoBlock(is_d, index, elem, divToLoad, level) + '</div></li></ul>';
            $(howtosStr).find('.howto-subtitle.' + elem['parent_how_to_id']).append(subtitleStr);
        }
    });

    howtosStr = howtosStr.outerHTML;

    return howtosStr;
}