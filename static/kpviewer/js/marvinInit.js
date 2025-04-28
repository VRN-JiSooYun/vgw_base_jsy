jQuery.fn.lookfor = function(elem) {
    var $target = this,
        $next = $target;

    while ($next.length) {
        $target = $next;
        var found = $target.find(elem);
        
        if (found.length > 0) {
            return found;
        }
        $next = $next.children();
    }
    return null;
}

function marvin(e) {
    var idx = $('.marvin-mod').length;
    var p = $(e).parent();

    p.attr("id","marvin-mod" + idx);
    $(e).addClass('marvin-mod');
    
    p.parent().addClass('whole-marvin-block' + idx);
    p.parent().find('.marvin-search-result').addClass('marvin-search-result' + idx);
    p.parent().lookfor('.save-by-smiles') && p.parent().lookfor('.save-by-smiles').val(idx);
    p.parent().lookfor('.search-by-smiles') && p.parent().lookfor('.search-by-smiles').val(idx);
    p.parent().lookfor('.search-by-name') && p.parent().lookfor('.search-by-name').val(idx);
    p.parent().lookfor('.submit-smiles') && p.parent().lookfor('.submit-smiles').val(idx);
    p.parent().lookfor('.input-smiles') && p.parent().lookfor('.input-smiles').val(idx);
    p.parent().lookfor('.input-smiles') && p.parent().lookfor('.input-smiles').addClass('input-smiles' + idx);

    console.log("ChemicalizeMarvinJs");
    console.log("ChemicalizeMarvinJs:" + ChemicalizeMarvinJs);

    ChemicalizeMarvinJs.createEditor("#marvin-mod" + idx).then((marvin) => {
        marvin.on("molchange", () => {
            marvin.exportStructure("smiles").then(function (smiles) {
                p.parent().lookfor('.smiles-result-markush').attr('value', smiles);
            })
        });

        $('.input-smiles' + idx).click(e => {
            e.preventDefault();

            var curTarget = $(e.target);
            while (!curTarget.is('form') && curTarget != null) curTarget = curTarget.parent();
        
            var markush = curTarget.lookfor('.smiles-result-markush').val();
            console.log(markush);

            marvin.importStructure(null, markush);
        });
    });
}
