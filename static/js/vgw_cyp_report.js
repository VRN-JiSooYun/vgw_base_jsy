var ksc, ksc1;
var chartDatas = {};
var chartLayouts = {};
var chartPos = {};
function viewReport(id) {
    console.log("view report call");
    $.ajax({
        url:"cyp-request/report",
        type:"post",
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
            var prevSampleType = "";
            var prevComp = "";

            $.each(psReqInfo, (i, elem) => {
                console.log(elem);
                var curComp = elem["compound"];
                var curSampleType = elem["sample_type"];
                var sampleName = elem["sample_name"];
                var endOfSampleName = sampleName[sampleName.length - 1];
                var analytePeakArea = parseFloat(elem["analyte_peak_area"]).toFixed(1);
                var isPeakArea = parseFloat(elem["is_peak_area"]).toFixed(1);
                var areaRatio = parseFloat(elem["area_ratio"]).toFixed(2);
                var mean = parseFloat(elem["mean"]).toFixed(2);
                var sd = parseFloat(elem["sd"]).toFixed(1);
                var cv = parseFloat(elem["cv"]).toFixed(1);
                var remaining = parseFloat(elem["remaining"]).toFixed(1);
                var controlActivity = null;
                if (elem["category"] == "IC50"){
                    controlActivity = parseFloat(elem["control_activity"]).toFixed(2);
                } else if (elem["category"] == null ) {
                    controlActivity = parseFloat(elem["control_activity"]).toFixed(1);
                } else {
                    if (elem["control_activity"] != null && elem["control_activity"] < 0 ){
                        controlActivity = ">"+Math.abs(elem["control_activity"].toFixed(4));
                    } else {
                        controlActivity = parseFloat(elem["control_activity"]).toFixed(4);
                    }
                }
                    
                var backColor = elem["is_control"] || elem["is_reference"] ? "style='background-color: #CDE3F2;'" : "";
                var category = elem["category"];

                if( curSampleType == "CYP3A4" ) curSampleType = "CYP3A(M)";
                if( curSampleType == "CYP3A_T" ) curSampleType = "CYP3A(T)";
                
                if (prevSampleType != curSampleType) {
                    if (prevSampleType != "") {
                        html += "</tbody>";
                    }
                    if (category != null && category != "") {
                        
                        html += `
                            <thead>
                                <tr><th colspan="3" style="text-align: left; padding-top: 12px; border-left: 1px solid white; border-right: 1px solid white; ${prevComp == "" ? "border-top: 1px solid white;" : ""}">${curSampleType}</th></tr>
                                <tr style="background-color:black; color:white;">
                                    <th>Sample Name</th><th>Category</th><th>Value</th>
                                <tr>
                            </thead>
                            <tbody>
                            <tr ${backColor}>
                                <td>${sampleName}</td>
                                <td>${category}</td>
                                <td>${controlActivity}</td>
                            </tr>
                        `;
                    } else {
                        html += `
                            <thead>
                                <tr><th colspan="8" style="text-align: left; padding-top: 12px; border-left: 1px solid white; border-right: 1px solid white; ${prevComp == "" ? "border-top: 1px solid white;" : ""}">${curSampleType}</th></tr>
                                <tr style="background-color:black; color:white;">
                                    <th>Sample Name</th><th>Analyte Peak Area (counts)</th><th>IS Peak Area (counts)</th><th>Area Ratio</th><th>.Avg</th><th>SD</th><th>CV</th><th>% of control activity</th>
                                <tr>
                            </thead>
                            <tbody>
                            <tr ${backColor}>
                                <td>${sampleName}</td>
                                <td>${analytePeakArea}</td>
                                <td>${isPeakArea}</td>
                                <td>${areaRatio}</td>
                                <td>${endOfSampleName == "1" ? mean : ''}</td>
                                <td>${endOfSampleName == "1" ? sd : ''}</td>
                                <td>${endOfSampleName == "1" ? cv : ''}</td>
                                <td style="color: blue;"><b>${endOfSampleName == "1" ? controlActivity : ''}</b></td>
                            </tr>
                        `;
                    }
                } else {
                    if (category != null && category != "") {
                        html += `
                            <tr ${backColor}>
                                <td>${sampleName}</td>
                                <td>${category}</td>
                                <td>${controlActivity}</td>
                            </tr>
                        `;
                    } else {
                        html += `
                            <tr ${backColor}>
                                <td>${sampleName}</td>
                                <td>${analytePeakArea}</td>
                                <td>${isPeakArea}</td>
                                <td>${areaRatio}</td>
                                <td>${endOfSampleName == "1" ? mean : ''}</td>
                                <td>${endOfSampleName == "1" ? sd : ''}</td>
                                <td>${endOfSampleName == "1" ? cv : ''}</td>
                                <td style="color: blue;"><b>${endOfSampleName == "1" ? controlActivity : ''}</b></td>
                            </tr>
                        `;
                    }
                }

                prevComp = curComp;
                prevSampleType = curSampleType;
            });

            html += `
                </tbody>
                </table>
            `;

            $("#report_detail").html(html);
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