var ksc, ksc1;
var chartDatas = {};
var chartLayouts = {};
var chartPos = {};
function viewReport(id) {
    console.log("view report call");
    $.ajax({
        url:"ps-request/report",
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
                var time = parseFloat(elem["time"]);

                if (prevComp != curComp) {
                    if (prevComp != "") {
                        // html += "</tbody></table>";
                        html += "</tbody>";
                    }

                    html += `
                        <thead>
                            <tr><th colspan="8" style="text-align: left; padding-top: 12px; border-left: 1px solid white; border-right: 1px solid white; ${prevComp == "" ? "border-top: 1px solid white;" : ""}">${curComp}</th></tr>
                            <tr style="background-color:black; color:white;">
                                <th>Sample Name</th><th>Analyte Peak Area (counts)</th><th>IS Peak Area (counts)</th><th>Area Ratio</th><th>Mean</th><th>SD</th><th>RSD</th><th>% R</th>
                            <tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td>${sampleName}</td>
                            <td>${analytePeakArea}</td>
                            <td>${isPeakArea}</td>
                            <td>${areaRatio}</td>
                            <td>${endOfSampleName == "1" ? mean : ''}</td>
                            <td>${endOfSampleName == "1" ? sd : ''}</td>
                            <td>${endOfSampleName == "1" ? cv : ''}</td>
                            <td style="color: blue;"><b>${endOfSampleName == "1" && time != 0 ? remaining: ''}</b></td>
                        </tr>
                    `;
                }
                else {
                    html += `
                        <tr>
                            <td>${sampleName}</td>
                            <td>${analytePeakArea}</td>
                            <td>${isPeakArea}</td>
                            <td>${areaRatio}</td>
                            <td>${endOfSampleName == "1" ? mean : ''}</td>
                            <td>${endOfSampleName == "1" ? sd : ''}</td>
                            <td>${endOfSampleName == "1" ? cv : ''}</td>
                            <td style="color: blue;"><b>${endOfSampleName == "1" && time != 0 ? remaining : ''}</b></td>
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
            console.log(msg);
        }
    });
    
}

// function getIntegerLogCount(val){
//     var ci = 1;
//     for(i=10; (val/i)>1; i*=10){
//         ci++;
//     }
//     return ci;
// }

// function arraySum(arr1, arr2) {
//     var rtnVal = [];
//     for(var i=0;i<arr1.length;i++){
//         var i1 = isNaN(arr1[i])?0:arr1[i];
//         var i2 = isNaN(arr2[i])?0:arr2[i];
//         rtnVal.push( i1 + i2);
//     }
//     return rtnVal;
// }