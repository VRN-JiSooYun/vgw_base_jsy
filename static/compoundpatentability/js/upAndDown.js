//======================================================================================================
//======================================================================================================
// get combination of markush and atoms
//======================================================================================================
//======================================================================================================
$("#generate-comb-btn").click(e => {
    e.preventDefault();
    var serialized = $('#upper-form').serialize();

    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];

    $.ajax({
        type: 'POST',
        url: "/compoundpatentability/combinateCompounds",
        data: serialized + '&sec=' + sec,
        success: (res) => {
            console.log(res);
            var data = res['data']

            if (res['message'] == "success") {

                console.log(data['pk']);
                console.log(data['total']);

                $(".total-combinations-" + data['pk']).html("Total combinations: " + data['total']);

                return;
            }
        }
    });
});

//======================================================================================================
//======================================================================================================
// Delete practical
//======================================================================================================
//======================================================================================================
$(".checkbox-practical-select-all").change(function() {
    if(this.checked) {
        $('.practical-checkbox').each((i, elem) => {
            elem.checked = true;                        
        });
    }
    else {
        console.log("unchecked");
        $('.practical-checkbox').each((i, elem) => {
            elem.checked = false;                       
        });
    }
});

$(".delete-practical").click(e => {
    e.preventDefault();
    var serialized = $('#practical-form').serialize();

    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];

    $.ajax({
        type: 'POST',
        url: "/compoundpatentability/deletePractical",
        data: serialized + '&sec=' + sec,
        success: (res) => {
            console.log(res);
            if (res['message'] == "success") {
                var data = res['data'];
                $.each(data, (i, elem) => {
                    $('.practical-' + elem).remove();
                });
            }
        }
    });
});


$(".up-markush,.down-markush").click(e => {
    e.preventDefault();
    //--------------------------------------------------------------------------------------
    // get lower markush
    //--------------------------------------------------------------------------------------
    var lowermarkush = $('input[name=lower-radio-markushcombined]:checked').val();

    var lowerelems = $('.lower-' + lowermarkush);
    // var elems = document.getElementsByClassName(markush);

    // console.log(elems);

    var markushToUp = '';
    var markushToDown = '';

    $.each(lowerelems, (i, val) => {
        // console.log(val);
        var html = $(val).clone();

        html = html.wrapAll("<div/>").parent().html();
        html = html.replaceAll('lower', 'upper');
        
        markushToUp += html;

        $(val).remove();
    });

    //--------------------------------------------------------------------------------------
    // get upper markush
    //--------------------------------------------------------------------------------------
    var uppermarkush = $('input[name=upper-radio-markushcombined]').val();
    // console.log(uppermarkush);
    var upperelems = $('.upper-' + uppermarkush);

    $.each(upperelems, (i, val) => {
        var html = $(val).clone();
        // html.find('td').find('#radio-' + markush).remove();

        html = html.wrapAll("<div/>").parent().html();
        html = html.replaceAll('upper', 'lower');
        // $('.singlemarkush').append($(html));
        markushToDown += html;

        $(val).remove();
    });

    $('.complexmarkush').html($(markushToUp));
    $('.singlemarkush').append($(markushToDown));
});