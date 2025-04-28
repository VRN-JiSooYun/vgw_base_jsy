//======================================================================================================
//======================================================================================================
// register complex compounds
//======================================================================================================
//======================================================================================================
const save = $("#register").click(e => {
    e.preventDefault();

    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];
    //======================================================================================================
    //======================================================================================================
    // actualizedmarkush - register with checkbox checked 
    //======================================================================================================
    //======================================================================================================
    var selectedType = $('.type-selection:checked').val();

    if (selectedType == "actualizedmarkush") {
        $.ajax({
            type: 'POST',
            url: "/compoundpatentability/registerComplexCompound",
            data: $('#smiles-markush').serialize() + '&sec=' + sec,
            success: (res) => {
                console.log(res);
                var data = res['data'];

                var len = $('.practical-row').length + 1;

                $.each(data, (idx, entry) => {
                    var markushKey = entry['pk'];
                    var elem = `
                        <tr class="practical-row practical-${markushKey}">
                            <td style="vertical-align: middle;">
                                <input class="practical-checkbox" type="checkbox" name="practical-checkbox" value="${markushKey}">
                                ${len++}
                            </td>
                            <td style="vertical-align: middle; text-align:center;">
                                <img style="width:80px; display: block; margin:auto; " src="data:image/png;base64, ${entry['img']}">
                            </td>
                            <td style="vertical-align: middle;">
                                ${entry['canonical_smiles']}
                            </td>
                        </tr>
                    `;

                    $('.actualizedmarkush').append(elem);
                });
            }
        });
        return;
    }

    //======================================================================================================
    //======================================================================================================
    // complexmarkush - register with marvin
    //======================================================================================================
    //======================================================================================================
    $.ajax({
        type: 'POST',
        url: "/compoundpatentability/registerComplexCompound",
        data: $('#smiles-markush').serialize() + '&sec=' + sec,
        success: (res) => {
            console.log(res);
            // return;
            if (res['message'] == "success") {

                $('.add-ring-constructors').css('display', '');

                var data = res['data'];

                $.each(data, (idx, entry) => {

                    //==========================================================================================================
                    // add definitive/probable ring constructors under Marvin sector
                    //==========================================================================================================
                    var unpassed = entry['unpassedNumbers'];
                    $.each(unpassed, (i, num) => {
                        $('.select-definitive-ring-constructors').append('<option class="option-definitive-ring-constructors" value="' + num + '">' + num +'</option>');
                        $('.select-probable-ring-constructors').append('<option class="option-probable-ring-constructors" value="' + num + '">' + num + '</option>');
                    });

                    //==========================================================================================================
                    // add Markush into Markush sector
                    //==========================================================================================================
                    var markushKey = entry['pk'];
                    var arr = entry['atoms'];

                    var elem = `
                        <tr class="upper-${markushKey}">
                            <td style="vertical-align: middle; text-align:center; font-size:13px; position: relative;" colspan="3">
                                <div style="width: 100%; word-wrap: break-word; word-break: break-all; text-align:left;">
                                    ${entry['frame_markush']}
                                </div>
                                <input type="radio" name="upper-radio-markushcombined" value="${markushKey}" id="radio-${markushKey}">&nbsp;&nbsp;
                                <label style="vertical-align: middle;">
                                    <img style="width:80px; display: block; margin: 0 auto;" src="data:image/png;base64, ${entry['img']}">
                                </label>
                                <button style="position: absolute; bottom: 50px; right: 20px; display:''; font-size: large;" class="btn btn-outline-secondary btn-sm delete-markush delete-markush-warning-box" value="${markushKey}" name="upper"><i class="fa fa-trash" style="pointer-events: none;"></i><span class="delete-markush-warning-box-text"><i style="font-size: large;" class="fa fa-exclamation-circle"></i> This action will delete the Markush and all the related atoms </span></button>
                                <div class="total-combinations-${markushKey}" style="position: absolute; bottom: 18px; right: 15px; display:'';">Total combinations: 0</div>
                            </td>
                        </tr>
                    `;
                    
                    $.each(arr, (i, num) => {
                        elem += `
                            <tr style="border-style: double;" class="upper-${markushKey}">
                                <td style="vertical-align: middle; border-style: double; width:15%;">
                                    <input class="upper-checkbox-markushcombined" type="checkbox" name="upper-checkbox-markushcombined-${markushKey}" value="${markushKey}-${num['r_indicator']}">
                                    ${num['r_indicator']}
                                </td>
                                <td style="border-style: double; width:85%;" class="upper-atom-buttons-${markushKey}-${num['r_indicator']}">
                                    <input style="display:none" type="text" name="uppermarkush-combinations-${markushKey}-${num['r_indicator']}" class="upper-${markushKey}-${num['r_indicator']}" readonly>
                                </td>
                            </tr>
                        `;
                    });

                    $('.complexmarkush').html(elem);
                });
            }
        }
    });
});

