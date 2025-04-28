(function () {
    window.voronoi_obj = {};
    var _VGW_DATA = window.voronoi_obj;
    var _trk_bMSIE=(document.all)?true:false;
    var _TAD_DOMAIN="tracking"
    var _trk_bJS12=(window.screen)?true:false;
    var _trk_tD = _vgw_getRootDomain(self.document.location.href);
    var _TAD_CKDOM=((typeof _L_LACD)!="undefined"&&_L_LACD!="")?_L_LACD:"."+_trk_tD;
    if((typeof _L_LALT)!="undefined"){var _TRK_LIFE=_L_LALT;}else{var _TRK_LIFE=30;}
    var _TRK_VISIT_NEW = "";
    var _TD=new Date();

    function _vgw_setCookie(name,value,expire) {
		var today=new Date();
		today.setTime(today.getTime()+ expire);

		var domainStr = "";
		//if((typeof _TAD_CKDOM)!="undefined" && _TAD_CKDOM!="") domainStr = "domain="+_TAD_CKDOM+";";
		document.cookie=name+"="+value+"; path=/; "+domainStr+" expires="+today.toGMTString()+";";
	}
	function _vgw_getCookie(name) {
		var cookieName=name+"=";
		var x=0;
		while(x<=document.cookie.length) {
			var y=(x+cookieName.length);
			if(document.cookie.substring(x,y)==cookieName) {
				if((endOfCookie=document.cookie.indexOf(";",y))==-1) endOfCookie=document.cookie.length;
				return unescape(document.cookie.substring(y,endOfCookie));
			}
			x=document.cookie.indexOf(" ",x)+1;
			if(x == 0) break;
		}
		return "";
	}
    function _vgw_getParameter(name){
		var paraName=name+"=";
		var URL=""+self.document.location.search;
		var tURL="";
		try{ tURL=top.document.location.search; }catch(_e){}
		URL=URL+"&"+tURL;
		if(URL.indexOf(paraName)!=-1){
			var x=URL.indexOf(paraName)+paraName.length;
			var y=URL.substr(x).indexOf("&");
			if(y!=-1)return URL.substring(x,x+y);
			else return URL.substr(x);
		}
		return""
	}
	function _vgw_getNewSID(len){
		var str="01234567890abcdef";
		var ret="";
		for(var i=0;i<len;i++){
			ret=ret+(str.substr(Math.floor(Math.random()*str.length),1))
		}
		return ret
	}
    function _vgw_getRootDomain(urlStr) {
        var CDs  = new Array("ac","ad","ae","af","ag","ai","al","am","ao","aq","ar","as","at","au","aw","ax","az","ba","bb","bd","be","bf","bg","bh","bi","bj","bm","bn","bo","br","bs","bt","bw","by","bz","ca","cc","cd","cf","cg","ch","ci","ck","cl","cm","cn","co","cr","cu","cv","cw","cx","cy","cz","de","dj","dk","dm","do","dz","ec","ee","eg","er","es","et","eu","fi","fj","fk","fm","fo","fr","ga","gd","ge","gf","gg","gh","gi","gl","gm","gn","gp","gq","gr","gs","gt","gu","gw","gy","hk","hm","hn","hr","ht","hu","id","ie","il","im","in","io","iq","ir","is","it","je","jm","jo","jp","ke","kg","kh","ki","km","kn","kp","kr","kw","ky","kz","la","lb","lc","li","lk","lr","ls","lt","lu","lv","ly","ma","mc","md","me","mg","mh","mk","ml","mm","mn","mo","mp","mq","mr","ms","mt","mu","mv","mw","mx","my","mz","na","nc","ne","nf","ng","ni","nl","no","np","nr","nu","nz","om","pa","pe","pf","pg","ph","pk","pl","pm","pn","pr","ps","pt","pw","py","qa","re","ro","rs","ru","rw","sa","sb","sc","sd","se","sg","sh","si","sk","sl","sm","sn","so","sr","ss","st","su","sv","sx","sy","sz","tc","td","tf","tg","th","tj","tk","tl","tm","tn","to","tr","tt","tv","tw","tz","ua","ug","uk","us","uy","uz","va","vc","ve","vg","vi","vn","vu","wf","ws","ye","yt","za","zm","zw");
        var NCDs = new Array("aero","an","arpa","asia","bike","biz","bv","camera","cat","clothing","com","construction","contractors","coop","diamonds","directory","edu","enterprises","equipment","estate","gallery","gb","gov","graphics","guru","holdings","info","int","jobs","kitchen","land","lighting","menu","mil","mobi","museum","name","net","org","photography","plumbing","post","pro","sexy","singles","sj","tattoo","technology","tel","tips","today","tp","travel","uno","ventures","voyage","xxx");

        var tmp = urlStr;
        tmp = tmp.replace(/http(s){0,1}:\/\//gi, '');
        tmp = tmp.replace(/\/.*/gi, '');
        tmp = tmp.replace(/:[0-9]+/gi, '');

        var domain = tmp.toLowerCase();
        if(domain.match(/^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$/)) {
            return domain;
        } else {
            var de = domain.split(".");
            var TLD = de[de.length-1];

            if(_vgw_indexOf(CDs, TLD) != -1 || _vgw_indexOf(NCDs, TLD) != -1) {
                if(_vgw_indexOf(CDs, TLD) != -1) {
                    var krSecondDomains = new Array("co","ne","or","re","pe","go","mil","ac","hs","ms","es","sc","kg","seoul","busan","daegu","incheon","gwangju","daejeon","ulsan","gyeonggi","gangwon","chungbuk","chungnam","jeonbuk","jeonnam","gyeongbuk","gyeongnam","jeju");
                    if(TLD == "kr") {
                        if(_vgw_indexOf(krSecondDomains, de[de.length-2]) != -1) {
                            if(de[de.length-3] != null && de[de.length-3] != "") {
                                return de[de.length-3]+"."+de[de.length-2]+"."+de[de.length-1];
                            } else {
                                return de[de.length-2]+"."+de[de.length-1];
                            }
                        } else {
                            return de[de.length-2]+"."+de[de.length-1];
                        }
                    } else {
                        return domain;
                    }
                } else if(_vgw_indexOf(NCDs, TLD) != -1) {
                    if(de[de.length-2] != null && de[de.length-2] != "") {
                        return de[de.length-2] + "." + de[de.length-1];
                    } else {
                        return de[de.length-2];
                    }
                } else {
                    return domain;
                }
            } else {
                return domain;
            }
        }
    }
    function _vgw_indexOf(arr, obj) {
        for (var i=0; i< arr.length; i++) {
            if (arr[i] === obj) {
                return i;
            }
        }
        return -1;
    }
    function _vgw_shortenURL(sourceURL) {
        function detectAndCut(paramName, paramValues) {
            var returnArray = new Array();
            for(var j=0; j<paramValues.length; j++) {
                var paramValuePair = paramValues[j].split("=");
                var param, value;
                if(paramValuePair.length<=2) {
                    param = paramValuePair[0];
                    value = paramValuePair[1];
                } else {
                    param = paramValuePair[0];
                    for(var p=1; p<paramValuePair.length; p++) {
                        value += paramValuePair[p];
                    }
                }

                if(param == paramName) {
                    returnArray.push(param + "=");
                } else {
                    returnArray.push(paramValues[j]);
                }
            }
            return returnArray;
        }
        var domainParamDetect = new Array("cr2.shopping.naver.com|x");
        var paramParamDetect = new Array("Ncisy|NaPm", "Ncisy|Ncisy");
        var newURL = "";
        var domainQueries = sourceURL.split("?");
        var paramValues = new Array();

        if(domainQueries.length == 2) {
            var domain = domainQueries[0].toLowerCase();
            var query = domainQueries[1];
            paramValues = query.split("&");

            if(domain != "" && paramValues.length>0) {
                for(var i=0; i<domainParamDetect.length; i++) {
                    var detectCutPair = domainParamDetect[i].split("|");
                    var detect = detectCutPair[0].toLowerCase();
                    var cut = detectCutPair[1];

                    if(domain.indexOf(detect)>=0) {
                        paramValues = detectAndCut(cut, paramValues);
                    }
                }
            }

            if(query != "" && paramValues.length>0) {
                for(var i=0; i<paramParamDetect.length; i++) {
                    var detectCutPair = paramParamDetect[i].split("|");
                    var detect = detectCutPair[0];
                    var cut = detectCutPair[1];

                    if(query.indexOf(detect)>=0) {
                        paramValues = detectAndCut(cut, paramValues);
                    }
                }
            }
            newURL = domain + (paramValues.length > 0 ? ("?" + paramValues.join("&")) : "");
        } else if(domainQueries.length == 1) {
            paramValues = domainQueries[0].split("&");
            if(paramValues.length>0) {
                for(var i=0; i<paramParamDetect.length; i++) {
                    var detectCutPair = paramParamDetect[i].split("|");
                    var detect = detectCutPair[0];
                    var cut = detectCutPair[1];

                    if(domainQueries[0].indexOf(detect)>=0) {
                        paramValues = detectAndCut(cut, paramValues);
                    }
                }
            }
            newURL = paramValues.join("&");
        } else {
            newURL = sourceURL;
        }
        return newURL;
    }
    function _vgw_escape(_str) {
		var str, ch;
		var bEncURI = "N"; try{bEncURI=encodeURI('Y');}catch(_e){}
		if( bEncURI == "Y" ) str=encodeURI(_str); else str = escape(_str);
		str=str.split("+").join("%2B");
		str=str.split("/").join("%2F");
		str=str.split("&").join("%26");
		str=str.split("?").join("%3F");
		str=str.split(":").join("%3A");
		str=str.split("#").join("%23");
		return str;
	}
    var _TRK_UUID="",_TRK_SID="";
	function _vgw_make_code(){
        var t = new Date;
        var tye=(_trk_bMSIE)?(t.getYear()):(t.getFullYear()); var tmo=t.getMonth()+1; var tda=t.getDate();
        var tho=t.getHours(); var tmi=t.getMinutes(); var tse=t.getSeconds();
        var tzo=t.getTimezoneOffset();

		var dr=self.document.referrer;
		var tdr="";
		try{ tdr=top.document.referrer; }catch(_e){}
		var tdu="";
		try{ tdu=top.document.location.href; }catch(_e){}
		var bFrm=false;
		if(dr==tdu){
			dr=tdr;
			bFrm=true;
		}
		if(dr=="undefined") dr="";
		var du=self.document.location.href;
		if(du.substr(0,4)=="file") return"";
		var adKeyVal="";

		if((typeof _L_LALT)!="undefined") _TRK_LIFE=_L_LALT;
		else _TRK_LIFE=30;
		if(!dr)dr="";
		if(!du)du="";
		var tc="";
		

		_VGW_DATA.UUID = _TRK_UUID;
		_VGW_DATA.SID = _TRK_SID;
		
		var bPNF=((typeof _TRK_PI)!="undefined" && _TRK_PI=="PNF")?true:false;
		if(!bPNF)tc=tc+"&js=Y";

		var ce=navigator.cookieEnabled?tc=tc+"&ce=Y":tc=tc+"&ce=N";
	    var je=navigator.javaEnabled()?tc=tc+"&je=Y":tc=tc+"&je=N";
		var _trk_bJS12=(window.screen)?true:false;
		var ss=""; var cd = "";
        if(_trk_bJS12) {
            ss=screen.width+"x"+screen.height;
            _VGW_DATA.SR = ss;
            cd=screen.colorDepth;
            tc=tc+"&cd="+cd+"&ss="+ss;
        }

        var browserName, os, agent = window.navigator.userAgent.toLowerCase(), ua = navigator.userAgent;;
        var browserName;
        switch(true){
            case agent.indexOf("edge") > -1 :
                browserName = "MS Edge";
                break;
            case agent.indexOf("edg/") > -1 :
                browserName = "Edge (chromium based)";
                break; 
            case agent.indexOf("opr") > -1 && !!window.opr:
                browserName = "Opera";
                break;
            case agent.indexOf("chrome") > -1 && !!window.chrome:
                browserName = "Chrome";
                break;
            case agent.indexOf("trident") > -1 :
                browserName = "MS IE";
                break;
            case agent.indexOf("firefox") > -1 :
                browserName = "Mozilla Firefox";
                break;
            case agent.indexOf("safari") > -1 :
                browserName = "Safari";
                break;
            default :
                browserName = "other";
        }
        _VGW_DATA.BS = browserName;

        if (ua.match(/Win(dows )?NT 6\.0/)) {
            os = "Windows Vista";
        } else if (ua.match(/Win(dows )?(NT 5\.1|XP)/)) {
            os = "Windows XP";
        } else {
            if ((ua.indexOf("Windows NT 5.1") != -1) || (ua.indexOf("Windows XP") != -1)) {
                os = "Windows XP";
            } else if ((ua.indexOf("Windows NT 7.0") != -1) || (ua.indexOf("Windows NT 6.1") != -1)) {
                os = "Windows 7";
            } else if ((ua.indexOf("Windows NT 8.0") != -1) || (ua.indexOf("Windows NT 6.2") != -1)) {
                os = "Windows 8";
            } else if ((ua.indexOf("Windows NT 8.1") != -1) || (ua.indexOf("Windows NT 6.3") != -1)) {
                os = "Windows 8.1";
            } else if ((ua.indexOf("Windows NT 10.0") != -1) || (ua.indexOf("Windows NT 6.4") != -1)) {
                os = "Windows 10";
            } else if ((ua.indexOf("iPad") != -1) || (ua.indexOf("iPhone") != -1) || (ua.indexOf("iPod") != -1)) {
                os = "Apple iOS";
            } else if (ua.indexOf("Android") != -1) {
                os = "Android OS";
            } else if (ua.match(/Win(dows )?NT( 4\.0)?/)) {
                os = "Windows NT";
            } else if (ua.match(/Mac|PPC/)) {
                os = "Mac OS";
            } else if (ua.match(/Linux/)) {
                os = "Linux";
            } else if (ua.match(/(Free|Net|Open)BSD/)) {
                os = RegExp.$1 + "BSD";
            } else if (ua.match(/SunOS/)) {
                os = "Solaris";
            }
        }
        if (os.indexOf("Windows") != -1) {
            if (navigator.userAgent.indexOf('WOW64') > -1 || navigator.userAgent.indexOf('Win64') > -1) {
                os += ' 64bit';
            } else {
                os += ' 32bit';
            }
        }
        _VGW_DATA.OS = os;
        _VGW_DATA.UA = ua;

		var dt=document.title.toString();
		dt=dt.substr(0,128);

		tc=tc+"&dr="+_vgw_escape(dr)+"&XDR=&du="+_vgw_escape(du)+"&dt="+_vgw_escape(dt);
		tc=tc+"&tzo="+tzo+"&tye="+tye+"&tmo="+tmo+"&tda="+tda+"&tho="+tho+"&tmi="+tmi+"&tse="+tse;
		
		_VGW_DATA.dr = _vgw_escape(dr);
		_VGW_DATA.du = _vgw_escape(du);
		_VGW_DATA.dt = _vgw_escape(dt);
        _VGW_DATA.dp = _vgw_escape(location.pathname);
        _VGW_DATA.dpr = _vgw_escape(location.search);
		_VGW_DATA.tzo = tzo;
		_VGW_DATA.tye = tye;
		_VGW_DATA.tmo = tmo;
		_VGW_DATA.tda = tda;
		_VGW_DATA.tho = tho;
		_VGW_DATA.tmi = tmi;
		_VGW_DATA.tse = tse;
		
        if((typeof _TRK_USERID)!="undefined"&&_TRK_USERID!="") _VGW_DATA.UID = _TRK_USERID;
        if((typeof _TRK_USERNM)!="undefined"&&_TRK_USERNM!="") _VGW_DATA.UNM = _TRK_USERNM;

		return tc;
	}

    function _vgw_callTracker(callTp){
		if((typeof _L_LALT)!="undefined") _TRK_LIFE=_L_LALT;
		else _TRK_LIFE=30;
		_TRK_LIFE=parseInt(_TRK_LIFE)*24*60*60*1000;
		var _SS_LIFE=30*60*1000;
		_TRK_UUID=_vgw_getCookie("_TRK_UUID");
		_TRK_SID=_vgw_getCookie("_TRK_SID");

		if(_TRK_UUID=="") _TRK_UUID=_vgw_getNewSID(32);
		if(_TRK_SID==""){
			_TRK_SID=_vgw_getNewSID(32);
		}

		_vgw_setCookie("_TRK_UUID", _TRK_UUID, 30*365*24*60*60*1000);
		_vgw_setCookie("_TRK_SID", _TRK_SID, _SS_LIFE);

		var dr=self.document.referrer;
		var tdu="";
		try{ tdu=top.document.location.href; }catch(_e){}
		var _TRK_REF=(dr==tdu?top.document.referrer:self.document.referrer);
		var _TRK_QST=(dr==tdu?top.document.location.search:self.document.location.search);
        _TRK_QST=_vgw_shortenURL(_TRK_QST);
        _TRK_REF=_vgw_shortenURL(_TRK_REF);
        _TRK_RV = "";
        var thisDomain = _vgw_getRootDomain(self.document.location.href);

		var landingF = false;
		if( _TRK_REF == "" ) landingF = true;
		var drr = "", drrr = "";
		try{
			drr = tdu.match(/^http:\/\/([a-z0-9-_\.]*)[\/\?]/i)[1];
			drrr = _TRK_REF.match(/^http:\/\/([a-z0-9-_\.]*)[\/\?]/i)[1];
		}catch(_e){}
		if( drr != drrr ) landingF = true;

        _vgw_make_code();

		var URL = "/"+_TAD_DOMAIN;
		var UNDEFINED = "undefined";
		var WITH_CREDENTIALS = "withCredentials";
		var POST = "POST";
		var CONTENT_TYPE = "Content-Type";
		var TYPE_JSON = "application/json:charset=UTF-8";
		var xhr = new XMLHttpRequest();
		var url = URL+"/"+callTp;

		if(WITH_CREDENTIALS in xhr){
			xhr.open(POST, url, true);
		} else if (typeof XDomainRequest != UNDEFINED) {
			xhr = new XDomainRequest();
			xhr.open(POST, url);
		} else {
			xhr = null;
		}
        xhr.onreadystatechange = function() {
            if (xhr.readyState == 4) {
                rtn = readBody(xhr);
                rtn = JSON.parse(rtn);
                if( rtn.code == '0000' ){
                    _VGW_DATA.p_no = rtn.p_no;
                }
            }
        }
		xhr.open(POST, url, true);
		xhr.widthCredentials = true;
		xhr.setRequestHeader(CONTENT_TYPE, TYPE_JSON);
		var jsonStr = "";
		jsonStr = JSON.stringify(_VGW_DATA);
		xhr.send(jsonStr);
	}
    function readBody(xhr) {
        var data;
        if (!xhr.responseType || xhr.responseType === "text") {
            data = xhr.responseText;
        } else if (xhr.responseType === "document") {
            data = xhr.responseXML;
        } else {
            data = xhr.response;
        }
        return data;
    }
    var G="apply",C="call",z="prototype",Qc="replace",t="indexOf";
	var aa=encodeURIComponent,f=window,ba=setTimeout,n=Math,ea=RegExp;
	var O=f,M=document,ua=function(a,b,c){a.removeEventListener?a.removeEventListener(b,c,!1):a.detachEvent&&a.detachEvent("on"+b,c)};
	var ta=function(a,b,c,d){try{a.addEventListener?a.addEventListener(b,c,!!d):a.attachEvent&&a.attachEvent("on"+b,c)}catch(e){}};
	function qa(a){return void 0!=a&&-1<(a.constructor+"")[t]("String")}
	var ld;
	if(ld=qa(f.VGWObj)){
		var md=f.VGWObj;
		ld=md?md[Qc](/^[\s\xa0]+|[\s\xa0]+$/g,""):"";
	}
	var gb=ld||"_vgwCall";
	var rc=function(a){
		if("prerender"==M.webkitVisibilityState)return!1;
		a();
		return!0;
	};
	var Mc=function(a){
		if(!rc(a)){
			var b=!1,c=function(){!b&&rc(a)&&(b=!0,ua(M,"webkitvisibilitychange",c))};
			ta(M,"webkitvisibilitychange",c)
		}
	};
	var BA={F:"/plugins/ua/"};
	BA.D=function(a){
		for(var i=0;i<arguments.length;i++){
			_vgw_callTracker(arguments[i][0]);
		}
	};
	var $=function(){_vgw_callTracker(arguments[0])};
	$.B=function(){
		var a=O[gb];O[gb]=$;var b=a&&a.q;"[object Array]"==Object[z].toString[C](Object(b))&&Mc(function(){BA.D[G]($,b)})
	};
	$.B();




	addEvent(document, 'click', function (event) {
		var element = getClickableElement(event.target);
		var category, action, label, label2, link;
		if (!element) {
			return;
		}
		category = getStructure(element).join('-');
		action = (element.nodeName == 'BUTTON')?'button':(
			element.href.indexOf('.pdf') > -1
			|| element.href.indexOf('.mov') > -1
			|| element.href.indexOf('.avi') > -1
			|| element.href.indexOf('.m4v') > -1
			|| element.href.indexOf('.wmv') > -1
			|| element.href.indexOf('.mp3') > -1
			|| element.href.indexOf('.rar') > -1
			|| element.href.indexOf('.zip') > -1
			|| element.href.indexOf('.xlsx') > -1
		) ? 'download' : (
			element.href.indexOf('.html') > -1
			|| element.href.indexOf('.txt') > -1
			|| element.href.indexOf('.js') > -1
		) ? 'example' : 'link';
		label = element.innerHTML;
		label2 = element.innerText;

		link = (element.nodeName == 'BUTTON')?element.textContent:element.href;

        _VGW_DATA.e_nm = label2;
        _VGW_DATA.e_tag = action;
        _VGW_DATA.e_desc = link;
        _VGW_DATA.e_stct = category;
        
        _vgw_callTracker('action');
	});
	function addEvent(obj, type, fn) {
		if (obj.addEventListener) {
			obj.addEventListener(type, fn, false);
		} else if (obj.attachEvent) {
			obj["e" + type + fn] = fn;
			obj[type + fn] = function() {
				obj["e" + type + fn](window.event);
			}
			obj.attachEvent("on" + type, obj[type + fn]);
		}
	}
	function getStructure(el) {
		var structure = [];
		if (el.parentNode && el.parentNode.tagName.toLowerCase() != 'body') {
			structure = getStructure(el.parentNode);
		}
		if (el.id) {
			structure.push(el.id);
		} else if (el.className) {
			structure.push(el.className);
		}
		return structure;
	}
	function getClickableElement(element) {
		if (element.tagName == undefined) {
			return false;
		}
		if (element.tagName.toLowerCase() == 'a' || element.tagName.toLowerCase() == 'area' || element.tagName.toLowerCase() == 'button') {
			return element;
		}
		if (element.parentNode) {
			return getClickableElement(element.parentNode);
		}
		return false;
	}


})();
