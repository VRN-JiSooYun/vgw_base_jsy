var ksc, ksc1;
var chartDatas = {};
var chartLayouts = {};
var chartPos = {};
function viewReport(id) {
    console.log("view report call:", id);
    $.ajax({
        url:"ms-request/report",
        type:"post",
        // dataType: "html",
        dataType:'json',
        data:"pkReqId="+id,
        success:function(msg){
            console.log("msg:", msg);

            ksc = msg;
            var html = "";
            if( msg.msg != "" && msg.msg == "permission denied" ) {
                html = "<div class='title'>권한이 없습니다.</div>";
                $("#report_detail").html(html);
                return false;
            }
            var psReqInfo = msg.psRequest;

            var html = `<table style="text-align:center;">`;
            var assayType = "";
            var prevComp = "";
            var prevSpecies = "";
            var prevRemaining = 0;
            var dataIndexBySpecies = 0;
            var remaingList = [];

            $.each(psReqInfo, (i, elem) => {
                assayType = elem["assay_tp"];
                var curComp = elem["compound"];
                var sampleName = elem["sample_name"];
                var endOfSampleName = sampleName[sampleName.length - 1];
                var analytePeakArea = parseFloat(elem["analyte_peak_area"]).toFixed(1);
                var isPeakArea = parseFloat(elem["is_peak_area"]).toFixed(1);
                var areaRatio = parseFloat(elem["area_ratio"]).toFixed(3);
                var mean = parseFloat(elem["mean"]).toFixed(3);
                var sd = parseFloat(elem["sd"]).toFixed(1);
                var cv = parseFloat(elem["cv"]).toFixed(1);
                var remaining = parseFloat(elem["remaining"]).toFixed(1);
                var species = elem["species"];
                var category = elem["category"];

                var volume = '-';
                if (elem["volume"] != null) volume = parseFloat(elem["volume"]) < 0 ? String(elem["volume"]).replace('-', '<') : parseFloat(elem["volume"]).toFixed(1);

                if (prevComp != curComp) {
                    if (prevComp != "") {
                        html += "</tbody>";
                        dataIndexBySpecies = 0;
                        remaingList.push({"compound":prevComp, "species": prevSpecies, "remaining": prevRemaining});
                    }

                    html += `
                        <thead>
                            <tr><th colspan="${assayType == "S9" ? 9 : 8}" style="text-align: left; padding-top: 12px; border-left: 1px solid white; border-right: 1px solid white; ${prevComp == "" ? "border-top: 1px solid white;" : ""}">${curComp}</th></tr>
                            <tr style="background-color:black; color:white;">
                                <th>Sample Name</th><th>Analyte Peak Area (counts)</th><th>IS Peak Area (counts)</th><th>Area Ratio</th><th>Mean</th><th>SD</th><th>RSD</th><th>% R</th>${assayType == "S9" ? '<th>CLint</th>' : ''}
                            <tr>
                        </thead>
                        <tbody>
                        <tr compound="${curComp}" species="${species}" data-index=${dataIndexBySpecies}>
                            <td class="sample-name">${sampleName}</td>
                            <td class="analyte-peak-area">${analytePeakArea}</td>
                            <td class="is-peak-area">${isPeakArea}</td>
                            <td class="area-ratio">${areaRatio}</td>
                            <td class="mean">${endOfSampleName == "1" ? mean : ''}</td>
                            <td class="sd">${endOfSampleName == "1" ? sd : ''}</td>
                            <td class="cv">${endOfSampleName == "1" ? cv : ''}</td>
                            <td class="remaining" style="color: blue;">${endOfSampleName == "1" && assayType == "S9" ? remaining : ''}</td>
                            ${assayType == "S9" ? '<td style="color:red;">' + volume + '</td>' : ''}
                        </tr>
                    `;
                }
                else {

                    var borderLine = '';
                    var clintStr = '';

                    if (prevSpecies != species) {
                        dataIndexBySpecies = 0;
                        remaingList.push({"compound":prevComp, "species": prevSpecies, "remaining": prevRemaining});
                        borderLine = "style='border-top: 4px solid;'";
                        clintStr = assayType == "S9" ? volume : '';
                    }

                    html += `
                        <tr ${borderLine} compound="${curComp}" species="${species}" data-index=${dataIndexBySpecies}>
                            <td class="sample-name">${sampleName}</td>
                            <td class="analyte-peak-area">${analytePeakArea}</td>
                            <td class="is-peak-area">${isPeakArea}</td>
                            <td class="area-ratio">${areaRatio}</td>
                            <td class="mean">${endOfSampleName == "1" ? mean : ''}</td>
                            <td class="sd">${endOfSampleName == "1" ? sd : ''}</td>
                            <td class="cv">${endOfSampleName == "1" ? cv : ''}</td>
                            <td class="remaining" style="color: blue;">${endOfSampleName == "1" && assayType == "S9" ? "<b>" + remaining + "</b>": ''}</td>
                            ${assayType == "S9" ? '<td style="color:red;">' + clintStr + '</td>' : ''}
                        </tr>
                    `;
                }

                prevComp = curComp;
                prevSpecies = species;
                prevRemaining = remaining;
                dataIndexBySpecies++;
            });
            remaingList.push({"compound":prevComp, "species": prevSpecies, "remaining": prevRemaining});

            html += `
                </tbody>
                </table>
            `;

            $("#report_detail").html(html);

            if (assayType == "MS") for(var i = 0; i < remaingList.length; i++) $("tr[compound='" + remaingList[i]["compound"] + "'][species='" + remaingList[i]["species"] + "'][data-index=0] .remaining").html("<b>" + remaingList[i]["remaining"] + "</b>");
        },
        error:function(msg){
            console.log(msg);
        }
    });
    
}

function getIntegerLogCount(val){
    var ci = 1;
    for(i=10; (val/i)>1; i*=10){
        ci++;
    }
    return ci;
}

function arraySum(arr1, arr2) {
    var rtnVal = [];
    for(var i=0;i<arr1.length;i++){
        var i1 = isNaN(arr1[i])?0:arr1[i];
        var i2 = isNaN(arr2[i])?0:arr2[i];
        rtnVal.push( i1 + i2);
    }
    return rtnVal;
}