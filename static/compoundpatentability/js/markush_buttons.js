//======================================================================================================
//======================================================================================================
// Add Atom (UP)
//======================================================================================================
//======================================================================================================
$(".add-atom").click(e => {
    e.preventDefault();

    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];
    var len = $(".upper-checkbox-markushcombined:checkbox:checked").length;
    console.log("len:" + len);

    if (len > 0) {

        var arrToSend = [];
        var atom = '';

        $.each($(".upper-checkbox-markushcombined:checkbox:checked"), (i, num) => {
            var smiles = document.getElementById("smiles-result-markush").value;
            
            var markushKey_r = $(num).val();
            
            var comma = $(".upper-" + markushKey_r).val() == '' ? "" : ", ";
            
            $(".upper-atom-buttons-" + markushKey_r).append(`
            <div class="lower-checkbox-individual-div-${markushKey_r}-${smiles}" style="display: inline"> ${comma} <input type="checkbox" style="filter: hue-rotate(120deg); clip-path: circle(50% at 50% 50%);" value="${markushKey_r}-${smiles}" name="upper-checkbox-individual-atom-${markushKey_r}-${smiles}"> ${smiles} </div>
            `);
            $(".upper-" + markushKey_r).attr("value", ($(".upper-" + markushKey_r).val() + comma + smiles));

            arrToSend.push(markushKey_r);
            atom = smiles;
        });

        $.ajax({
            type: 'POST',
            url: "/compoundpatentability/registerAtmosIntoR",
            data: {
                'sec': sec,
                'markushKey_r': JSON.stringify(arrToSend),
                'smiles': atom
            },
            success: (res) => {
                console.log(res);
                
            }
        });

        return;
    }
});

//======================================================================================================
//======================================================================================================
// Delete Atom (UP)
//======================================================================================================
//======================================================================================================
$(".upper-delete-atom,.lower-delete-atom").click(e => {
    e.preventDefault();

    var val = $(e.target).val();
    var serialized = $('#' + val + '-form').serializeArray();
    
    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];

    $.ajax({
        type: 'POST',
        url: "/compoundpatentability/deleteAtom",
        data: $('#' + val + '-form').serialize() + '&sec=' + sec,
        success: (res) => {
            console.log(res);

            $.each(serialized, function (index, elem) {
                var name = elem['name'];
                var value = elem['value'];

                if (name.includes(val + '-checkbox-individual-atom')) {
                    var markush_key = value.split('-')[0];
                    var r_indicator = value.split('-')[1];
                    var atom = value.split('-')[2];
                    var curAtomList = $("." + val + "-" + markush_key + "-" + r_indicator).val().replaceAll(' ', '').split(',');
                    console.log("curAtomList:", curAtomList);

                    // remove prev comma
                    var curIndex = curAtomList.indexOf(atom);
                    if (curIndex > 0) {
                        var prevAtom = curAtomList[curIndex - 1];
                        $('.' + val + '-checkbox-individual-div-' + markush_key + '-' + r_indicator + '-' + prevAtom).html($('.' + val + '-checkbox-individual-div-' + markush_key + '-' + r_indicator + '-' + prevAtom).html().replace(',', '')); 
                    }

                    // remove checkboxes
                    $('.' + val + '-checkbox-individual-div-' + value).remove();

                    // fix text input value
                    curAtomList.splice(curIndex, 1);
                    var newStr = '';
                    for (var i = 0; i < curAtomList.length; i++) {
                        if (curAtomList[i] != atom) {
                            newStr += curAtomList[i] + ((i == (curAtomList.length - 1)) ? '' : ', ');
                        }
                    }
        
                    $("." + val +"-" + markush_key + "-" + r_indicator).attr('value', newStr);
                }
            });
        }
    });
});

//======================================================================================================
//======================================================================================================
// Delete Markush (UP)
//======================================================================================================
//======================================================================================================
$(document).on('click', '.delete-markush', e => {
    e.preventDefault();

    var val = $(e.target).val();
    var name = $(e.target).attr('name');

    var cookie = getCookie("csrftoken");
    console.log('cookie:', cookie);

    // var csrftoken = Cookies.get('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                // xhr.setRequestHeader("X-CSRFToken", csrftoken);
                xhr.setRequestHeader("X-CSRFToken", cookie);
            }
        }
    });

    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];

    $.ajax({
        type: 'POST',
        url: "/compoundpatentability/deleteMarkush",
        data: $('#' + name + '-form').serialize() + '&sec=' + sec + '&pk=' + val,
        success: (res) => {
            console.log(res);
            console.log('.' + name + '-' + val);

            if (res['message'] == 'success') {
                $.each($('.' + name + '-' + val), (i, v) => {
                    $(v).remove();
                });
            }
        }
    });
});

//======================================================================================================
//======================================================================================================
// Copy Atom (Down)
//======================================================================================================
//======================================================================================================
$(document).on('click', '.copy-atom', e => {
    e.preventDefault();

    var cookie = getCookie("csrftoken");
    console.log('cookie:', cookie);

    // var csrftoken = Cookies.get('csrftoken');

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                // xhr.setRequestHeader("X-CSRFToken", csrftoken);
                xhr.setRequestHeader("X-CSRFToken", cookie);
            }
        }
    });

    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];

    $.ajax({
        type: 'POST',
        url: "/compoundpatentability/copyAtom",
        data: $('#upper-form').serialize() + '&' + $('#lower-form').serialize() + '&sec=' + sec,
        success: (res) => {
            console.log(res);

            if (res['message'] == 'success') {
                var data = res['data'];
                console.log(data);

                //==========================================================================================================
                // add Markush into Markush sector
                //==========================================================================================================
                var markushKey = data['pk'];
                var arr = data['atoms'];

                var elem = `
                    <tr class="upper-${markushKey}">
                        <td style="vertical-align: middle; text-align:center; font-size:13px; position: relative;" colspan="3">
                            <div style="width: 100%; word-wrap: break-word; word-break: break-all; text-align:left;">
                                ${data['frame_markush']}<br>
                            </div>
                            <input type="radio" name="upper-radio-markushcombined" value="${markushKey}" id="radio-${markushKey}">&nbsp;&nbsp;
                            <label style="vertical-align: middle;">
                                <img style="width:80px; display: block; margin: 0 auto;" src="data:image/png;base64, ${data['img']}">
                            </label>
                            <button style="position: absolute; bottom: 50px; right: 20px; display:''; font-size: large;" class="btn btn-outline-secondary btn-sm delete-markush delete-markush-warning-box" value="${markushKey}" name="upper"><i class="fa fa-trash" style="pointer-events: none;"></i><span class="delete-markush-warning-box-text"><i style="font-size: large;" class="fa fa-exclamation-circle"></i> This action will delete the Markush and all the related atoms </span></button>
                            <div class="total-combinations-${markushKey}" style="position: absolute; bottom: 18px; right: 15px; display:'';">Total combinations: 0</div>
                        </td>
                    </tr>
                `;
                
                $.each(arr, (i, num) => {
                    var r_indicator = i;
                    elem += `
                        <tr style="border-style: double;" class="upper-${markushKey}">
                            <td style="vertical-align: middle; border-style: double; width:15%;">
                                <input class="upper-checkbox-markushcombined" type="checkbox" name="upper-checkbox-markushcombined-${markushKey}" value="${markushKey}-${r_indicator}">
                                ${r_indicator}
                            </td>
                            <td style="border-style: double; width:85%;" class="upper-atom-buttons-${markushKey}-${r_indicator}">`;

                    var inputVal = "";

                    $.each(num, (index, val) => {
                        var smiles = val;
                        elem += `
                            <div class="lower-checkbox-individual-div-${markushKey}-${r_indicator}-${smiles}" style="display: inline">
                                <input type="checkbox" style="filter: hue-rotate(120deg); clip-path: circle(50% at 50% 50%);" value="${markushKey}-${r_indicator}-${smiles}" name="lower-checkbox-individual-atom-${markushKey}-${r_indicator}-${smiles}"> ${smiles} ${(index == num.length -1) ? '' : ', '}
                            </div>
                        `;
                        // console.log(smiles);

                        inputVal += smiles + ((index == num.length -1) ? '' : ', ');
                        // console.log(inputVal);
                    });
                    
                    
                    elem +=`    <input style="display:none" type="text" name="uppermarkush-combinations-${markushKey}-${r_indicator}" class="upper-${markushKey}-${r_indicator}" value="${inputVal}">
                            </td>
                        </tr>
                    `;
                });

                $('.complexmarkush').html(elem);
            }
        }
    });
});