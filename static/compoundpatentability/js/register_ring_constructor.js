//======================================================================================================
//======================================================================================================
// register Ring constructors
//======================================================================================================
//======================================================================================================
$('.btn-add-group-definitive-ring-constructor,.btn-add-group-probable-ring-constructor').click((e) => {
    e.preventDefault();

    var defintiveOrProbable = $(e.target).val();

    var idx = $('.ol-' + defintiveOrProbable +'-ring-constructors > li').length;

    var elem = `
        <li>
            <ul style="margin-left: -30px;" class="${defintiveOrProbable}-ring-constructors-group-${idx}-list">
                <input type="text" style="display: none;" name="${defintiveOrProbable}-ring-constructors-groups" class="${defintiveOrProbable}-ring-constructors-group-${idx}-input"/>
                <li style="display: inline-block; zoom:1; *display:inline;"><input type="radio" name="radio-${defintiveOrProbable}-ring-constructors-group-radio" value="${idx}"></li>
            </ul>
        </li>
    `;

    $(".ol-" + defintiveOrProbable + "-ring-constructors").append(elem);
})

$(".btn-add-definitive-ring-constructors,.btn-add-probable-ring-constructors").click((e) => {
    e.preventDefault();
    var defintiveOrProbable = $(e.target).val();
    
    console.log("defintiveOrProbable: " + defintiveOrProbable);

    var selectedGroupIdx = $('input[name="radio-' + defintiveOrProbable + '-ring-constructors-group-radio"]:checked').val();
    console.log("selectedGroupIdx: " + selectedGroupIdx);

    var selectedR = $('.select-' + defintiveOrProbable + '-ring-constructors').find(":selected").val();
    console.log("selected R: " + selectedR);

    var prev = $('.' + defintiveOrProbable + '-ring-constructors-group-' + selectedGroupIdx + '-input').val();
    var space = prev=='' ? prev  : ' ';
    $('.' + defintiveOrProbable + '-ring-constructors-group-' + selectedGroupIdx + '-input').val(prev + space + selectedR);
    $('.' + defintiveOrProbable + '-ring-constructors-group-' + selectedGroupIdx + '-list').append('<li style="display: inline-block; zoom:1; *display:inline;">' + selectedR + '&nbsp;</li>');
});

$('.register-ring-constructors').click(e => {
    e.preventDefault();
    var arrurl = document.URL.split('/');
    var sec = arrurl[arrurl.length-2];

    $.ajax({
        type: 'POST',
        url: "/compoundpatentability/registerRingConstructors",
        data: $('#smiles-markush').serialize() + '&sec=' + sec,
        success: (res) => {
            console.log(res);
            
        }
    });
});
