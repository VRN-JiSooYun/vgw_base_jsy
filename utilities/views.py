from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from utilities.functions import *
# from home.function_common import checkStructureAuthority
# from project.functions import *
# from inventory.functions import *
# Create your views here.


@login_required(login_url='/security/login/')
def utilities_home_view(request) :

    return redirect('utilities-solubility-view')

@login_required(login_url='/security/login/')
def utilities_solubility_view(request) :

    context = {
    }
    return render(request, 'utilities/prediction_solubility.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_solubility_api(request) :
    data1 = chemaxon_solubility(request)
    data2 = chemaxon_solubility_ext1(request)
    data = {
        "logs" : json.loads(data1),
        "mm" : json.loads(data2)
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_pka_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_pka.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_pka_api(request) :
    data1 = chemaxon_pka(request)
    data2 = chemaxon_pka_distribution(request)
    data = {
        "info" : json.loads(data1[0]),
        "svg_img" : data1[1],
        "temps" : data1[2],
        "distribution" : json.loads(data2[0]),
        "distribution_svg_imgs": data2[1],
        "distribution_smiles": data2[2],
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_logd_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_logd.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_logd_api(request) :
    logd = chemaxon_logd(request)
    logp = chemaxon_logp(request)
    data = {
        "logd" : json.loads(logd),
        "logp" : json.loads(logp[0]),
        "svg_img" : logp[1],
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/security/login/')
def utilities_combination_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_combination.html', context)


###################################################################
#                             Charge                              #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_charge_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_charge.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_charge_api(request) :
    charge = chemaxon_charge(request)
    data = {
        "charge" : json.loads(charge[0]),
        "form_svg_img" : charge[1],
        "total_svg_img" : charge[2],
    }
    return JsonResponse(data, safe=False)


###################################################################
#                             hERG                                #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_herg_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_herg.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_herg_api(request) :
    herg_act = chemaxon_herg_activity(request)
    herg_class = chemaxon_herg_class(request)
    data = {
        "herg_act" : json.loads(herg_act),
        "herg_class" : json.loads(herg_class),
    }
    return JsonResponse(data, safe=False)

###################################################################
#                   Pola Surface Area(PSA)                        #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_psa_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_psa.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_psa_api(request) :
    psa = chemaxon_psa(request)
    data = {
        "psa" : json.loads(psa),
    }
    return JsonResponse(data, safe=False)

###################################################################
#                  H-bond donors/acceptors                        #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_hbda_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_hbda.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_hbda_api(request) :
    hbda = chemaxon_hbda(request)
    data = {
        "hbda" : json.loads(hbda),
    }
    return JsonResponse(data, safe=False)

###################################################################
#                             CNS MPO                             #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_cns_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_cns.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_cns_api(request) :
    cns = chemaxon_cns(request)
    data = {
        "cns" : json.loads(cns),
    }
    return JsonResponse(data, safe=False)

###################################################################
#                       Elemental Analysis                        #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_elemental_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_elemental.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_elemental_api(request) :
    cns = chemaxon_elemental(request)
    data = {
        "elemental" : json.loads(cns),
    }
    return JsonResponse(data, safe=False)


###################################################################
#                   tautomerization_dominant                      #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_tautomer_domi_view(request) :
    context = {
    }
    return render(request, 'utilities/calculate_tautomer_domi.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_tautomer_domi_api(request) :
    rtn = chemaxon_tautomer_domi(request)
    data = {
        "tautomer" : json.loads(rtn),
    }
    return JsonResponse(data, safe=False)



###################################################################
#                             API                                 #
###################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_api_view(request) :
    admin = False
    data = getCalculatorAPI(request)
    if request.user.is_superuser :
        admin = True
    current_url = request.META.get('wsgi.url_scheme')+"://"+request.META.get('HTTP_HOST')
    http_host = request.META.get('HTTP_HOST')
    context = {
        'datas':data,
        'admin':admin,
        'current_url':current_url,
        'http_host':http_host
    }
    return render(request, 'utilities/calculate_api.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_get_api(request) :
    data = getCalculatorToken(request)
    return JsonResponse(data, safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_api_create(request) :
    data = createCalculatorToken(request)
    return JsonResponse(data, safe=False)

@csrf_exempt
def utilities_api(request) :
    token = request.headers.get('Voronoi-Token')
    token_validation, token_obj, limit_count = getApiTokenCheck(token)
    result_code = '0000'
    result_msg = 'success'
    result = None
    if token == None :
        result_code = "1111"
        result_msg = "Missing Token."
    elif not token_validation :
        result_code = "2222"
        result_msg = "Token is not valid."
    else :
        api_type = request.POST.get('t')
        smiles = request.POST.get('s')
        if api_type == None :
            result_code = "3333"
            result_msg = "API Type is not defined."
        elif smiles == None :
            result_code = "4444"
            result_msg = "Smiles is not defined."
        elif limit_count <= 0 :
            result_code = "5555"
            result_msg = "The number of API calls has been limited."
        else :
            if result_code == '0000' :
                try :
                    if api_type == 'pka' :
                        rtn, svg_img, temps = chemaxon_pka(request)
                        result = json.loads(rtn)

                    elif api_type == 'pka-dist' :
                        rtn, svg_imgs, smileses = chemaxon_pka_distribution(request)
                        result = json.dumps(smileses)
                        result = {
                            'smiles':json.loads(json.dumps(smileses)),
                            'distribution':json.loads(rtn)
                        }
                    elif api_type == 'solubility' :
                        unit = request.POST.get('u')
                        if unit == None :
                            result_code = "8888"
                            result_msg = "unit is not defined."
                        else :
                            rtn = chemaxon_solubility_ext2(request)
                            result = json.loads(rtn)

                    elif api_type == 'logd' :
                        rtn = chemaxon_logd(request)
                        result = rtn

                    elif api_type == 'logp' :
                        rtn = chemaxon_logp(request)
                        result = rtn

                    elif api_type == 'charge' :
                        ph = request.POST.get('p')
                        if ph == None :
                            result_code = "7777"
                            result_msg = "pH is not defined."
                        else :
                            rtn, form_svg_img, total_svg_img = chemaxon_charge(request)
                            result = json.loads(rtn)

                    elif api_type == 'herg-act' :
                        rtn = chemaxon_herg_activity(request)
                        result = json.loads(rtn)

                    elif api_type == 'herg-class' :
                        rtn = chemaxon_herg_class(request)
                        result = json.loads(rtn)

                    elif api_type == 'psa' :
                        ph = request.POST.get('p')
                        if ph == None :
                            result_code = "7777"
                            result_msg = "pH is not defined."
                        else :
                            rtn = chemaxon_psa(request)
                            result = json.loads(rtn)

                    elif api_type == 'hbda' :
                        ph = request.POST.get('p')
                        if ph == None :
                            result_code = "7777"
                            result_msg = "pH is not defined."
                        else :
                            rtn = chemaxon_hbda(request)
                            result = json.loads(rtn)

                    elif api_type == 'cns' :
                        rtn = chemaxon_cns(request)
                        result = json.loads(rtn)

                    elif api_type == 'elemental' :
                        operations = request.POST.get('o')
                        if operations == None :
                            result_code = "9000"
                            result_msg = "operations is not defined."
                        else :
                            rtn = chemaxon_elemental(request)
                            result = json.loads(rtn)

                    elif api_type == 'tautomer-dominant' :
                        rtn = chemaxon_tautomer_domi(request)
                        result = json.loads(rtn)


                    else :
                        result_code = "6666"
                        result_msg = "This type is not yet implemented."

                    if result_code == "0000" :
                        setApiTokenUseCount(token, limit_count)
                        ip = get_client_ip(request)
                        setApiStatus(token_obj, api_type, smiles, ip)
                except Exception as e:
                    print(e)
                    result_code = "9999"
                    result_msg = "The data you passed seems to be incorrect.(smiles,,)"
                    pass


    data = {
        'result_code':result_code,
        'result_msg':result_msg,
    }
    if result_code == '0000' :
        data['result'] = result
    return JsonResponse(data, safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_api_update(request):
    updateApiToken(request)
    data = {
        'result_code':'0000',
        'result_msg':'success'
    }
    return JsonResponse(data, safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_api_delete(request) :
    deleteApiToken(request)
    data = {
        'result_code':'0000',
        'result_msg':'success'
    }
    return JsonResponse(data, safe=False)


@login_required(login_url='/security/login/')
def utilities_etc_view(request) :
    # d = checkStructureAuthority(request, 'VNA100000')
    # print("D::",d)
    context = {
    }
    return render(request, 'utilities/calculate_etc.html', context)


@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_etc_operation(request) :
    datas = compound_v2_property_caclulate(request)
    data = {
        "result" : datas,
    }
    return JsonResponse(data, safe=False)


@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_etc_caco2(request) :
    datas = compound_caco2_caclulate(request)
    data = {
        "result" : datas,
    }
    return JsonResponse(data, safe=False)



@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_etc_enzyme_lle(request) :
    datas = enzyme_lle_caclulate(request)
    data = {
        "result" : datas,
    }
    return JsonResponse(data, safe=False)


@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_etc_solubility(request) :
    datas = compound_solubility_caclulate(request)
    data = {
        "result" : datas,
    }
    return JsonResponse(data, safe=False)


############################################################################
############              Cell Mutation             ############
############################################################################
@login_required(login_url='/security/login/')
def cell_mutation_view(request) :
    if request.method == 'GET':
        return render(request, 'utilities/cell_mutation.html', {
            'columns': getCellMutationColumns(request)['columns'],
            'lineages': getCellMutationColumns(request)['lineages']
        })
    if request.method == 'POST':
        actionType = request.POST.get('actionType')
        print("cell_mutation_view:" + actionType)

        if actionType == 'PARTIAL-SEARCH':
            process = searchCellMutation(request)

        if actionType == 'TOTAL-SEARCH':
            process = totalSearchCellMutation(request)

        if actionType == 'UPLOAD':
            process = uploadCellMutation(request)

        if actionType == 'AUTOCOMPLETE':
            process = getAutocompleteList(request)

        return JsonResponse(process, safe=False)

@login_required(login_url='/security/login/')
def cell_mutation_download(request) :
    return downloadCellMutation(request)

############################################################################
############              Cell Line Selector             ############
############################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def cell_line_selector_view(request) :
    if request.method == 'GET':
        total_num_sets = 0
        rows = CellLineSelectorGeneNormalStructure.objects.raw(f"""
            select 1 as id, category, count("set") from (
                select distinct on (category, "set") * from cell_line_selector_gene_normal_structure
                where check_display=true and check_discard=false
            ) t1
            group by category;
        """)

        normal_list = []

        for row in rows:
            total_num_sets += row.count
            normal_list.append({'category': row.category, 'count': row.count, 'tree_dict': getCellLineSelectorGeneList(structure='normal', category=row.category)})

        rows = CellLineSelectorGeneTreeStructure.objects.raw(f"""
            select 1 as code, category, count(code) from cell_line_selector_gene_tree_structure
            where check_display=true and check_discard=false
            group by category;
        """)

        tree_list = []

        for row in rows:
            total_num_sets += row.count
            tree_list.append({'category': row.category, 'count': row.count, 'tree_dict': json.dumps(getCellLineSelectorGeneList(structure='tree', category=row.category))})

        total_num_genes = 0
        gene_count_list = CellLineSelectorGeneCount.objects.all()
        for row in gene_count_list:
            total_num_genes += row.num_children

        return render(request, 'utilities/cell_line_selector.html', {
            'total_num_sets': total_num_sets,
            'total_num_genes': total_num_genes,
            'gene_normal_structure': normal_list,
            'gene_tree_structure': tree_list,
            'thread_list': CellLineSelectorChatGptThread.objects.filter(Q(owner_id=request.user.id) & Q(check_discard=False)).order_by('-id'),
            'cell_names_map': CellLineSelectorCellMappingId.objects.all()
        })
    if request.method == 'POST':
        actionType = request.POST.get('actionType')
        print("cell_line_selector_view:" + actionType)

        if actionType == 'CHECK-PRESAVED-DATA':
            process = checkPresavedData(request)

        if actionType == 'SEARCH' or actionType == 'CHANGE-PERCENTILE':
            process = cellLineSelectorSearch(request)
        
        if actionType == 'PRESAVE-RESULT':
            process = presaveResults(request)
        
        if actionType == 'CHANGE-FEATURE':
            process = cellLineSelectorChangeFeatures(request)
        
        if actionType == 'UPLOAD':
            process = uploadCellLineSelectorGene(request)
        
        if actionType == 'GET-GENE-LIST':
            process = getCellLineSelectorGeneList(request)
        
        if actionType == 'CHECK-KEYWORD-FROM-DEPMAP':
            process = checkKeywordFromDepmap(request)

        if actionType == 'FILTER-GENE-LIST':
            process = filterCellLineSelectorGeneList(request)
        
        if actionType == 'GET-CHILDREN-NUM':
            process = getMatchingCellLineSelectorGeneNum(request)
        
        if actionType == 'GET-CHILDREN-GENE-LIST':
            process = getChildrenGeneList(request)
        
        if actionType == 'GPT':
            process = cellLineSelectorChatGpt(request)
        
        if actionType == 'GET-GPT-MESSAGES':
            process = getGptMessages(request)
        
        if actionType == 'ADD-TRACKING-DATA':
            process = addTrackingData(request)

        return JsonResponse(process, safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def cell_line_selector_download(request) :
    return downloadSection(request)


############################################################################
############              Deep learning Solubilty               ############
############################################################################

# view
@login_required(login_url='/security/login/')
def utilities_deep_learning_solubility_view(request) :
    context = {
        "datas": getInventroyCompoundList(request),
    }
    return render(request, 'utilities/deep_learning_solubility.html', context)

# api
@csrf_exempt
def get_solubility_predit(request) :
  return JsonResponse(getSolubilityPredit(request), safe=False)

@csrf_exempt
def get_solubility_predit_file(request) :
  return JsonResponse(getSolubilityPreditFile(request), safe=False)

############################################################################
############                       3DPSA                        ############
############################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_3dpsa_view(request) :
    datas = None
    context = {
        "datas":datas,
    }
    return render(request, 'utilities/calculate_3dpsa.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_3dpsa_search(request) :
    data = get3dpsaDatas(request)
    return JsonResponse(
        data
    , safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_3dpsa_register(request) :
    data = set3dpsaData(request)
    return JsonResponse(
        data
    , safe=False)

############################################################################
############                        ESOL                        ############
############################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_esol_view(request) :
    datas = None
    context = {
        "datas":datas,
    }
    return render(request, 'utilities/calculate_esol.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_esol_search(request) :
    data = getEsolDatas(request)
    return JsonResponse(
        data
    , safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_esol_register(request) :
    data = setEsolData(request)
    return JsonResponse(
        data
    , safe=False)

############################################################################
######                         Deep Solubility                        ######
############################################################################
@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_deep_solubility_view(request) :
    datas = None
    context = {
        "datas":datas,
    }
    return render(request, 'utilities/calculate_deep_solubility.html', context)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_deep_solubility_search(request) :
    data = getDeepSolubilityDatas(request)
    return JsonResponse(
        data
    , safe=False)

@login_required(login_url='/security/login/')
@csrf_exempt
def utilities_deep_solubility_register(request) :
    data = setDeepSolubilityData(request)
    return JsonResponse(
        data
    , safe=False)
