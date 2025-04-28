var ksc, ksc1;
var chartDatas = {};
var chartLayouts = {};
var chartPos = {};
function viewReport(id) {
    console.log("ppb view report call");
    $.ajax({
        url:"ppb-request/report",
        type:"post",
        dataType: "text",
        data:"pkReqId="+id,
        success:function(msg){
            msg = JSON.parse(msg.replaceAll('NaN', null));
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
            var prevComp = "";

            $.each(psReqInfo, (i, elem) => {
                var assay_tp = elem["assay_tp"];
                var curComp = elem["compound"];
                var sampleName = elem["sample_name"];
                var endOfSampleName = sampleName[sampleName.length - 1];
                var analytePeakArea = parseFloat(elem["analyte_peak_area"]).toFixed(3);
                var isPeakArea = parseFloat(elem["is_peak_area"]).toFixed(3);
                var areaRatio = parseFloat(elem["area_ratio"]).toFixed(4);
                var volume = parseFloat(elem["volume"]).toFixed(3);
                var mean = parseFloat(elem["mean"]).toFixed(3);
                var sd = parseFloat(elem["sd"]).toFixed(1);
                var cv = parseFloat(elem["cv"]).toFixed(1);
                var free = parseFloat(elem["free"]).toFixed(2);
                var bound = parseFloat(elem["bound"]).toFixed(2);
                var bound_mean = parseFloat(elem["bound_mean"]).toFixed(2);
                var recovery = parseFloat(elem["recovery"]).toFixed(1);
                var remaining = parseFloat(elem["remaining"]).toFixed(1);
                var tissue = elem["tissue"];
                var sample_type = elem["sample_type"];
                var c_no = elem["c_no"];
                var subject_no = parseFloat(elem["subject_no"]);
                var conv_ppb = parseFloat(elem["conv_ppb"]).toFixed(2);
                var fu = parseFloat(elem["fu"]).toFixed(3);
                var dilution = parseFloat(elem["dilution"]).toFixed(3);
                var control_activity = parseFloat(elem["control_activity"]).toFixed(3);
                
                if (prevComp != curComp) {
                    if (prevComp != "") {
                        html += "</tbody>";
                    }

                    if (assay_tp == "PPB_UF_DILUTION") {
                        html += `
                            <thead>
                                <tr><th colspan="16" style="text-align: left; padding-top: 12px; border: 1px solid white;">${curComp}</th></tr>
                                <tr style="background-color:black; color:white;">
                                    <th>Sample Name</th>
                                    <th>Analyte Peak Area (counts)</th>
                                    <th>IS Peak Area (counts)</th>
                                    <th>Area Ratio</th>
                                    <th>Mean</th>
                                    <th>SD</th>
                                    <th>RSD</th>
                                    <th>Volume (mL)</th>
                                    <th>Mean</th>
                                    <th>Bound</th>
                                    <th>Free</th>
                                    <th>Recovery</th>
                                    <th>% R</th>
                                    <th style='background-color:white; border: 1px white solid;'></th>
                                    <th style='background-color:white; border: 1px white solid;'></th>
                                    <th style='background-color:white; border: 1px white solid;'></th>
                                <tr>
                            </thead>
                            <tbody>
                        `;
                    }
                    else {
                        html += `
                            <thead>
                                <tr><th colspan="${assay_tp == "PPB" ? 10 : ''} ${assay_tp == "PPB_UF" ? 13 : ''} ${assay_tp == "PPB_DILUTION" ? 13 : ''}" style="text-align: left; padding-top: 12px; border: 1px solid white;">${curComp}</th></tr>
                                <tr style="background-color:black; color:white;">
                                    <th>Sample Name</th>
                                    <th>Analyte Peak Area (counts)</th>
                                    <th>IS Peak Area (counts)</th>
                                    <th>Area Ratio</th>
                                    <th>Mean</th>
                                    <th>SD</th>
                                    <th>RSD</th>
                                    ${assay_tp == "PPB_UF" ? "<th>Volume (mL)</th>" : ''}
                                    ${assay_tp == "PPB_UF" ? "<th>Mean</th>" : ''}
                                    ${assay_tp == "PPB_UF" ? "<th>Bound</th>" : "<th>Free</th>" }
                                    ${assay_tp == "PPB_UF" ? "<th>Free</th>" : "<th>Bound</th>"}
                                    <th>Recovery</th>
                                    ${assay_tp == "PPB_UF" ? "<th>% R</th>" : ''} ${assay_tp == "PPB_DILUTION" ? "<th style='background-color:white; border: 1px white solid;'></th>" : ''}
                                    ${assay_tp == "PPB_DILUTION" ? "<th style='background-color:white; border: 1px white solid;'></th>" : ''}
                                    ${assay_tp == "PPB_DILUTION" ? "<th style='background-color:white; border: 1px white solid;'></th>" : ''}
                                <tr>
                            </thead>
                            <tbody>
                        `;
                    }
                }

                if (assay_tp == "PPB_UF_DILUTION") {
                    var style = '';
                    if (c_no == 'c3' && subject_no == 2) style = "style='background-color:black; color:white;'";
                    else if (c_no == 'c2' && subject_no == 1) style = "style='border: solid;'";
                    else style="style='border: 1px white solid;'";

                    html += `
                        <tr>
                            <td>${sampleName}</td>
                            <td>${analytePeakArea}</td>
                            <td>${isPeakArea}</td>
                            <td>${areaRatio}</td>
                            <td>${ sample_type != "initial" && subject_no == 1 ? mean : ''}</td>                         
                            <td>${ sample_type != "initial" && subject_no == 1 ? sd : ''}</td>
                            <td>${ sample_type != "initial" && subject_no == 1 ? cv : ''}</td>
                            <td>${volume}</td>
                            <td>${ sample_type != "initial" && subject_no == 1 ? control_activity : ''}</td>
                            <td style="color:blue;"><b>${ c_no == 'c3' && subject_no == 1 ? bound : ''}</b></td>
                            <td>${ c_no == 'c3' && subject_no == 1 ? free : ''}</td>
                            <td style="color:blue;"><b>${ c_no == 'c1' && subject_no == 1 && sample_type != 'initial' ? recovery : ''}</b></td>
                            <td style="color:blue;"><b>${ c_no == 'c1' && subject_no == 1 && sample_type != 'initial' ? remaining : ''}</b></td>
                            <td ${style}>${ c_no == 'c3' && subject_no == 2 ? '&nbsp;&nbsp;&nbsp;&nbsp;fu&nbsp;&nbsp;&nbsp;&nbsp;' : ''} ${ c_no == 'c2' && subject_no == 1 ? fu : ''}</td>
                            <td ${style}>${ c_no == 'c3' && subject_no == 2 ? 'dilution' : ''}${ c_no == 'c2' && subject_no == 1 ? dilution : ''}</td>
                            <td ${style}>${ c_no == 'c3' && subject_no == 2 ? 'Converting PPB' : ''} ${ c_no == 'c2' && subject_no == 1 ? conv_ppb : ''}</td>
                        </tr>
                    `;
                }
                else if (assay_tp == "PPB_DILUTION") {
                    var style = '';
                    if (tissue == "buffer" && subject_no == 2) style = "style='background-color:black; color:white;'";
                    else if (tissue != "initial" && tissue != "buffer" && subject_no == 1) style = "style='border: solid;'";
                    else style="style='border: 1px white solid;'";

                    html += `
                        <tr>
                            <td>${sampleName}</td>
                            <td>${analytePeakArea}</td>
                            <td>${isPeakArea}</td>
                            <td>${areaRatio}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? mean : ''}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? sd : ''}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? cv : ''}</td>
                            <td>${ tissue != "buffer" && tissue != "initial" && subject_no == 1 ? free : ''}</td>
                            <td style="color:blue;"><b>${ tissue != "buffer" && tissue != "initial" && subject_no == 1 ? bound : ''}</b></td>
                            <td style="color:blue;"><b>${ tissue == "initial" ? recovery : ''}</b></td>
                            <td ${style}>${ tissue == "buffer" && subject_no == 2 ? '&nbsp;&nbsp;&nbsp;&nbsp;fu&nbsp;&nbsp;&nbsp;&nbsp;' : ''} ${ tissue != "initial" && tissue != "buffer" && subject_no == 1 ? fu : ''}</td>
                            <td ${style}>${ tissue == "buffer" && subject_no == 2 ? 'dilution' : ''}${ tissue != "initial" && tissue != "buffer" && subject_no == 1 ? dilution : ''}</td>
                            <td ${style}>${ tissue == "buffer" && subject_no == 2 ? 'Converting PPB' : ''} ${ tissue != "initial" && tissue != "buffer" && subject_no == 1 ? conv_ppb : ''}</td>
                        </tr>
                    `;
                }
                else if (assay_tp == "PPB_UF") {
                    html += `
                        <tr>
                            <td>${sampleName}</td>
                            <td>${analytePeakArea}</td>
                            <td>${isPeakArea}</td>
                            <td>${areaRatio}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? mean : ''}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? sd : ''}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? cv : ''}</td>
                            <td>${volume}</td>
                            <td>${ sample_type != "initial" && subject_no == 1 ? control_activity : ''}</td>
                            <td><b>${ c_no == 'c3' && subject_no == 1 ? bound : '' }</b></td>
                            <td style="color:blue;"><b>${ c_no == 'c3' && subject_no == 1 ? free : ''}</b></td>
                            <td style="color:blue;"><b>${ c_no == 'c1' && subject_no == 1 && sample_type != 'initial' ? recovery : '' }</b></td>
                            <td style="color:blue;"><b>${ c_no == 'c1' && subject_no == 1 && sample_type != 'initial' ? remaining : ''}</b></td>
                        </tr>
                    `;
                }
                else { // PPB
                    html += `
                        <tr>
                            <td>${sampleName}</td>
                            <td>${analytePeakArea}</td>
                            <td>${isPeakArea}</td>
                            <td>${areaRatio}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? mean : ''}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? sd : ''}</td>
                            <td>${ tissue != "initial" && subject_no == 1 ? cv : ''}</td>
                            <td>${ tissue != "buffer" && tissue != "initial" && subject_no == 1 ? free : ''}</td>
                            <td style="color:blue;"><b>${ tissue != "buffer" && tissue != "initial" && subject_no == 1 ? bound : ''}</b></td>
                            <td style="color:blue;"><b>${ tissue == "initial" ? recovery : ''}</b></td>
                        </tr>
                    `;
                }
                prevComp = curComp;
            });

            html += `
                </tbody>
                </table>
            `;

            $("#report_detail").html(html);
        },
        error:function(msg){
            console.log("error:", msg);
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