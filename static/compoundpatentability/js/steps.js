const colorStepOn = "rgb(127, 98, 255)";
const colorStepOff = "rgb(196, 217, 253)";

// function imgClicked(e, img){
//     e.stopPropagation();

//     var modal = document.getElementById("myModal");
//     var modalImg = document.getElementById("img01");
//     var captionText = document.getElementById("caption");
//     modal.style.display = "block";
//     modalImg.src = img.src;
//     captionText.innerHTML = img.alt;
// }

// function closeClicked() { 
//     var modal = document.getElementById("myModal");
//     modal.style.display = "none";
// }

//========================================================================================================================================
//========================================================================================================================================
// step1
//========================================================================================================================================
//========================================================================================================================================
// $('.patent-registration-form').submit((e) => {
$('.patent-registration-form').on('change', (e) => {
    e.preventDefault();

    var formData = new FormData($('.patent-registration-form').get(0));

    for (var pair of formData.entries()) {
        console.log(pair[0], pair[1]);
        if (pair[0] == 'patent_file') {
            if (pair[1]['name'] == '') {
                return;
            }
            else {
                console.log('file attached');
                var stack = pair[1]['name'].split('.');
                var fileExt = stack.pop();
                var fileName = stack.pop();

                if (fileExt != 'pdf') {
                    window.alert(".pdf 형식의 파일을 업로드해주시길 바랍니다.");
                    return;
                }
                else {
                    var alt = $('.patent-registration-confirm-img').prop('alt');
                    console.log("fileName: ", fileName);
                    console.log("alt: ", alt);
                    if (alt != fileName) {
                        $('.patent-registration-confirm-img').prop('alt', fileName);
                        $('.registration-loader-wrapper').css('display', 'flex');
                        $('.registration-loader').addClass('loader');
                    }
                }
            }
        }
    }

    $.ajax({
        url: '/compoundpatentability/register-patent',
        type:'POST',
        dataType: "JSON",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            $('.patent-registration-confirm-img').attr('src', 'data:image/png;base64, ' + data['image'])
            $('.patent-registration-btn').css('display', 'none');
            $('.patent-registration-confirm-td').css('display', 'block');

            $('.registration-loader-wrapper').css('display', 'none');
            $('.registration-loader').removeClass('loader');
        }
    }); 
});

$('.patent-registration-confirm-yes').click((e) => {
    e.preventDefault();

    var inputId = $('.patent-registration-input-id').val();
    var inputTile = $('.patent-registration-input-title').val();
    var inputOrg = $('.patent-registration-input-organization').val();

    var inputRegion = $('.patent-registration-input-region').is(':checked');

    if (inputId == '') { alert('특허의 ID를 입력해주세요.'); return; }
    if (inputTile == '') { alert('특허의 제목을 입력해주세요.'); return; }
    if (inputOrg == '') { alert('기관을 입력해주세요.'); return; }
    if (!inputRegion) { alert('지역을 입력해주세요.'); return; }

    $.ajax({
        url: '/compoundpatentability/confirm-register-patent',
        type:'POST',
        dataType: "JSON",
        data: new FormData($('.patent-registration-form').get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            
            $('.patent-registration-step-1').css('background-color', colorStepOff);
            $('.patent-registration-step-1-after').css('background-color', colorStepOff);
            $('.patent-registration-step-2-before').css('background-color', colorStepOff);
            $('.patent-registration-step-1').css('color', 'white');
            $('.patent-registration-step-2').css('background-color', colorStepOn);
            $('.patent-registration-page-1').css('display', 'none');
            $('.patent-registration-page-2').css('display', "");

        }
    });
});

$('.patent-registration-confirm-no').click((e) => {
    e.preventDefault();

    $('.patent-registration-confirm-img').attr('src', '/static/images/logo.png')
    $('.patent-registration-confirm-img').prop('alt', 'logo');
    $('.patent-registration-btn').css('display', '""');
    $('.patent-registration-confirm-td').css('display', 'none');
});

//========================================================================================================================================
//========================================================================================================================================
// step2
//========================================================================================================================================
//========================================================================================================================================
$('.register-embodiment-by-one-btn').click(function(e) {
    e.preventDefault();

    $.ajax({
        url: '/compoundpatentability/add-embodiment',
        type:'POST',
        dataType: "JSON",
        data: new FormData($('.form-upload-embodiment').get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            if (data['operation'] == 'failed') {
                $('.embodiment-registration-result-message').html('Invalid Smiles');
                $('.embodiment-registration-result-message').css('color', 'red');
                return;
            }
            else {
                $('.embodiment-registration-result-message').html('성공적으로 등록되었습니다.');
                $('.embodiment-registration-result-message').css('color', 'green');
            }

            var elem = data['data'];

            var body = `
                <tr class="embodiment embodiment-row embodiment-row-${elem['pk']}">
                    <td style="vertical-align: middle;">
                        <input class="embodiment-checkbox" type="checkbox" name="embodiment-checkbox" value="${elem['pk']}">
                        ${i}
                    </td>
                    <td style="vertical-align: middle; text-align:center;">
                        <div style="width:80px; display: block; margin: 0 auto;">
                            ${elem['image']}
                        </div>
                    </td>
                    <td style="vertical-align: middle; width: 100%; word-wrap: break-word; word-break: break-all; text-align:left; font-size: 13px;">
                        ${elem['smiles']}
                    </td>
                </tr>
            `;

            $('.embodiment-list-table').append(body);
        }
    });
});

// $('.form-upload-embodiments').submit(function(e) {
$('.embodiments-file-input').on('change', (e) => {
    e.preventDefault();

    var formData = new FormData($('.form-upload-embodiments').get(0));

    for (var pair of formData.entries()) {
        console.log(pair[0], pair[1]);
        if (pair[0] == 'document') {
            if (pair[1]['name'] == '') {
                return;
            }
            else {
                console.log('file attached');
                var fileExt = pair[1]['name'].split('.').pop();
                if (fileExt != 'csv' && fileExt != 'xlsx') {
                    alert(".csv 이나 .xlsx 형식의 파일을 업로드해주시길 바랍니다.");
                    return;
                }
            }
        }
    }

    if (confirm("해당 파일을 업로드 하시겠습니까?") == false) {
        $('.form-upload-embodiments').trigger("reset");
        return;
    }

    $('.registration-loader-wrapper').css('display', 'flex');
    $('.registration-loader').addClass('loader');

    $.ajax({
        url: '/compoundpatentability/add-embodiments',
        type:'POST',
        dataType: "JSON",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            var arr = data['data'];

            var body = "";
            
            $.each(arr, (i, elem) => {
                body += `
                    <tr class="embodiment embodiment-row embodiment-row-${elem['pk']}">
                        <td style="vertical-align: middle;">
                            <input class="embodiment-checkbox" type="checkbox" name="embodiment-checkbox" value=${elem['pk']}>
                            ${i}
                        </td>
                        <td style="vertical-align: middle; text-align:center;">
                            <div style="width:80px; display: block; margin: 0 auto;">
                                ${elem['image']}
                            </div>
                        </td>
                        <td style="vertical-align: middle; width: 100%; word-wrap: break-word; word-break: break-all; text-align:left; font-size: 13px;">
                            ${elem['smiles']}
                        </td>
                    </tr>
                `;
            });

            $('.embodiment-list-table').append(body);
            $('.registration-loader-wrapper').css('display', 'none');
            $('.registration-loader').removeClass('loader');
        }
    });
});

$(".checkbox-embodiment-select-all").change(function() {
    if (this.checked) {
        $('.embodiment-checkbox').prop('checked', true);
    }
    else {
        $('.embodiment-checkbox').prop('checked', false);
    }
});

$('.delete-embodiment-btn').click((e) => {
    e.preventDefault();

    var formData = new FormData($('.embodiment-list-form').get(0));

    $.ajax({
        url: '/compoundpatentability/remove-embodiments',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            if (data["operation"] == "success") {
                for (var pair of formData.entries()) {
                    if (pair[0] == "embodiment-checkbox") {
                        console.log('.embodiment-row-' + pair[1]);
                        $('.embodiment-row-' + pair[1]).remove();
                    }
                }
            }
        }
    });
});

$('.patent-embodiment-next-btn').click((e) => {
    e.preventDefault();

    $.ajax({
        url: '/compoundpatentability/complete-embodiment',
        type: 'GET',
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            $('.patent-registration-step-2').css('background-color', colorStepOff);
            $('.patent-registration-step-2-after').css('background-color', colorStepOff);
            $('.patent-registration-step-3-before').css('background-color', colorStepOff);
            $('.patent-registration-step-2').css('color', 'white');
            $('.patent-registration-step-3').css('background-color', colorStepOn);
            $('.patent-registration-page-2').css('display', 'none');
            $('.patent-registration-page-3').css('display', "");
        }
    });
});

//========================================================================================================================================
//========================================================================================================================================
// step4
//========================================================================================================================================
//========================================================================================================================================
$('.patent-markush-r-weight-registration,.patent-markush-core-weight-registration').submit((e) => {
    e.preventDefault();
    var className = '';
    if ($(e.target).hasClass('patent-markush-r-weight-registration')) {
        className = 'r';
    }
    else if ($(e.target).hasClass('patent-markush-core-weight-registration')) {
        className = 'core';
    }
    console.log("className:", className);

    var formData = new FormData($('.patent-markush-' + className + '-weight-registration').get(0))

    var sum = 0;
    for (var pair of formData.entries()) {
        console.log(pair[0], pair[1]);
        if (pair[0].includes('R') || pair[0].includes('markush')) {
            if (!isNaN(pair[1])) {
                sum += Number(pair[1]);
            }
        }
    }

    console.log("sum:", sum);

    if (sum != 100.0) {
        $('.' + className + '-weight-warning').html('입력된 전체 가중치의 합이 100이어야만 합니다.');
        $('.' + className + '-weight-warning').css('color', 'red');
        return;
    }

    $.ajax({
        url: '/compoundpatentability/add-weights-' + className,
        type: 'POST',
        dataType: "JSON",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            $('.' + className + '-weight-warning').html('업데이트가 완료되었습니다.');
            $('.' + className + '-weight-warning').css('color', 'black');
        }
    });
});

$('.complete-patent-markush-core-weight-registration').submit((e) => {
    e.preventDefault();

    $.ajax({
        url: '/compoundpatentability/check-weights',
        type: 'POST',
        dataType: "JSON",
        data: new FormData($(e.target).get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            if (data["operation"] == "success") {
                console.log("redirect");
                window.location.href = "/compoundpatentability/complete-patent-registration-process";
            }
        }
    });
});