// const evaluatePatentabilityMarvin = ChemicalizeMarvinJs.createEditor("#evaluate-patentability-marvin").then((marvin) => {
//     marvin.on("molchange", val => {
//         marvin.exportStructure("smiles").then(function (smiles) {
//             document.getElementById("evaluate-patentability-marvin-smiles").value = smiles;
//         });
//     });

//     $("#evaluate-patentability-marvin-input").click(e => {
//         e.preventDefault();
//         let smiles = document.getElementById("evaluate-patentability-marvin-smiles").value;
//         marvin.importStructure(null, smiles);
//     })
// });

$('.upload-excel-help-btn').click((e) => {
    $(".image-background-to-popup").css('display', 'block');
    var img = `<img style="width:100%;" src='/static/images/compound_form_sample.png'>`;
    $('.popup-image-modal-content').html(img);
    $('.popup-image-model-caption').prop('alt', '');
});

$('.image-background-to-popup').click((e) => {
    $(".image-background-to-popup").css('display', 'none');
});

$('.upload-excel-to-evaluate-input').on('change', (e) => {
    e.preventDefault();

    var formData = new FormData($('.form-upload-query-compounds').get(0));

    var uploadedFile = null;

    console.log('upload-excel-to-evaluate-input');

    for (var pair of formData.entries()) {
        console.log(pair[0], pair[1]);
        if (pair[0] == 'document') {
            if (pair[1]['name'] == '') {
                return;
            }
            else {
                console.log('file attached');
                uploadedFile = pair[1]; 
                var fileExt = pair[1]['name'].split('.').pop();
                if (fileExt != 'csv' && fileExt != 'xlsx') {
                    alert(".csv 이나 .xlsx 형식의 파일을 업로드해주시길 바랍니다.");
                    return;
                }
            }
        }
    }

    if (confirm("해당 파일을 업로드 하시겠습니까?") == false) {
        console.log("cancel: ", uploadedFile);
        $('.form-upload-query-compounds').trigger("reset");
        return;
    }

    $('.registration-loader-wrapper').css('display', 'flex');
    $('.registration-loader').addClass('loader');

    $.ajax({
        url: '/compoundpatentability/upload-excel-to-evaluate',
        type:'POST',
        dataType: "JSON",
        data: new FormData($('.form-upload-query-compounds').get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            var arr = data['data'];

            var body = "";

            var len = $('.checkbox-smiles-to-evaluate-row').length + 1;

            $.each(arr, (i, elem) => {

                body += `
                    <tr class="checkbox-smiles-to-evaluate-row">
                        <td style="vertical-align: middle;">

                            <input class="checkbox-smiles-to-evaluate" type="checkbox" name="checkbox-id-to-evaluate" value="${elem['db']}-${elem['pk']}" checked>
                            ${len++}
                        </td>
                        <td style="vertical-align: middle; text-align:center;">
                            <div style="width:235px; height:235px; display: block; margin: 0 auto;">
                                ${elem['image']}
                            </div>
                        </td>
                        <td style="vertical-align: middle; width: 100%; word-wrap: break-word; word-break: break-all; text-align:center; font-size: 13px;">
                            Pending
                        </td>
                    </tr>
                `;
            });

            $('.table-smiles-evaluated-tbody').append(body);
            $('.registration-loader-wrapper').css('display', 'none');
            $('.registration-loader').removeClass('loader');
        }
    });
});

$('.add-smiles-to-evaluate-btn').click(function(e) {
    e.preventDefault();

    var smilesToUpload = $('#evaluate-patentability-marvin-smiles').val();

    if (smilesToUpload == '') {
        alert('평가할 화합물을 입력해주세요.')
        return;
    }

    if (smilesToUpload.length > 500) {
        alert('500자 이내로 적어주세요.')
        return;
    }

    if (confirm("해당 화합물을 업로드 하시겠습니까?") == false) {
        return;
    }

    $.ajax({
        url: '/compoundpatentability/add-smiles-to-evaluate',
        type:'POST',
        dataType: "JSON",
        data: new FormData($('.form-add-smiles-to-evaluate').get(0)),
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            if (data['operation'] == 'success') {
                var elem = data;

                var len = $('.checkbox-smiles-to-evaluate-row').length + 1;

                var body = `
                    <tr class="checkbox-smiles-to-evaluate-row checkbox-smiles-to-evaluate-row-${elem['pk']}">
                        <td style="vertical-align: middle;">
                            <input style="display:none;" type="checkbox" name="checkbox-id-to-evaluate" value="${elem['db']}-${elem['pk']}" checked>
                            <input class="checkbox-smiles-to-evaluate" type="checkbox" name="checkbox-smiles-to-evaluate" value="${elem['smiles']}" checked>
                            ${len}
                        </td>
                        <td style="vertical-align: middle; text-align:center;">
                            <div style="width:235px; height:235px; display: block; margin: 0 auto;">
                                ${elem['image']}
                            </div>
                        </td>
                        <td style="vertical-align: middle; width: 100%; word-wrap: break-word; word-break: break-all; text-align:center; font-size: 13px;">
                            Pending
                        </td>
                    </tr>
                `;

                $('.table-smiles-evaluated-tbody').append(body);
            }
            else {
                alert('유효하지 않은 화합물입니다.');
            }
        }
    });
});

$('.evaluate-patentability-btn').click(function(e) {
    e.preventDefault();

    if (!$('.evaluate-patentability-radio-patent-list-each-row').is(':checked')) {
        alert("특허를 선택해주세요.");
        return;
    }
    if (!$('.checkbox-smiles-to-evaluate').is(':checked')) {
        alert("평가할 화합물을 추가하거나 체크박스에 체크해주세요.");
        return;
    }

    var formData = new FormData($('#evaluate-patentability-list-form').get(0));
    var formDataPrecios = new FormData($('.form-add-smiles-list-to-evaluate').get(0));

    for (var pair of formDataPrecios.entries()) {
        formData.append(pair[0], pair[1]);
    }

    $('.registration-loader-wrapper').css('display', 'flex');
    $('.registration-loader').addClass('loader');

    console.log("formData:", formData);

    $.ajax({
        url: '/compoundpatentability/get-patent-score',
        type:'POST',
        dataType: "JSON",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status) {
            // console.log("data:", data);

            var arr = data['data'];

            // console.log("data:", arr['markush_data']);

            var len = $('.table-smiles-evaluated-row').length + 1;

            var body = "";
            
            $.each(arr, (i, elem) => {
                // console.log("data:", elem['markush_data']);
                body += `
                    <tr class="table-smiles-evaluated-row">
                        <td style="vertical-align: middle;">
                            ${len++}
                        </td>
                        <td style="vertical-align: middle; text-align:center;">
                            <div style="width:235px; height:235px; display: block; margin: 0 auto;">
                                ${elem['image']}
                            </div>
                        </td>
                        <td style=" display: block;">
                            <div style="width:160px; height:235px; vertical-align: middle; display:table-cell; text-align:center; font-size: 13px;">
                                비교 특허: ${elem['patent']}
                                <br>
                                <br>
                                점수: ${elem['score']}
                                <br>
                                <br>
                                <button class="check-reason-why-score-btn" value=${len}>더보기</button>
                            </div>
                            <div style="width:250px; height:235px; vertical-align: middle; display:table-cell; text-align:center; font-size: 13px; padding-left:40px;">
                                ${elem['message']}
                            </div>
                        </td>
                    </tr>
                `;

                var details = elem['details'];

                if (details.length > 0) 
                    body += `
                        <tr>
                            <td colspan=5>
                                <div class="row">
                                    <div class="col-md-1 collapse-image collapse-image-${len}">
                                        <div style="display:table-cell; vertical-align:middle; width: 50px; height:115px;">
                                        </div>
                                        상세
                                    </div>
                                    <div class="col-md-11">
                    `;

                $.each(details, (index, element) => {
                    var r_indicator = element[0];
                    var img = element[1];
                    
                    body += `
                        <div class="collapse-image collapse-image-${len}" style="width:210px; display: block; float: left; margin-right: 20px; text-align:center;">
                            ${img}
                            <br>
                            ${r_indicator}
                        </div>
                    `;
                });
                if (details.length > 0) body += `</div></div></td></tr>`;

                var markush_data = elem['markush_data'];
                console.log("markush_data.length: ", markush_data);
                
                // if (Object.keys(markush_data).length > 0) body += `<tr><td colspan=5>`;

                Object.keys(markush_data).forEach(function(key) {
                    console.log(key, markush_data[key]);
                    body += `<tr><td colspan=5 style="align-content: right;">`;

                    body += `
                        <div class="row">
                            <div class="col-md-1 collapse-image collapse-image-${len}">
                                <div style="display:table-cell; vertical-align:middle; width: 50px; height:50px;">
                                </div>
                                ${key}
                            </div>
                            <div class="col-md-11">
                    `;

                    $.each(markush_data[key], (index, element) => {
                        var img = element[0]
                        var r_freq = element[1]
                        body += `
                                <div class="collapse-image collapse-image-${len}" style="width:130px; display: block; float: left; margin-right: 20px; text-align:center;">
                                    ${img}
                                    <br>
                                    빈도수: ${r_freq}
                                </div>
                        `;
                    });

                    body += `</div></div></td></tr>`;
                });

                // if (Object.keys(markush_data).length > 0) body += `</td></tr>`;
                
            });
            // console.log(body);
            $('.registration-loader-wrapper').css('display', 'none');
            $('.registration-loader').removeClass('loader');

            $('.table-smiles-evaluated-tbody').html(body);
            $(".collapse-image").hide();
        }
    });
});

$(document).on("click", ".check-reason-why-score-btn", (e) => {
    e.stopPropagation();
    e.preventDefault();

    var html = $(e.target).html();
    var val = $(e.target).val();
    console.log(val);

    if ( !html.includes('더보기') ) {
        $(e.target).html('더보기');
        $(".collapse-image-" + val).slideUp();
    }
    else {
        $(e.target).html('가리기');
        $(".collapse-image-" + val).slideToggle();
    }
});

$('.patentability-empty-result-list').click(e => {
    $('.table-smiles-evaluated-tbody').html('');
});