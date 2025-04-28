$('.submit-smiles').click(function(e) {
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

    $.ajax({
        url: $('.whole-marvin-block' + $(e.target).attr('value')).attr('action'),
        type: 'post',
        data: $('.whole-marvin-block' + $(e.target).attr('value')).serialize(),
        success:(response) => {}
    });
});

$('.save-by-smiles').click(function(e) {
    e.preventDefault();

    var idx = $(e.target).attr('value');

    $.ajax({
        url: '/kpviewer/save/',
        type: 'post',
        data: $('.whole-marvin-block' + idx).serialize(),
        success:(response) => {}
    });
});

$('.search-by-smiles,.search-by-name').click(function(e) {
    e.preventDefault();

    $.ajax({
        url: $('.whole-marvin-block' + $(e.target).attr('value')).attr('action'),
        type: 'post',
        data: $('.whole-marvin-block' + $(e.target).attr('value')).serialize() + '&sec=' + $(e.target).attr('name'),
        success:(response) => {
            var items = JSON.parse(response.items);
            displayCompounds(items, $(e.target).attr('value'));
        }
    });
});

function displayCompounds(allCompounds, idx) {

    var trHTML = `
        <tr class="marvin-smiles-tr" style="border: groove;">
            <th scope="col">Rank</th>
            <th scope="col">Name</th>
            <th scope="col">Properties</th>
            <th scope="col" colspan="2">Molecule</th>
        </tr>
    `;

    $(allCompounds).each(function (i, item) {
        item = item["fields"];
        item["img"] = item["img"].replace(/ /g, '+');

        trHTML += `
            <tr class="marvin-smiles-tr" style="border: groove;" id="${item["compound_name"]}">
                <td class="section1" rowspan="2" style="background-color: darkgrey; vertical-align:middle; border: solid 1px;">
                    ${i+1}
                </td>
                <td class="compound-detail section2" colspan="3" style="padding-top: 6px; padding-bottom: 6px; background-color: lightgrey; font-style: oblique; font-weight:bold; min-width:330px; max-width:300px; word-wrap: break-word; text-align:left; vertical-align: text-top; border: solid 1px;">
                    ${item["canonical_smiles"]}
                </td>
            </tr>
            <tr>
                <td class="section3" style="background-color: lightgrey; vertical-align:middle; border: solid 1px;">
                    ${item["compound_name"]}
                </td>
                <td class="section4" style="vertical-align:middle; border: solid 1px;">
                    <div style="display: flex;">
                        <div class="col" style="display: inline-block; width: 100%;">
                            <div><b>weight:</b><p>${item["molecular_weight"]}</p></div>
                            <div><b>log P:</b><p>${item["log_p"]}</p></div>
                        </div>
                    </div>
                </td>
                <td class="section5" style="vertical-align:middle; border: solid 1px;">
                    <div style="width:350px; height:350px; cursor:pointer;" class="${item["compName"]} list img" alt="${item["smiles"]}">
                        ${item["svg_img"]}
                    </div>
                </td>
            </tr>
        `;
    
    });

    $('.marvin-search-result' + idx).html(trHTML);
    $('.whole-marvin-block' + idx).lookfor('.marvin-search-total-result').html("Total: " + allCompounds.length);
    
    return;
}
