var ksc, ksc1;
var chartDatas = {};
var chartLayouts = {};
var chartPos = {};
function viewReport(id) {
    console.log("view report call");
    $.ajax({
        url:"pk-request/report",
        type:"post",
        data:"pkReqId="+id,
        success:function(msg){
            ksc = msg;
            var html = "";
            if( msg.msg != "" && msg.msg == "permission denied" ) {
                html = "<div class='title'>권한이 없습니다.</div>";
                $("#report_detail").html(html);
                return false;
            }
            var pkReqInfo = msg.pkRequest[0];
            var tissueInfo = msg.tissues_info;
            var timeInfo = msg.time_info;
            var doseInfo = msg.doseConc;
            var cycle = msg.doseCycle;
            var report = msg.report;
            var memInfo = msg.mem_info[0];
            var workMemInfo = msg.work_mem_info[0];
            var assayReportPkDesc = msg.assayReportPkDesc[0];
            var assayTissue = msg.assayTissue;
            var doseConcO = msg.doseConcO;

            document.title = pkReqInfo.complete_date + ' ' + pkReqInfo.compound_name + ' (' + pkReqInfo.target + ')';


            if( msg.pkRequest[0].is_fullpk ) {
                console.log("Full PK");
                var doseCnt = 0;
                for(dose of doseInfo) {
                    doseA = dose.rate.split(",");
                    doseCnt += doseA.length;
                }
                var headHtml = "", th = "", contHtml = "";
                var fullCnt = 0;
                var paramBa = false;
                var subjectCount = 0;

                for(tissue of tissueInfo) {
                    chartDatas[tissue.tissue] = [];
                    chartLayouts[tissue.tissue] = [];
                    chartPos[tissue.tissue] = [];
                }

                var reportInfo1 = "<div>"+
                    "<div class='title0'><span>Bioanalysis</span></div>"+
                    "<div class='title1' style='padding-left:15px;'><span>Animal Study</span></div>"+
                    "</div>";
                var purpose = "", time = "";
                /*
                cycle.forEach(function(item, index){
                    if(index != 0 ) time += ", ";
                    time += parseFloat((item.time / 60).toFixed(3));
                });
                */
                timeInfo.forEach(function(item, index){
                    if(index != 0 ) time += ", ";
                    time += parseFloat((item.time / 60).toFixed(3));
                });
                purpose = pkReqInfo.assay_tp + " (" + time + " hr)";
                
                var reportInfo1_cont = "<table class='reportInfo'>" +
                    "<tr>"+
                        "<th colspan='2'>Site</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.site==null?"":assayReportPkDesc.site)+"</td>" +
                        "<th>Manager</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_manager==null?"":assayReportPkDesc.a_manager)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th colspan='2'>Sampling</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_sampling==null?"":assayReportPkDesc.a_sampling)+"</td>" +
                        "<th>Storage</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_storage==null?"":assayReportPkDesc.a_storage)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th colspan='2'>Shipping</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_shipping==null?"":assayReportPkDesc.a_shipping)+"</td>" +
                        "<th>Shipping Condition</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_shipping_condition==null?"":assayReportPkDesc.a_shipping_condition)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th colspan='2'>Purpose</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+purpose+"</td>" +
                        "<th>Study No.</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.study_no==null?"":assayReportPkDesc.study_no)+"</td>" +
                    "</tr>" +
                    "<tr>" +
                        "<th colspan='2'>Animal<br>(species / sex / No.)</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.animal==null?"":assayReportPkDesc.animal)+"</td>" +
                        "<th>InVivo Study No.</th>" +
                        "<td colspan='3'>"+(pkReqInfo.invivo_study_no==undefined||pkReqInfo.invivo_study_no==null?"":pkReqInfo.invivo_study_no)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th>Article ID</th>" +
                        "<th>Route</th>" +
                        "<th>Dose</th>";
                    if(pkReqInfo.check_dfa) reportInfo1_cont += "<th>DFA(%)</th>";
                    reportInfo1_cont += "<th>Vehicle</th>" +
                        "<th>Days</th>" +
                        "<th>Solubility</th>" +
                        "<th>Information</th>" +
                    "</tr>";
                    for( dose of doseConcO ) {
                        reportInfo1_cont += "<tr>" +
                            "<td>"+pkReqInfo.compound_name+"</td>" +
                            "<td>"+dose.dose_tp+"</td>" +
                            "<td>"+dose.dose_rate+"mg/kg"+(dose.dose_rate_desc==null?"":"<br>("+dose.dose_rate_desc+")")+"</td>";
                            if(pkReqInfo.check_dfa) reportInfo1_cont += "<td>"+(dose.dfa_rate==null?"":dose.dfa_rate)+"</td>";
                            reportInfo1_cont += "<td>"+(dose.vehicle==null?"":dose.vehicle)+"</td>" +
                            "<td>"+(pkReqInfo.dose_days==null?"":pkReqInfo.dose_days)+"</td>" +
                            "<td>"+(dose.solubility==null?"":dose.solubility)+"</td>" +
                            "<td>"+(dose.info==null?"":dose.info)+"</td>" +
                        "</tr>";
                    }
                    reportInfo1_cont += "</table>";
                var reportInfo2 = "<div style='padding-top: 10px;'>"+
                    "<div class='title1' style='padding-left:15px;'><span>Bioanalysis</span></div>"+
                    "</div>";
                var reportInfo2_cont = "<table class='reportInfo'>" +
                    "<tr>" +
                        "<th colspan='5' class='trGray'>Sample</th>" +
                    "</tr>" +
                    "<tr>"+
                        "<th>Site</th>" +
                        "<td colspan='2' style='width:250px;'>"+(assayReportPkDesc==undefined||assayReportPkDesc.site==null?"":assayReportPkDesc.site)+"</td>" +
                        "<th>Manager</th>" +
                        "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.b_manager==null?"":assayReportPkDesc.b_manager)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th>Date</th>" +
                        "<td colspan='2'>"+(assayReportPkDesc==undefined||assayReportPkDesc.b_date==null?"":assayReportPkDesc.b_date)+"</td>" +
                        "<th>Storage</th>" +
                        "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.b_storage==null?"":assayReportPkDesc.b_storage)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th style='width:150px;height:50px;'>Article ID</th>" +
                        "<th style='width:150px;'>Matrix</th>" +
                        "<th colspan='3'>Sample preparation</th>" +
                    "</tr>";
                    for( tissue of assayTissue ) {
                        reportInfo2_cont += "<tr>"+
                            "<td>"+pkReqInfo.compound_name+"</td>" +
                            "<td>"+tissue.tissue+"</td>" +
                            "<td colspan='3'>"+tissue.preparation+"</td>" +
                        "</tr>";
                    }        
                    reportInfo2_cont += "<tr>"+
                        "<th>PK Analysis</th>" +
                        "<td colspan='4'>"+(assayReportPkDesc==undefined||assayReportPkDesc.pk_analysis==null?"":assayReportPkDesc.pk_analysis)+"</th>" +
                    "</tr>";            
                    reportInfo2_cont += "</table>";

                var reportInfo3 = "<table class='reportInfo'>" +
                                    "<tr>" +
                                        "<th colspan='4' class='trGray'>HPLC</th>" +
                                    "</tr>" +
                                    "<tr>" +
                                        "<th style='width:30%;'>HPLC system</th>" +
                                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.hplc_system==null?"":assayReportPkDesc.hplc_system)+"</td>" +
                                    "</tr>" +
                                    "<tr>" +
                                        "<th>Column</th>" +
                                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.hplc_column==null?"":assayReportPkDesc.hplc_column)+"</td>" +
                                    "</tr>" +
                                    "<tr>" +
                                        "<th>Mobile Phase</th>" +
                                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.mobile_phase==null?"":assayReportPkDesc.mobile_phase)+"</td>" +
                                    "</tr>" +
                                    "<tr>" +
                                        "<th>Injection Volume</th>" +
                                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.injection_volume==null?"":assayReportPkDesc.injection_volume)+"</td>" +
                                    "</tr>" +
                                    "<tr>" +
                                        "<th>Sample analysis time</th>" +
                                        "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.analysis_time==null?"":assayReportPkDesc.analysis_time)+"</td>" +
                                        "<th>Retention time</th>" +
                                        "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.retention_time==null?"":assayReportPkDesc.retention_time)+"</td>" +
                                    "</tr>" +
                                "</table>";
                var reportInfo4 = "<table class='reportInfo'>" +
                                "<tr>" +
                                    "<th colspan='2' class='trGray'>Mass spectrometry</th>" +
                                "</tr>" +
                                "<tr>" +
                                    "<th style='width:30%;'>System of Analysis</th>" +
                                    "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.system_analysis==null?"":assayReportPkDesc.system_analysis)+"</td>" +
                                "</tr>" +
                                "<tr>" +
                                    "<th>Molecular Weight</th>" +
                                    "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.molecular_weight==null?"":assayReportPkDesc.molecular_weight)+"</td>" +
                                "</tr>" +
                                "<tr>" +
                                    "<th>Ion Source type <br>& Ionization mode</th>" +
                                    "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.ion_info==null?"":assayReportPkDesc.ion_info)+"</td>" +
                                "</tr>" +
                                "<tr>" +
                                    "<th>Lower Limit of Quantification<br>(LLOQ)/th>" +
                                    "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.lloq==null?"":assayReportPkDesc.lloq)+"</td>" +
                                "</tr>" +
                                "<tr>" +
                                    "<th>Standard Curve Range</th>" +
                                    "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.curve_range==null?"":assayReportPkDesc.curve_range)+"</td>" +
                                "</tr>" +
                            "</table>";



                var reportInfoHtml = reportInfo1 + reportInfo1_cont + reportInfo2 + reportInfo2_cont + reportInfo3 + reportInfo4;

                html += reportInfoHtml;

                var subCount = {};
                for( reportPos = 0; reportPos < report.length; reportPos++ ){
                    var reportType = report[reportPos].type;
                    var reportInfo = report[reportPos].info;
                    var reportData = report[reportPos].data;
                    if(reportTissue != report[reportPos].tissue) paramBa = false;
                    var reportTissue = report[reportPos].tissue;

                    if( reportType == 'full') {
                        var title = reportTissue + " concentration of " + pkReqInfo.compound_name + "("+pkReqInfo.salt_form+" form, "+pkReqInfo.batch_no+")";
                        //var title = reportTissue + " concentration of " + pkReqInfo.compound_name;
                        if( reportTissue.toLowerCase() == "plasma" ) minusLen = 2;
                        else minusLen = 3;
                        if( reportInfo.dose_tp == "IV") var title2 = reportTissue + " concentration after intravenous injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData[0].subject.length-minusLen)+")";
                        else if (reportInfo.dose_tp == "IC") var title2 = reportTissue + " concentration after intracutaneous(IC) administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData[0].subject.length-minusLen)+")";
                        else if (reportInfo.dose_tp == "IP") var title2 = reportTissue + " concentration after intraperitoneal administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData[0].subject.length-minusLen)+")";
                        else if (reportInfo.dose_tp == "IT") var title2 = reportTissue + " concentration after intratracheal injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData[0].subject.length-minusLen)+")";
                        else var title2 = reportTissue + " concentration after oral administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData[0].subject.length-minusLen)+")";

                        /*
                        for( var di=0; di<doseConcO.length; di++ ) {
                            if( reportInfo.id == doseConcO[di].id ){
                                if( doseConcO[di].dfa_rate != null ) title2 += " (DFA:"+doseConcO[di].dfa_rate+"%)";
                            }
                        }
                        */

                        var titleHtml = "<div style='padding-top:20px;'>" +
                            "  <div class='title0'><span>Result</span></div>" +
                            "  <div class='title1'><span>"+title+"</span></div>" +
                            "  <div class='title2'><span>"+title2+"</span></div>" +
                            "</div>";
                        subjectObj = report[reportPos].subject;
                        //subjectCount = reportData[0].subject.length-minusLen;
                        subjectCount = subjectObj.length-minusLen;
                        th = "";
                        contHtml = "";
                        //var tLen = reportData[0].subject.length;
                        var tLen = subjectObj.length
                        var meanPos = 0, sdPos = 0, ctcpPos = -1;
                        var tmpHtml = "";
                        for(i=0; i<tLen; i++){
                            //var nm = reportData[0].subject[i];
                            var nm = subjectObj[i];
                            if(nm != "Mean" && nm != "SD" && nm != "CtCp_Mean") nm = "Subject "+nm;
                            else if(nm == "CtCp_Mean") nm = "Ct/Cp ratio";
                            if( nm == "Ct/Cp ratio" ){
                                if( reportTissue != "Wholeblood" ){
                                    tmpHtml = "<th class='report_black'>"+nm+"</th>";
                                }
                            } else {
                                th += "<th class='report_black'>"+nm+"</th>";
                            }
                            if(nm == "Mean") meanPos = i;
                            if(nm == "SD") sdPos = i;
                            if(nm == "Ct/Cp ratio") ctcpPos = i;
                        }
                        th+=tmpHtml;
                        tmlHtml = "";
                        headHtml = titleHtml + "<table class='report'>" +
                            "<tr>" +
                            "<th class='report_black'>Time (hr)</th>" +
                            th +
                            "</tr>";
                        var chartData = {};
                        data_x = [];
                        data_y = [];
                        data_e = [];
                        for( data of reportData ){
                            contHtml += "<tr>" +
                                "<td class='bold'>"+parseFloat((data.time/60).toFixed(3))+"</td>";
                                data_x.push(parseFloat((data.time/60).toFixed(3)));
                            for(i=0; i<tLen; i++){
                                //if( tLen == data.subject.length ){
                                if( tLen == subjectObj.length ){
                                    var val, valStr, preVal;
                                    var preMouseNo = null;
                                    try {
                                        //preVal = data.value[i];
                                        //preVal = data.keyValue[data.subject[i]];
                                        preVal = data.keyValue[subjectObj[i]];
                                        preMouseNo = data.mouseNo[subjectObj[i]];
                                        if (preVal == undefined) preVal = "-";
                                    } catch {
                                        preVal = "-";
                                    }
                                    if( preVal == -99999999 ) {
                                        val = "N/A";
                                        valStr = val;
                                    } else if ( preVal < 0 ){
                                        val = "< "+Math.abs(preVal);
                                        valStr = val;
                                    } else if ( preVal >= 0 && data.bql[i] > preVal ){
                                        val = preVal.toFixed(1);
                                        valStr = "<span class='red'>"+val+"</span>";
                                    } else if ( preVal >= 0 ){
                                        val = preVal.toFixed(1);
                                        valStr = val;
                                    } else {
                                        val = preVal;
                                        valStr = val;
                                    }

                                    /*
                                    if (preMouseNo != null) {
                                        valStr = valStr + " ["+preMouseNo+"]";
                                    }
                                    */

                                    if( i != ctcpPos ){
                                        if( i >= tLen-2 ) {
                                            contHtml += "<td class='bold'>"+valStr+"</td>";
                                        } else {
                                            contHtml += "<td>"+valStr+"</td>";
                                        }
                                    } else {
                                        if( reportTissue != "Wholeblood" ){
                                            tmpHtml = "<td class='bold'>"+valStr+"</td>";
                                        }
                                    }

                                    //if (data.subject[i] == 'Mean') data_y.push(parseFloat(val));
                                    if (subjectObj[i] == 'Mean') data_y.push(parseFloat(val));
                                    //if (data.subject[i] == "SD") data_e.push(parseFloat(val));
                                    if (subjectObj[i] == "SD") data_e.push(parseFloat(val));
                                } else {
                                    //if (i == data.subject.length ) continue;
                                    //var gap = reportData[0].subject.length - data.subject.length;
                                    var gap = subjectObj.length - data.subject.length;
                                    if( reportData[0].subject[i] != data.subject[i] ) {
                                        data.subject.splice(i,0,reportData[0].subject[i]);
                                        data.value.splice(i,0,'N/A');
                                    }
                                    var val, valStr, preVal;
                                    var preMouseNo = null;
                                    try {
                                        //preVal = data.value[i];
                                        preVal = data.keyValue[data.subject[i]];
                                        preMouseNo = data.mouseNo[data.subject[i]];
                                        if (preVal == undefined) preVal = "-";
                                    } catch {
                                        preVal = "-";
                                    }
                                    if( preVal == -99999999 ) {
                                        val = "N/A";
                                        valStr = val;
                                    } else if ( preVal < 0 ){
                                        val = "< "+Math.abs(preVal);
                                        valStr = val;
                                    } else if ( preVal >= 0 && data.bql[i] > preVal ){
                                        val = preVal.toFixed(1);
                                        valStr = "<span class='red'>"+val+"</span>";
                                    } else if ( preVal >= 0 ){
                                        val = preVal.toFixed(1);
                                        valStr = val;
                                    } else {
                                        val = preVal;
                                        valStr = val;
                                    }
                                    /*
                                    if (preMouseNo != null) {
                                        valStr = valStr + " ["+preMouseNo+"]";
                                    }
                                    */
                                    if( i != ctcpPos ){
                                        if( i >= tLen-2 ) {
                                            contHtml += "<td class='bold'>"+valStr+"</td>";
                                        } else {
                                            contHtml += "<td>"+valStr+"</td>";
                                        }
                                    } else {
                                        if( reportTissue != "Wholeblood" ){
                                            tmpHtml = "<td class='bold'>"+valStr+"</td>";
                                        }
                                    }
                                    
                                    if (data.subject[i] == 'Mean') data_y.push(parseFloat(val));
                                    if (data.subject[i] == "SD") data_e.push(parseFloat(val));
                                }
                            }
                            contHtml += tmpHtml;
                            contHtml += "</tr>";
                        }
                        html += "<div>" + headHtml + contHtml;
                        html += "</table>" + 
                            "<div class='chart' id='chart_"+reportPos+"'></div>" +
                            "</div>";
                        fullCnt++;
                        if( fullCnt > 1 && fullCnt == doseCnt ) {
                            html += "<div class='chart' id='chart_"+reportTissue+"_total'></div>";
                        }

                        for( cic=data_y.length-1; cic >= 0; cic--){
                            if (data_y[cic] > 0) {
                                break;
                            } else {
                                data_x.pop();
                                data_y.pop();
                                data_e.pop();
                            }
                        }

                        var lType = "-";
                        var rangeTp = true;
                        var range = [];
                        if (reportInfo.dose_tp == "IV") {
                            lType="log";
                            rangeTp = false;
                            var mY = arraySum(data_y, data_e);
                            var yM = Math.max.apply(null, mY);
                            yMax = getIntegerLogCount(yM)+1;
                            range = [0,yMax]
                        }

                        var xM = Math.max.apply(null, data_x);
                        data_x.push(xM+1);
                        data_y.push(NaN);

                        chartData.name = pkReqInfo.compound_name + "_" + reportInfo.dose_tp + "_" + reportInfo.dose_rate + " mg/kg";
                        chartData.x = data_x;
                        chartData.y = data_y;
                        chartData.error_y = {};
                        chartData.error_y.type = "data";
                        chartData.error_y.array = data_e;
                        chartData.type = "scatter";
                        
                        var layout = {
                            xaxis: {
                                title:'Time (hr)',
                                autorange: true
                            },
                            yaxis: {
                                type: lType,
                                autorange: rangeTp,
                                range : range,
                                title:'Conc (ng/ml)'
                            }
                        };
                        
                        chartDatas[reportTissue].push(chartData);
                        chartLayouts[reportTissue].push(layout);
                        chartPos[reportTissue].push(reportPos);
                        
                    } else if( reportType == 'param' && reportInfo.dose_tp == 'IV' ) {
                        var naChk = false;
                        var exAvChk = false;
                        //var title = "PK Parameter of " + pkReqInfo.compound_name + " ("+reportTissue+")";
                        var title = "PK Parameter of " + pkReqInfo.compound_name + " ("+reportTissue+")" + " ("+pkReqInfo.salt_form+" form, "+pkReqInfo.batch_no+")";
                        var title2 = "PK Parameter after intravenous injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData.length-2)+")";
                        subCount[reportInfo.id] = reportData.length-2;
                        /*
                        for( var di=0; di<doseConcO.length; di++ ) {
                            if( reportInfo.id == doseConcO[di].id ){
                                if( doseConcO[di].dfa_rate != null ) title2 += " (DFA:"+doseConcO[di].dfa_rate+"%)";
                            }
                        }
                        */

                        var titleHtml = "<div style='padding-top:20px;'>" +
                            "  <div class='title0'><span>Result</span></div>" +
                            "  <div class='title1'><span>"+title+"</span></div>" +
                            "  <div class='title2'><span>"+title2+"</span></div>" +
                            "</div>";
                        contHtml = "";
                        headHtml = "<table class='report'>" +
                            "<tr class='report_black'>" +
                            "<th>Subject</th>" +
                            "<th>T<span class='small'>1/2</span><br>(hr)</th>" +
                            "<th>AUC<span class='small'>last</span><br>(hr*ng/mL)</th>" +
                            "<th>AUC<span class='small'>inf</span>obs<br>(hr*ng/mL)</th>" +
                            "<th>%AUC Extrap</th>" +
                            "<th>Cl_obs<br>(mL/min/kg)</th>" +
                            "<th>MRT<span class='small'>inf</span>_obs<br>(hr)</th>" +
                            "<th>V<span class='small'>ss</span>_obs (L/kg)</th>" +
                            "</tr>";
                        for( data of reportData ){
                            var bold = false, exAvChkI = false;
                            if( data.subject == "Mean" || data.subject == "SD") bold = true;
                            if( data.auc_extrap >= 20 ) {
                                exAvChk = true;
                                exAvChkI = true;
                            }
                            if( data.t_half==-99999999 || data.auc_last==-99999999 || data.auc_inf_obs==-99999999 || 
                                data.auc_extrap==-99999999 || data.cl_obs==-99999999 || data.mrt_inf_obs==-99999999 || 
                                data.v_ss_obs==-99999999 ) naChk = true;
                            contHtml += "<tr class='" + (bold?"bold":"") + "'>";
                            contHtml += "<td class='bold'>" + data.subject + "</td>";
                            contHtml += "<td>" + (data.t_half==-99999999?"N/A":data.t_half.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            contHtml += "<td>" + (data.auc_last==-99999999?"N/A":data.auc_last.toFixed(1)) + "</td>";
                            contHtml += "<td>" + (data.auc_inf_obs==-99999999?"N/A":data.auc_inf_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            contHtml += "<td>" + (data.auc_extrap==-99999999?"N/A":data.auc_extrap.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            contHtml += "<td>" + (data.cl_obs==-99999999?"N/A":data.cl_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            contHtml += "<td>" + (data.mrt_inf_obs==-99999999?"N/A":data.mrt_inf_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            contHtml += "<td>" + (data.v_ss_obs==-99999999?"N/A":data.v_ss_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            contHtml += "</tr>";
                        }
                        html += "<div>" + titleHtml + headHtml + contHtml;
                        html += "</table>";
                        if( naChk ) html += "<div><span>&#8251; N/A : Not applicable</span></div>";
                        if( exAvChk ) html += "<div><span>&#8251; * : Excluded from the average</span></div>";
                        html += "</div>";
                        paramBa = true;
                    } else if( reportType == 'param' && (reportInfo.dose_tp == 'PO' || reportInfo.dose_tp == 'IC' || reportInfo.dose_tp == 'IP' || reportInfo.dose_tp == 'IT') ) {
                        contHtml = "";
                        var naChk = false;
                        var exAvChk = false;
                        //var title = "PK Parameter of " + pkReqInfo.compound_name + " ("+reportTissue+")";
                        var title = "PK Parameter of " + pkReqInfo.compound_name + " ("+reportTissue+")" + " ("+pkReqInfo.salt_form+" form, "+pkReqInfo.batch_no+")";
                        if (reportInfo.dose_tp == 'IC') var title2 = "PK Parameter after intracutaneous(IC) administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData.length-2)+")";
                        else if (reportInfo.dose_tp == 'IP') var title2 = "PK Parameter after intraperitoneal administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData.length-2)+")";
                        else if (reportInfo.dose_tp == 'IT') var title2 = "PK Parameter after intratracheal injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData.length-2)+")";
                        else var title2 = "PK Parameter after oral administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportData.length-2)+")";
                        subCount[reportInfo.id] = reportData.length-2;
                        /*
                        for( var di=0; di<doseConcO.length; di++ ) {
                            if( reportInfo.id == doseConcO[di].id ){
                                if( doseConcO[di].dfa_rate != null ) title2 += " (DFA:"+doseConcO[di].dfa_rate+"%)";
                            }
                        }
                        */

                        var titleHtml = "<div style='padding-top:20px;'>" +
                            "  <div class='title0'><span>Result</span></div>" +
                            "  <div class='title1'><span>" + title + "</span></div>" +
                            "  <div class='title2'><span>" + title2 + "</span></div>" +
                            "</div>";
                        var cMin = "", cTrough = "", cAvg = "", fluctuation = "";
                        
                        for( const [key, data] of reportData.entries() ){
                            var bold = false, exAvChkI = false;
                            if( data.subject == "Mean" || data.subject == "SD" ) bold = true;
                            if( data.auc_extrap >= 20 ) {
                                exAvChk = true;
                                exAvChkI = true;
                            }
                            if( data.t_half==-99999999 || data.t_max==-99999999 || data.c_max==-99999999 || 
                                data.auc_last==-99999999 || data.auc_inf_obs==-99999999 || data.auc_extrap==-99999999 || 
                                data.mrt_inf_obs==-99999999 ) naChk = true;
                            contHtml += "<tr class='" + (bold?"bold":"") + "'>";
                            contHtml += "<td class='bold'>" + data.subject + "</td>";
                            if (exAvChkI) exAvChk = true;
                            contHtml += "<td>" + (data.t_half==-99999999?"N/A":data.t_half.toFixed(1)) + (exAvChkI&&!bold?"*":"") +"</td>";
                            contHtml += "<td>" + (data.t_max==-99999999?"N/A":data.t_max.toFixed(1)) + "</td>";

                            if( data.c_min != null ) {
                                contHtml += "<td>" + (data.c_min==-99999999?"N/A":data.c_min.toFixed(1)) + "</td>";
                                cMin = "<th>C<span class='small'>min</span><br>(ng/mL)</th>";
                            }
                            contHtml += "<td>" + (data.c_max==-99999999?"N/A":data.c_max.toFixed(1)) + "</td>";
                            if( data.c_trough != null ) {
                                contHtml += "<td>" + (data.c_trough==-99999999?"N/A":data.c_trough.toFixed(1)) + "</td>";
                                cTrough = "<th>C<span class='small'>trough</span><br>(ng/mL)</th>";
                            }
                            if( data.c_avg != null ) {
                                contHtml += "<td>" + (data.c_avg==-99999999?"N/A":data.c_avg.toFixed(1)) + "</td>";
                                cAvg = "<th>C<span class='small'>avg,ss</span><br>(ng/mL)</th>";
                            }
                            
                            contHtml += "<td>" + (data.auc_last==-99999999?"N/A":data.auc_last.toFixed(1)) + "</td>";

                            contHtml += "<td>" + (data.auc_inf_obs==-99999999?"N/A":data.auc_inf_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") +"</td>";
                            contHtml += "<td>" + (data.auc_extrap==-99999999?"N/A":data.auc_extrap.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            if( data.fluctuation != null ) {
                                contHtml += "<td>" + (data.fluctuation==-99999999?"N/A":data.fluctuation.toFixed(1)) + "</td>";
                                fluctuation = "<th>Fluctuation<br>(%)</th>";
                            }
                            contHtml += "<td>" + (data.mrt_inf_obs==-99999999?"N/A":data.mrt_inf_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                            contHtml += "</tr>";

                            if( paramBa && key == reportData.length-1 ) {
                                contHtml += "<tr class='"+(bold?"bold":"")+"'>";
                                contHtml += "<td colspan='9'>Bioavailability (BA) : " + (data.bioavailability==-99999999?"N/A":data.bioavailability.toFixed(1)+"%") + "</td>";
                                contHtml += "</tr>";
                            }
                        }
                        headHtml = "<table class='report'>" +
                            "<tr class='report_black'>" +
                            "<th>Subject</th>" +
                            "<th>T<span class='small'>1/2</span><br>(hr)</th>" +
                            "<th>T<span class='small'>max</span><br>(hr)</th>" + 
                            cMin +
                            "<th>C<span class='small'>max</span><br>(ng/mL)</th>" + 
                            cTrough + 
                            cAvg + 
                            "<th>AUC<span class='small'>last</span><br>(hr*ng/mL)</th>" +
                            "<th>AUC<span class='small'>inf</span>_obs<br>(hr*ng/mL)</th>" +
                            "<th>%AUC Extrap</th>" +
                            fluctuation + 
                            "<th>MRT<span class='small'>inf</span>_obs<br>(hr)</th>" +
                            "</tr>";
                        html += "<div>" + titleHtml + headHtml + contHtml;
                        html += "</table>";
                        if( naChk ) html += "<div><span>&#8251; N/A : Not applicable</span></div>";
                        if( exAvChk ) html += "<div><span>&#8251; * : Excluded from the average</span></div>";
                        html += "</div>";

                    } else if( reportType == 'param_ext' ) {
                        contHtml = "";
                        var naChk = false;
                        var exAvChk = false;
                        //var title = "PK Parameter of " + pkReqInfo.compound_name + " ("+reportTissue+")";
                        var title = "PK Parameter of " + pkReqInfo.compound_name + " ("+reportTissue+")" + " ("+pkReqInfo.salt_form+" form, "+pkReqInfo.batch_no+")";
                        if (reportInfo.dose_tp == 'IC') var title2 = "PK Parameter after intracutaneous(IC) administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+subCount[reportInfo.id]+", mean value)";
                        else if (reportInfo.dose_tp == 'IP') var title2 = "PK Parameter after intraperitoneal administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+subCount[reportInfo.id]+", mean value)";
                        else if (reportInfo.dose_tp == 'IV') var title2 = "PK Parameter after intravenous injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+subCount[reportInfo.id]+", mean value)";
                        else if (reportInfo.dose_tp == 'IT') var title2 = "PK Parameter after intratracheal injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+subCount[reportInfo.id]+", mean value)";
                        else var title2 = "PK Parameter after oral administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+subCount[reportInfo.id]+", mean value)";
                        
                        /*
                        for( var di=0; di<doseConcO.length; di++ ) {
                            if( reportInfo.id == doseConcO[di].id ){
                                if( doseConcO[di].dfa_rate != null ) title2 += " (DFA:"+doseConcO[di].dfa_rate+"%)";
                            }
                        }
                        */

                        var titleHtml = "<div style='padding-top:20px;'>" +
                            "  <div class='title0'><span>Result</span></div>" +
                            "  <div class='title1'><span>" + title + "</span></div>" +
                            "  <div class='title2'><span>" + title2 + "</span></div>" +
                            "</div>";
                        var cMin = "", cTrough = "", cAvg = "", fluctuation = "";
                        
                        for( const [key, data] of reportData.entries() ){
                            var bold = false, exAvChkI = false;
                            //if( data.subject == "Mean" || data.subject == "SD" ) bold = true;
                            bold = true;
                            if( data.auc_extrap >= 20 ) {
                                exAvChk = true;
                                exAvChkI = true;
                                //naChk = true;
                            }
                            if( data.t_half==-99999999 || data.t_max==-99999999 || data.c_max==-99999999 || 
                                data.auc_last==-99999999 || data.auc_inf_obs==-99999999 || data.auc_extrap==-99999999 || 
                                data.mrt_inf_obs==-99999999 ) naChk = true;
                            contHtml += "<tr class='" + (bold?"bold":"") + "'>";
                            
                            if (exAvChkI) exAvChk = true;
                            
                            if (reportInfo.dose_tp == "IV" ){
                                if( data.t_half==-99999999 || data.auc_last==-99999999 || data.auc_inf_obs==-99999999 || 
                                    data.auc_extrap==-99999999 || data.cl_obs==-99999999 || data.mrt_inf_obs==-99999999 || 
                                    data.v_ss_obs==-99999999 || exAvChk ) naChk = true;
                                contHtml += "<tr class='" + (bold?"bold":"") + "'>";
                                /*contHtml += "<td>" + (data.t_half==-99999999?"N/A":data.t_half.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                                contHtml += "<td>" + (data.auc_last==-99999999?"N/A":data.auc_last.toFixed(1)) + "</td>";
                                contHtml += "<td>" + (data.auc_inf_obs==-99999999?"N/A":data.auc_inf_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                                contHtml += "<td>" + (data.auc_extrap==-99999999?"N/A":data.auc_extrap.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                                contHtml += "<td>" + (data.cl_obs==-99999999?"N/A":data.cl_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                                contHtml += "<td>" + (data.mrt_inf_obs==-99999999?"N/A":data.mrt_inf_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";
                                contHtml += "<td>" + (data.v_ss_obs==-99999999?"N/A":data.v_ss_obs.toFixed(1)) + (exAvChkI&&!bold?"*":"") + "</td>";*/
                                contHtml += "<td>" + (data.t_half==-99999999?"N/A":data.t_half.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "<td>" + (data.auc_last==-99999999?"N/A":data.auc_last.toFixed(1)) + "</td>";
                                contHtml += "<td>" + (data.auc_inf_obs==-99999999?"N/A":data.auc_inf_obs.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "<td>" + (data.auc_extrap==-99999999?"N/A":data.auc_extrap.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "<td>" + (data.cl_obs==-99999999?"N/A":data.cl_obs.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "<td>" + (data.mrt_inf_obs==-99999999?"N/A":data.mrt_inf_obs.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "<td>" + (data.v_ss_obs==-99999999?"N/A":data.v_ss_obs.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "</tr>";
                            } else {
                                if( data.t_half==-99999999 || data.t_max==-99999999 || data.c_max==-99999999 || 
                                    data.auc_last==-99999999 || data.auc_inf_obs==-99999999 || data.auc_extrap==-99999999 || 
                                    data.mrt_inf_obs==-99999999 || exAvChk) naChk = true;
                                contHtml += "<tr class='" + (bold?"bold":"") + "'>";
                                if (exAvChkI) exAvChk = true;
                                contHtml += "<td>" + (data.t_half==-99999999?"N/A":data.t_half.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "<td>" + (data.t_max==-99999999?"N/A":data.t_max.toFixed(1)) + "</td>";

                                if( data.c_min != null ) {
                                    contHtml += "<td>" + (data.c_min==-99999999?"N/A":data.c_min.toFixed(1)) + "</td>";
                                    cMin = "<th>C<span class='small'>min</span><br>(ng/mL)</th>";
                                    if(data.c_min==-99999999) naChk = true;
                                }
                                contHtml += "<td>" + (data.c_max==-99999999?"N/A":data.c_max.toFixed(1)) + "</td>";
                                if( data.c_trough != null ) {
                                    contHtml += "<td>" + (data.c_trough==-99999999?"N/A":data.c_trough.toFixed(1)) + "</td>";
                                    cTrough = "<th>C<span class='small'>trough</span><br>(ng/mL)</th>";
                                    if(data.c_trough==-99999999) naChk = true;
                                }
                                if( data.c_avg != null ) {
                                    contHtml += "<td>" + (data.c_avg==-99999999?"N/A":data.c_avg.toFixed(1)) + "</td>";
                                    cAvg = "<th>C<span class='small'>avg,ss</span><br>(ng/mL)</th>";
                                    if(data.c_avg==-99999999) naChk = true;
                                }
                                
                                contHtml += "<td>" + (data.auc_last==-99999999?"N/A":data.auc_last.toFixed(1)) + "</td>";
                                contHtml += "<td>" + (data.auc_inf_obs==-99999999?"N/A":data.auc_inf_obs.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "<td>" + (data.auc_extrap==-99999999?"N/A":data.auc_extrap.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                if( data.fluctuation != null ) {
                                    contHtml += "<td>" + (data.fluctuation==-99999999?"N/A":data.fluctuation.toFixed(1)) + "</td>";
                                    fluctuation = "<th>Fluctuation<br>(%)</th>";
                                    if(data.fluctuation==-99999999) naChk = true;
                                }
                                contHtml += "<td>" + (data.mrt_inf_obs==-99999999?"N/A":data.mrt_inf_obs.toFixed(1)) + (exAvChkI?"*":"") + "</td>";
                                contHtml += "</tr>";
                            }

                            contHtml += "</tr>";

                            if( reportInfo.dose_tp != 'IV' && paramBa && key == reportData.length-1 ) {
                                contHtml += "<tr class='"+(bold?"bold":"")+"'>";
                                contHtml += "<td colspan='9'>Bioavailability (BA) : " + (data.bioavailability==-99999999?"N/A":data.bioavailability.toFixed(1)+"%") + "</td>";
                                contHtml += "</tr>";
                            }
                        }
                        if (reportInfo.dose_tp == "IV") {
                            headHtml = "<table class='report'>" +
                                "<tr class='report_black'>" +
                                    "<th>T<span class='small'>1/2</span><br>(hr)</th>" +
                                    "<th>AUC<span class='small'>last</span><br>(hr*ng/mL)</th>" +
                                    "<th>AUC<span class='small'>inf</span>obs<br>(hr*ng/mL)</th>" +
                                    "<th>%AUC<br>Extrap</th>" +
                                    "<th>Cl_obs<br>(mL/min/kg)</th>" +
                                    "<th>MRT<span class='small'>inf</span>_obs<br>(hr)</th>" +
                                    "<th>V<span class='small'>ss</span>_obs (L/kg)</th>" +
                                "</tr>";
                        } else {
                            headHtml = "<table class='report'>" +
                                "<tr class='report_black'>" +
                                "<th>T<span class='small'>1/2</span><br>(hr)</th>" +
                                "<th>T<span class='small'>max</span><br>(hr)</th>" +                             
                                cMin +
                                "<th>C<span class='small'>max</span><br>(ng/mL)</th>" + 
                                cTrough + 
                                cAvg + 
                                "<th>AUC<span class='small'>last</span><br>(hr*ng/mL)</th>" +
                                "<th>AUC<span class='small'>inf</span>_obs<br>(hr*ng/mL)</th>" +
                                "<th>%AUC<br>Extrap</th>" +
                                fluctuation + 
                                "<th>MRT<span class='small'>inf</span>_obs<br>(hr)</th>" +
                                "</tr>";
                        }
                        
                        html += "<div>" + titleHtml + headHtml + contHtml;
                        html += "</table>";
                        if( naChk ) html += "<div><span>&#8251; N/A : Not applicable</span></div>";
                        if( exAvChk ) html += "<div><span>&#8251; * : Excluded from the average</span></div>";
                        html += "</div>";

                    } else if( reportType == 'full_semi' ){
                        var reportDtlInfo = reportInfo;
                        var reportDtlData = reportData;
                        var ctcp;
                        var tmL = {};
                        for (i=0; i<reportDtlData.length; i++) {
                            if ( reportDtlData[i].subject == "CtCp_Mean" ) {
                                ctcp = reportDtlData[i];
                            }

                            for(k=0;k<reportDtlData[i].time.length;k++){
                                tmL[reportDtlData[i].time[k]] = reportDtlData[i].time[k];
                            }

                            
                        }
                        // var tmLoop = reportDtlData[0].time.length;
                        // var tmLoop = Math.max.apply(null, tmL);
                        var tmLoop = Object.keys(tmL).length;
                        contHtml = "";
                        //var title = reportTissue + " concentration of " + pkReqInfo.compound_name;
                        var title = reportTissue + " concentration of " + pkReqInfo.compound_name + "("+pkReqInfo.salt_form+" form, "+pkReqInfo.batch_no+")";
                        
                        var title2 = "";
                        if (reportInfo.dose_tp == "IV") var title2 = reportTissue + " concentration after intravenous injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportDtlData.length-3)+")";
                        else if (reportInfo.dose_tp == "IC") var title2 = reportTissue + " concentration after intracutaneous(IC) administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportDtlData.length-3)+")";
                        else if (reportInfo.dose_tp == "IP") var title2 = reportTissue + " concentration after intraperitoneal administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportDtlData.length-3)+")";
                        else if (reportInfo.dose_tp == "IT") var title2 = reportTissue + " concentration after intratracheal injection at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportDtlData.length-3)+")";
                        else var title2 = reportTissue + " concentration after oral administration at a dose of " + reportInfo.dose_rate + " mg/kg (n="+(reportDtlData.length-3)+")";
                        
                        /*
                        for( var di=0; di<doseConcO.length; di++ ) {
                            if( reportInfo.id == doseConcO[di].id ){
                                if( doseConcO[di].dfa_rate != null ) title2 += " (DFA:"+doseConcO[di].dfa_rate+"%)";
                            }
                        }
                        */

                        var titleHtml = "<div style='padding-top:20px;'>" +
                            "  <div class='title0'><span>Result</span></div>" +
                            "  <div class='title1'><span>" + title + "</span></div>" +
                            "  <div class='title2'><span>" + title2 + "</span></div>" +
                            "</div>";

                        headHtml = "<table class='report'>" +
                            "<tr class='report_black'>" +
                            "<th rowspan='2'>Subject</th>" +
                            "<th colspan='" + tmLoop + "'>" + reportTissue + " (ng/mL)</th>" +
                            "</tr>" +
                            "<tr>";
                        for(i=0;i<tmLoop;i++){
                            headHtml += "<th>" + parseFloat((Object.keys(tmL)[i]/60).toFixed(3)) + "hr</th>";
                        }
                        headHtml += "</tr>";

                        for( ii=0; ii<reportDtlData.length; ii++){
                            if ( reportDtlData[ii].subject == "CtCp_Mean" ) continue;
                            
                            var meanFlg = false;
                            var sdFlg = false;
                            if ( reportDtlData[ii].subject == "Mean" ) meanFlg = true;
                            if ( reportDtlData[ii].subject == "SD" ) sdFlg = true;
                            contHtml += "<tr class='"+(meanFlg||sdFlg?"bold":"")+"'>";
                            contHtml += "<td class='bold'>"+reportDtlData[ii].subject+"</td>";
                            // for(j=0;j<reportDtlData[ii].time.length;j++){
                            for(j=0; j<tmLoop; j++) {
                                var val = null;
                                var mouseVal = null;
                                try{
                                    // val = reportDtlData[ii].value[j].toFixed(1);
                                    // val = reportDtlData[ii].keyValue[reportDtlData[ii].time[j]].toFixed(1);
                                    val = reportDtlData[ii].keyValue[Object.keys(tmL)[j]].toFixed(1);
                                    mouseVal = reportDtlData[ii].mouseNo[Object.keys(tmL)[j]];
                                    if (val == null) val = -99999999;
                                } catch {
                                    val = "-";
                                }
                                if( val == -99999999 ) {
                                    val = "N/A";
                                } else if ( val >= 0 && reportDtlData[ii].bql[j] > val ){
                                    val = "<span class='red'>"+val+"</span>";
                                } else if( val < 0 ){
                                    val = "< "+Math.abs(val);
                                }
                                
                                if( meanFlg && ctcp.value[j] != 1) {
                                    if( ctcp.value[j] == 0 || ctcp.value[j] == -99999999) {
                                        if(reportTissue != "Wholeblood") {
                                            val = val + "(N/A)*";
                                        }
                                    } else {
                                        if(reportTissue != "Wholeblood") {
                                            val = val + "<br>("+ctcp.value[j].toFixed(2)+")*";
                                        }
                                    }
                                }

                                /*
                                if( !meanFlg && !sdFlg ) {
                                    if(mouseVal != null ) val = val + " ["+mouseVal+"]";
                                }
                                */

                                contHtml += "<td>"+val+"</td>";
                            }
                            contHtml += "</tr>";
                        }


                        html += "<div>" + titleHtml + headHtml + contHtml;        
                        html += "</table>";

                        if(reportTissue != "Wholeblood") {
                            html += "<div><span>&#8251; * : Ct/Cp ratio</span></div>";
                        }
                        html += "<div><span>&#8251; N/A : Not applicable</span></div>";

                        html += "</div>";

                    }

                }

            } else {
                //Semi PK
                console.log("Semi PK");
                var reportInfo1 = "<div>"+
                    "<div class='title0'><span>Bioanalysis</span></div>"+
                    "<div class='title1' style='padding-left:15px;'><span>Animal Study</span></div>"+
                    "</div>";
                var animal = pkReqInfo.species + " / / " + (report.length-3);
                var route = "", dose = "", doseArr = [], purpose = "", time = "";
                doseInfo.forEach(function(item,index){ 
                    if(index != 0 ) dose += ", ";
                    dose += item.rate + " mg/kg";
                    doseArr.push(item.dose_tp);
                });
                var doseS = new Set(doseArr);
                route = Array.from(doseS).join(', ');
                /*
                cycle.forEach(function(item, index){
                    if(index != 0 ) time += ", ";
                    time += item.time / 60;
                });
                */
                timeInfo.forEach(function(item, index){
                    if(index != 0 ) time += ", ";
                    //time += item.time / 60;
                    time += parseFloat((item.time / 60).toFixed(3));
                });
                purpose = pkReqInfo.assay_tp + " (" + time + " hr)";

                var reportInfo1_cont = "<table class='reportInfo'>" +
                    "<tr>"+
                        "<th colspan='2'>Site</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.site==null?"":assayReportPkDesc.site)+"</td>" +
                        "<th>Manager</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_manager==null?"":assayReportPkDesc.a_manager)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th colspan='2'>Sampling</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_sampling==null?"":assayReportPkDesc.a_sampling)+"</td>" +
                        "<th>Storage</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_storage==null?"":assayReportPkDesc.a_storage)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th colspan='2'>Shipping</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_shipping==null?"":assayReportPkDesc.a_shipping)+"</td>" +
                        "<th>Shipping Condition</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.a_shipping_condition==null?"":assayReportPkDesc.a_shipping_condition)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th colspan='2'>Purpose</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+purpose+"</td>" +
                        "<th>Study No.</th>" +
                        "<td colspan='3'>"+(assayReportPkDesc==undefined||assayReportPkDesc.study_no==null?"":assayReportPkDesc.study_no)+"</td>" +
                    "</tr>" +
                    "<tr>" +
                        "<th colspan='2'>Animal<br>(species / sex / No.)</th>" +
                        "<td colspan='"+(pkReqInfo.check_dfa?"2":"1")+"'>"+(assayReportPkDesc==undefined||assayReportPkDesc.animal==null?"":assayReportPkDesc.animal)+"</td>" +
                        "<th>InVivo Study No.</th>" +
                        "<td colspan='3'>"+(pkReqInfo.invivo_study_no==undefined||pkReqInfo.invivo_study_no==null?"":pkReqInfo.invivo_study_no)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th>Article ID</th>" +
                        "<th>Route</th>" +
                        "<th>Dose</th>";
                    if(pkReqInfo.check_dfa) reportInfo1_cont += "<th>DFA(%)</th>";
                    reportInfo1_cont += "<th>Vehicle</th>" +
                        "<th>Days</th>" +
                        "<th>Solubility</th>" +
                        "<th>Information</th>" +
                    "</tr>";
                    for( dose of doseConcO ) {
                        reportInfo1_cont += "<tr>" +
                            "<td>"+pkReqInfo.compound_name+"</td>" +
                            "<td>"+dose.dose_tp+"</td>" +
                            "<td>"+dose.dose_rate+"mg/kg"+(dose.dose_rate_desc==null?"":"<br>("+dose.dose_rate_desc+")")+"</td>";
                            if(pkReqInfo.check_dfa) reportInfo1_cont += "<td>"+(dose.dfa_rate==null?"":dose.dfa_rate)+"</td>";
                            reportInfo1_cont += "<td>"+(dose.vehicle==null?"":dose.vehicle)+"</td>" +
                            "<td>"+(pkReqInfo.dose_days==null?"":pkReqInfo.dose_days)+"</td>" +
                            "<td>"+(dose.solubility==null?"":dose.solubility)+"</td>" +
                            "<td>"+(dose.info==null?"":dose.info)+"</td>" +
                        "</tr>";
                    }
                    reportInfo1_cont += "</table>";
                var reportInfo2 = "<div style='padding-top: 10px;'>"+
                    "<div class='title1' style='padding-left:15px;'><span>Bioanalysis</span></div>"+
                    "</div>";
                var reportInfo2_cont = "<table class='reportInfo'>" +
                    "<tr>" +
                        "<th colspan='5'>Sample</th>" +
                    "</tr>" +
                    "<tr>"+
                        "<th>Site</th>" +
                        "<td colspan='2' style='width:250px;'>"+(assayReportPkDesc==undefined||assayReportPkDesc.site==null?"":assayReportPkDesc.site)+"</td>" +
                        "<th>Manager</th>" +
                        "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.b_manager==null?"":assayReportPkDesc.b_manager)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th>Date</th>" +
                        "<td colspan='2'>"+(assayReportPkDesc==undefined||assayReportPkDesc.b_date==null?"":assayReportPkDesc.b_date)+"</td>" +
                        "<th>Storage</th>" +
                        "<td>"+(assayReportPkDesc==undefined||assayReportPkDesc.b_storage==null?"":assayReportPkDesc.b_storage)+"</td>" +
                    "</tr>" +
                    "<tr>"+
                        "<th style='width:150px;height:50px;'>Article ID</th>" +
                        "<th style='width:150px;'>Matrix</th>" +
                        "<th colspan='3'>Sample preparation</th>" +
                    "</tr>";
                    for( tissue of assayTissue ) {
                        reportInfo2_cont += "<tr>"+
                            "<td>"+pkReqInfo.compound_name+"</td>" +
                            "<td>"+tissue.tissue+"</td>" +
                            "<td colspan='3'>"+tissue.preparation+"</td>" +
                        "</tr>";
                    }        
                    reportInfo2_cont += "<tr>"+
                        "<th>PK Analysis</th>" +
                        "<td colspan='4'>"+(assayReportPkDesc==undefined||assayReportPkDesc.pk_analysis==null?"":assayReportPkDesc.pk_analysis)+"</th>" +
                    "</tr>";            
                    reportInfo2_cont += "</table>";
                var reportInfoHtml = reportInfo1 + reportInfo1_cont + reportInfo2 + reportInfo2_cont;

                html += reportInfoHtml;

                for(rpt of report) {
                    var titleName = "";
                    for( i=0; i<tissueInfo.length; i++) {
                        if( i!=0 && i<tissueInfo.length -1 ) titleName += ", ";
                        if( tissueInfo.length > 1 && i == tissueInfo.length -1) titleName += " and ";
                        titleName += tissueInfo[i].tissue;
                    }
                    var title = titleName + " concentration of " + pkReqInfo.compound_name + "("+pkReqInfo.salt_form+" form, "+pkReqInfo.batch_no+")";
                    if( rpt.info.dose_tp == "IV") var title2 = titleName + " concentration after intravenous injection at a dose of " + rpt.info.dose_rate + " mg/kg (n="+(rpt.data.length-3)+")";
                    else if( rpt.info.dose_tp == "IC") var title2 = titleName + " concentration after intracutaneous(IC) administration at a dose of " + rpt.info.dose_rate + " mg/kg (n="+(rpt.data.length-3)+")";
                    else if( rpt.info.dose_tp == "IP") var title2 = titleName + " concentration after intraperitoneal administration at a dose of " + rpt.info.dose_rate + " mg/kg (n="+(rpt.data.length-3)+")";
                    else if( rpt.info.dose_tp == "IT") var title2 = titleName + " concentration after intratracheal injection at a dose of " + rpt.info.dose_rate + " mg/kg (n="+(rpt.data.length-3)+")";
                    else var title2 = titleName + " concentration after oral administration at a dose of " + rpt.info.dose_rate + " mg/kg (n="+(rpt.data.length-3)+")";
                    //var title2 = titleName + " concentration after oral administration at a dose of " + rpt.info.dose_rate + " mg/kg (n="+(rpt.data.length-3)+")";
                    var titleHtml = "<div style='padding-top:20px;'>" +
                        "  <div class='title0'><span>Result</span></div>" +
                        "  <div class='title1'><span>"+title+"</span></div>" +
                        "  <div class='title2'><span>"+title2+"</span></div>" +
                        "</div>";

                    var headHtml = "<table class='report'>" +
                        "<tr>" +
                        "<th class='report_black' rowspan='3'>Subject</th>" +
                        "<th class='report_black' colspan='"+(tissueInfo.length * timeInfo.length)+"'>Conc.(ng/ml)</th>" +
                        "</tr>" +
                        "<tr>";
                    for (i=0; i<timeInfo.length; i++) {
                        headHtml += "<th colspan='"+tissueInfo.length+"' class='first'>"+parseFloat((timeInfo[i].time/60).toFixed(3))+"hr</th>";
                    }
                    headHtml += "</tr>";
                    headHtml += "<tr>";
                    for (j=0; j<timeInfo.length; j++) {
                        for (i=0; i<tissueInfo.length; i++) {
                            headHtml += "<th class='"+(i==0?"first":"")+"'>"+tissueInfo[i].tissue+"</th>";
                        }
                    }
                    headHtml += "</tr>";

                    var ctcp;
                    for (i=0; i<rpt.data.length; i++) {
                        if ( rpt.data[i].subject == "CtCp_Mean" ) {
                            ctcp = rpt.data[i];
                        }
                    }

                    var contHtml = "";
                    for( ii=0; ii<rpt.data.length; ii++){
                        if ( rpt.data[ii].subject == "CtCp_Mean" ) continue;
                        
                        var meanFlg = false;
                        var sdFlg = false;
                        if ( rpt.data[ii].subject == "Mean" ) meanFlg = true;
                        if ( rpt.data[ii].subject == "SD" ) sdFlg = true;
                        contHtml += "<tr class='"+(meanFlg||sdFlg?"bold":"")+"'>";
                        contHtml += "<td class='bold'>"+rpt.data[ii].subject+"</td>";
                        for (j=0; j<timeInfo.length; j++) {
                            for (i=0; i<tissueInfo.length; i++) {
                                var val = null;
                                var mouse_no = null;
                                try{
                                    val = rpt.data[ii].keyValue[timeInfo[j].time][tissueInfo[i].tissue].toFixed(1);
                                    mouse_no = rpt.data[ii].mouseNo[timeInfo[j].time][tissueInfo[i].tissue];
                                    if (val == null) val = -99999999;
                                } catch {
                                    val = "-";
                                }
                                if( val == -99999999 ) {
                                    val = "N/A";
                                } else if( val < 0 ){
                                    val = "< "+Math.abs(val);
                                }
                                var ctcpV = null;
                                try {
                                    ctcpV = ctcp.keyValue[timeInfo[j].time][tissueInfo[i].tissue];
                                } catch {
                                    ctcpV = null;
                                }
                                if( meanFlg && ctcpV != 1) {
                                    if( ctcpV == null ) {
                                        val = val + "";
                                    } else if( ctcpV == 0 ) {
                                        if(tissueInfo[i].tissue != "Wholeblood") {
                                            val = val + "(N/A)*";
                                        }
                                    } else if( ctcpV == -99999999 ) {
                                        if(tissueInfo[i].tissue != "Wholeblood") {
                                            val = val + "(N/A)*";
                                        }
                                    } else {
                                        if(tissueInfo[i].tissue != "Wholeblood") {
                                            val = val + "<br>("+ctcpV.toFixed(2)+")*";
                                        }
                                    }
                                }
                                /*
                                if( !meanFlg && !sdFlg ) {
                                    if(mouse_no != null ) val = val + " ["+mouse_no+"]";
                                }
                                */
                                contHtml += "<td class='"+(i==0?"first":"")+"'>"+val+"</td>";
                            }
                        }
                        contHtml += "</tr>";
                    }
                    html += titleHtml;
                    html += headHtml;
                    html += contHtml;
                    html += "</table>";
                    html += "<div><span>&#8251; * : Ct/Cp ratio</span></div>";
                    html += "<div><span>&#8251; N/A : Not applicable</span></div>";

                }

            }

            if( pkReqInfo.review != null && pkReqInfo.review != "" ){
                html += "<div style='padding-top:40px;'>" +
                    "<div class='title0' style='padding-bottom: 5px;'><span>Discussion</span></div>"+
                    "<table class='reportInfo'>" +
                    "<tr>" +
                    "<td>" + pkReqInfo.review.replace(/\n/g,"<br>") +
                    "</td>" +
                    "</tr>" +
                    "</table>";
            }

            html = "<div class='title'>"+(pkReqInfo.title==null||pkReqInfo.title==""?"-":pkReqInfo.title)+"</div>" + html;

            $("#report_detail").html(html);
            $("#pkRequestReportModal").modal({show:true, backdrop:false});
            if( msg.pkRequest[0].is_fullpk ) {
                for(tissue of tissueInfo) {
                    for( var ci=0; ci<chartDatas[tissue.tissue].length; ci++){
                        var chDas = [];
                        var chDass = chartDatas[tissue.tissue][ci];
                        if( chDass.x.length > 3 ) {
                            chDas.push( chDass );
                        } else{
                            chDass['mode'] = 'markers';
                            chDass['marker'] = {symbol: 'circle'};
                            chDas.push( chDass );
                        }
                        try{
                            Plotly.newPlot('chart_'+chartPos[tissue.tissue][ci], chDas, chartLayouts[tissue.tissue][ci]);
                        }catch{}
                    }
                    try{
                        Plotly.newPlot('chart_'+tissue.tissue+'_total', chartDatas[tissue.tissue], chartLayouts[tissue.tissue][0]);
                    }catch{}
                }
            }

            /*
            PK AUC, Vss Predict Button
            */
            var predictDiv = "<div style='padding-top: 40px;'>";
            predictDiv += "<a href=\"javascript:predict('"+id+"')\" class='btn btn-info btn-sm' style='font-size:18px;font-weight:bold;'>PK Curve & Dose Prediction</a>";
            predictDiv += "</div>";
            $("#report_detail").append(predictDiv);


        },
        error:function(msg){
            console.log(msg);
        }
    });
    
}

function predict(id){
    window.open('pk-request/predict?id='+id,'','width=900,height=800');
}

function predict_manual(id, dose){
    window.open('pk-request/predict_manual?id='+id+'&dose='+dose,'','width=900,height=800');
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