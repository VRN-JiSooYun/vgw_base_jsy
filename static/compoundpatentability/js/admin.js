// const patentAdminMarvinSketcher = ChemicalizeMarvinJs.createEditor("#patent-admin-marvin").then((marvin) => {
//     marvin.on("molchange", val => {
//         marvin.exportStructure("smiles").then(function (smiles) {
//             document.getElementById("patent-admin-marvin-smiles").value = smiles;
//         });
//     });

//     $("#patent-admin-marvin-input").click(e => {
//         e.preventDefault();
//         let smiles = document.getElementById("patent-admin-marvin-smiles").value;
//         marvin.importStructure(null, smiles);
//     })
// });

$('.patent-pdf-file-download-btn').click((e) => {
    e.preventDefault();

    var selectedPatent = $('.admin-radio-patent-list-each-row:checked').val();
    if (selectedPatent == undefined) {
        alert("특허를 선택해주세요.");
        return;
    }
    
    fetch('/compoundpatentability/download-patent-pdf?title=' + selectedPatent).then(response => response.blob()).then(blob => {
        console.log(blob);
        const link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = selectedPatent + '.pdf';
        link.click();
    }).catch(console.error);
});

$('.admin-radio-patent-list-each-row').on('change', function() {
    console.log($(this).val());

    $.ajax({
        url: '/compoundpatentability/get-markush?title=' + $(this).val(),
        type:'GET',
        dataType: "JSON",
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            $('.markush-list-table').html('');

            var arr = data['data'];

            var len = $('.markush-row').length + 1;

            var body = "";
            
            $.each(arr, (i, elem) => {
                body += `
                <tr class="markush markush-row markush-row-${elem['pk']}">
                        <td style="vertical-align: middle;">
                            <input class="markush-checkbox" type="checkbox" name="markush-checkbox" value="${elem['pk']}">
                            ${len++}
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

            $('.markush-list-table').append(body);
        }
    });
});

$('.form-upload-markush').submit(function(e) {
    e.preventDefault();

    var selectedPatent = $('.admin-radio-patent-list-each-row:checked').val();
    var selectedSmiles = $('#patent-admin-marvin-smiles').val();
    if (selectedPatent == undefined) {
        alert("특허를 선택해주세요.");
        return;
    }
    if(selectedSmiles == '') {
        alert("마쿠쉬를 입력해주세요.");
        return;
    }

    var formData = new FormData($(this).get(0));
    var formDataPrecios = new FormData($('#admin-patent-list-form').get(0));

    for (var pair of formDataPrecios.entries()) {
        formData.append(pair[0], pair[1]);
    }

    $.ajax({
        url: '/compoundpatentability/add-markush',
        type:'POST',
        dataType: "JSON",
        data: formData,
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            var elem = data;

            if (elem['operation'] == 'failed') {
                $('.markush-decompose-embodiments-result-message').html('Invalid Smiles');
                $('.markush-decompose-embodiments-result-message').css('color', 'red');
                return;
            }

            var len = $('.markush-row').length + 1;

            var body = `
                <tr class="markush markush-row markush-row-${elem['pk']}">
                    <td style="vertical-align: middle;">
                        <input class="markush-checkbox" type="checkbox" name="markush-checkbox" value="${elem['pk']}">
                        ${len}
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

            $('.markush-list-table').append(body);
        }
    });
});

$(".checkbox-markush-select-all").change(function() {
    if (this.checked) {
        $('.markush-checkbox').prop('checked', true);
    }
    else {
        $('.markush-checkbox').prop('checked', false);
    }markush
});

$('.delete-markush-btn').click((e) => {
    e.preventDefault();

    var patentFormData = new FormData($('#admin-patent-list-form').get(0));

    var formData = new FormData($('.markush-list-form').get(0));

    for (var pair of formData.entries()) {
        patentFormData.append(pair[0], pair[1]);
    }

    for (var pair of patentFormData.entries()) {
        console.log(pair[0], pair[1]);
    }

    $.ajax({
        url: '/compoundpatentability/remove-markushes',
        type: 'POST',
        data: patentFormData,
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);
            if (data["operation"] == "success") {
                for (var pair of formData.entries()) {
                    if (pair[0] == "markush-checkbox") {
                        console.log('.markush-row-' + pair[1]);
                        $('.markush-row-' + pair[1]).remove();
                    }
                }
            }
        }
    });
});

$('.markush-decompose-embodiments-btn').click((e) => {
    e.preventDefault();

    var selectedPatent = $('.admin-radio-patent-list-each-row:checked').val();
    if (selectedPatent == undefined) {
        alert("특허를 선택해주세요.");
        return;
    }

    $('.registration-loader-wrapper').css('display', 'flex');
    $('.registration-loader').addClass('loader');

    var val = $('.admin-radio-patent-list-each-row:checked').val();

    $.ajax({
        url: '/compoundpatentability/decompose-markush?title=' + val,
        type:'GET',
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            if (data['operation'] == 'success') {
                $('.markush-decompose-embodiments-result-message').html('실시예 분해가 완료되었습니다.');
                $('.markush-decompose-embodiments-result-message').css('color', 'green');
            }
            else {
                var group = data['group'];
                var unmatched = data['unmatched'];

                $('.markush-decompose-embodiments-result-message').html('Decomposition failed<br>unmatched: ' + unmatched + '<br>group: ' + group);
            }

            $('.registration-loader-wrapper').css('display', 'none');
            $('.registration-loader').removeClass('loader');
        }
    });
});

$('.admin-page-send-email-btn').click((e) => {
    e.preventDefault();

    var selectedPatent = $('.admin-radio-patent-list-each-row:checked').val();
    if (selectedPatent == undefined) {
        alert("특허를 선택해주세요.");
        return;
    }

    $('.registration-loader-wrapper').css('display', 'flex');
    $('.registration-loader').addClass('loader');

    var val = $('.admin-radio-patent-list-each-row:checked').val();

    $.ajax({
        url: '/compoundpatentability/send-email?title=' + val,
        type:'GET',
        processData: false,
        contentType: false,
        success: function (data, status) {
            console.log("data:", data);

            if (data['operation'] == 'success') {
                $('.patent-registration-step-3').css('background-color', colorStepOff);
                $('.patent-registration-step-3-after').css('background-color', colorStepOff);
                $('.patent-registration-step-4-before').css('background-color', colorStepOff);
                $('.patent-registration-step-3').css('color', 'white');
                $('.patent-registration-step-4').css('background-color', colorStepOn);
                $('.patent-registration-page-3').css('display', 'none');
                $('.patent-registration-page-4').css('display', "");
                $('.markush-decompose-embodiments-result-message').html('사용자에게 메일을 성공적으로 보냈습니다.');
                $('.markush-decompose-embodiments-result-message').css('color', 'green');
            }
            $('.registration-loader-wrapper').css('display', 'none');
            $('.registration-loader').removeClass('loader');
        }
    });
});