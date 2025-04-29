import requests
import json
import datetime
from django.conf import settings
from urllib import parse
# from hr.models import *
# from dashboard.models import *
# from hr.functions import initiate_authority_for_superuser
# from home.functions import *
from django.db import connection, transaction
from utilities.models import *
from rdkit import Chem
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, AllChem, rdDepictor, MolsFromPNGString, DataStructs
from rdkit.Chem.Draw import MolsToImage, MolsToGridImage, MolToFile, rdMolDraw2D, MolToImageFile
from rdkit.Chem.SaltRemover import SaltRemover
from rdkit.Chem import rdTautomerQuery
import string
import random
from django.http import StreamingHttpResponse, HttpResponse
# import http.client
from django.core.files.storage import default_storage  # file save
# from compoundbank.crypt_vgw import *
from django.core.exceptions import ValidationError
import time
import math
import pandas as pd
from openpyxl import Workbook

# Target finder
from django.db import connection
# from kpviewer.models import KinaseProfilingAssayResult
# from home.function_common import checkStructureAuthority
from django.forms.models import model_to_dict
import markdown as md
import openpyxl
from django.db.models import Q, Count, F, Value, Max
import ast
from collections import defaultdict
from collections import Counter
import zipfile
from sys import platform
import io

import numpy as np
import matplotlib.pyplot as plt

# from compoundbank.functions_tmp import get_scaled_mol, moltosvg


def chemaxon_solubility(request) :
    # host = request._current_scheme_host
    # if '110.15.60.66:30080' in host or '192.168.1.5' in host or 'voronoi.app' in host :
    #     url = "http://192.168.1.177:8080/jws-calculations/rest-v1/calculator/calculate/solubility"
    # else :
    #     url = "http://110.15.60.66:25600/jws-calculations/rest-v1/calculator/calculate/solubility"

    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/solubility"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "phSequence": {
            "pHLower": 0.0,
            "pHStep": 0.1,
            "pHUpper": 15.0
        },
        "structure": s,
        "unit": "LOGS"
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter( Q(check_discard=False) ).last()
    solubility = SolubilityHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(unit='LOGS') & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if solubility is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'unit':'LOGS',
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = SolubilityHistory.objects.create(**data)

        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = solubility.response_data
        json_object = json.loads(rtn)
        version = json_object.get('version')


    # print(rtn)

    return rtn

def chemaxon_solubility_by_smiles(smiles) :
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/solubility"

    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "phSequence": {
            "pHLower": 0.0,
            "pHStep": 0.1,
            "pHUpper": 15.0
        },
        "structure": s,
        "unit": "LOGS"
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter( Q(check_discard=False) ).last()
    solubility = SolubilityHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(unit='LOGS') & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if solubility is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'unit':'LOGS',
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = SolubilityHistory.objects.create(**data)

        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = solubility.response_data
        json_object = json.loads(rtn)
        version = json_object.get('version')


    # print(rtn)

    return rtn


def chemaxon_solubility_ext1(request) :
    # host = request._current_scheme_host
    # if '110.15.60.66:30080' in host or '192.168.1.5' in host or 'voronoi.app' in host :
    #     url = "http://192.168.1.177:8080/jws-calculations/rest-v1/calculator/calculate/solubility"
    # else :
    #     url = "http://110.15.60.66:25600/jws-calculations/rest-v1/calculator/calculate/solubility"

    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/solubility"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "phSequence": {
            "pHLower": 0.0,
            "pHStep": 0.1,
            "pHUpper": 15.0
        },
        "structure": s,
        "unit": "UM"
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    solubility = SolubilityHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(unit='UM') & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if solubility is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'unit':'UM',
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = SolubilityHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = solubility.response_data

    json_object = json.loads(rtn)
    version = json_object.get('version')

    # print(rtn)

    return rtn

def chemaxon_solubility_ext2(request) :
    # host = request._current_scheme_host
    # if '110.15.60.66:30080' in host or '192.168.1.5' in host or 'voronoi.app' in host :
    #     url = "http://192.168.1.177:8080/jws-calculations/rest-v1/calculator/calculate/solubility"
    # else :
    #     url = "http://110.15.60.66:25600/jws-calculations/rest-v1/calculator/calculate/solubility"

    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/solubility"

    unit = request.POST.get('u')
    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "phSequence": {
            "pHLower": 0.0,
            "pHStep": 0.1,
            "pHUpper": 15.0
        },
        "structure": s,
        "unit": unit
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    solubility = SolubilityHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(unit=unit) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if solubility is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'unit':'UM',
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = SolubilityHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = solubility.response_data

    json_object = json.loads(rtn)
    version = json_object.get('version')

    # print(rtn)

    return rtn


########################################################
#                       pKa                            #
########################################################
def chemaxon_pka(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/pka"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/pka"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    temps = 298
    payload = json.dumps({
        "inputFormat": "smiles",
        "micro": False,
        "outputFormat": "mol",
        "outputStructureIncluded": True,
        "pKaLowerLimit": -20,
        "pKaUpperLimit": 10,
        "prefix": "DYNAMIC",
        "structure": s,
        "temperature": temps,
        "types": "pKa, acidic, basic"
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    pka = PkaHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if pka is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = PkaHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = pka.response_data

    svg_img = ''
    json_object = json.loads(rtn)
    molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    atomIdx = 0
    for atom in molFromSmiles.GetAtoms() :
        for pkaValue in json_object.get('pkaValuesByAtom') :
            if pkaValue.get('atomIndex') == atomIdx :
                atom.SetProp('atomNote',str(pkaValue.get('value')))
        atomIdx += 1

    if molFromSmiles is not None:
        svg_img = moltosvg(molFromSmiles)

    # print(rtn)
    return rtn, svg_img, temps

def chemaxon_pka_by_smiles(smiles) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/pka"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/pka"

    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    temps = 298
    payload = json.dumps({
        "inputFormat": "smiles",
        "micro": False,
        "outputFormat": "mol",
        "outputStructureIncluded": True,
        "pKaLowerLimit": -20,
        "pKaUpperLimit": 10,
        "prefix": "DYNAMIC",
        "structure": s,
        "temperature": temps,
        "types": "pKa, acidic, basic"
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    pka = PkaHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if pka is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = PkaHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = pka.response_data

    svg_img = ''
    json_object = json.loads(rtn)
    molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    atomIdx = 0
    for atom in molFromSmiles.GetAtoms() :
        for pkaValue in json_object.get('pkaValuesByAtom') :
            if pkaValue.get('atomIndex') == atomIdx :
                atom.SetProp('atomNote',str(pkaValue.get('value')))
        atomIdx += 1

    if molFromSmiles is not None:
        svg_img = moltosvg(molFromSmiles)

    # print(rtn)
    return rtn, svg_img, temps

def chemaxon_pka_distribution(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/pka-distribution"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/pka-distribution"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "considerTautomerization": True,
        "inputFormat": "smiles",
        "pKaLowerLimit": -20,
        "pKaUpperLimit": 10,
        "phSequence": {
            "pHLower": 0.0,
            "pHStep": 0.1,
            "pHUpper": 15.0
        },
        "resultMoleculeFormat": "mol",
        "structure": s,
        "temperature": 298
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    pkaDistribution = PkaDistributionHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if pkaDistribution is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = PkaDistributionHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = pkaDistribution.response_data

    # print(rtn)

    json_object = json.loads(rtn)
    structures = json_object.get('structures')

    svg_imgs = []
    smileses = []

    for s in structures :
        molFromSmiles = Chem.MolFromMolBlock(s)
        smile = Chem.MolToSmiles(molFromSmiles)
        svg_img = moltosvg(molFromSmiles)
        svg_imgs.append(svg_img)
        smileses.append(smile)

    return rtn, svg_imgs, smileses


########################################################
#                      LogD, LogP                      #
########################################################
def chemaxon_logd(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/logd"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/logd"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    temps = 298
    payload = json.dumps({
        "inputFormat": "smiles",
        "phSequence": {
            "pHLower": 0.0,
            "pHStep": 0.1,
            "pHUpper": 15.0
        },
    "structure": s
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    logd = LogdHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if logd is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = LogdHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = logd.response_data

    # print(rtn)
    return rtn

def chemaxon_logp(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/logp"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/logp"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "atomIncrements": True,
        "inputFormat": "smiles",
        "method": "CHEMAXON",
        "structure": s
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    logp = LogpHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if logp is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != None or status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = LogpHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = logp.response_data

    svg_img = ''
    json_object = json.loads(rtn)
    molFromSmiles = Chem.MolFromSmiles(s)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    atomIdx = 0
    for atom in molFromSmiles.GetAtoms() :
        for atomValue in json_object.get('logPByAtom') :
            if atomValue.get('atomIndex') == atomIdx :
                atom.SetProp('atomNote',str(atomValue.get('value')))
        atomIdx += 1

    if molFromSmiles is not None:
        svg_img = moltosvg(molFromSmiles)

    # print(rtn)
    return rtn, svg_img


def chemaxon_charge(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/charge"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/charge"

    ph = request.POST.get("p")
    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "ph": float(ph),
        "structure": s
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    charge = ChargeHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(ph=float(ph)) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if charge is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'ph' : ph,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = ChargeHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = charge.response_data

    form_svg_img = ''
    total_svg_img = ''
    json_object = json.loads(rtn)
    molFromSmiles = Chem.MolFromSmiles(s)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    atomIdx = 0
    for atom in molFromSmiles.GetAtoms() :
        for atomValue in json_object.get('formalChargeByAtom') :
            if atomValue.get('atomIndex') == atomIdx :
                atom.SetProp('atomNote',str(atomValue.get('value')))
        atomIdx += 1

    if molFromSmiles is not None:
        form_svg_img = moltosvg(molFromSmiles)

    atomIdx = 0
    molFromSmiles = Chem.MolFromSmiles(s)
    for atom in molFromSmiles.GetAtoms() :
        for atomValue in json_object.get('totalChargeByAtom') :
            if atomValue.get('atomIndex') == atomIdx :
                atom.SetProp('atomNote',str(atomValue.get('value')))
        atomIdx += 1

    if molFromSmiles is not None:
        total_svg_img = moltosvg(molFromSmiles)

    # print(rtn)
    return rtn, form_svg_img, total_svg_img


def chemaxon_herg_activity(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/herg-activity"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/herg-activity"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "outputFormat": "mol",
        "structure": s
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    charge = HergActivityHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if charge is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = HergActivityHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = charge.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    mols = json_object.get('mostSimilars')
    for mol in mols :
        molFromSmiles = Chem.MolFromMolBlock(mol.get('structure'))
        smiles = Chem.MolToSmiles(molFromSmiles)
        svg_img = moltosvg(molFromSmiles)
        mol['svg_img'] = svg_img
        mol['smiles'] = smiles

    # print(rtn)
    return json.dumps(json_object)



def chemaxon_herg_class(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/herg-class"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/herg-class"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "outputFormat": "mol",
        "structure": s
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    charge = HergClassHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if charge is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = HergClassHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = charge.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    mols = json_object.get('mostSimilars')
    for mol in mols :
        molFromSmiles = Chem.MolFromMolBlock(mol.get('structure'))
        smiles = Chem.MolToSmiles(molFromSmiles)
        svg_img = moltosvg(molFromSmiles)
        mol['svg_img'] = svg_img
        mol['smiles'] = smiles

    # print(rtn)
    return json.dumps(json_object)

def chemaxon_psa(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/polar-surface-area"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/polar-surface-area"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    ph = request.POST.get("p")
    payload = json.dumps({
        "excludePhosphorus": True,
        "excludeSulfur": True,
        "inputFormat": "smiles",
        "outputFormat": "smiles",
        "outputStructureIncluded": False,
        "pH": float(ph),
        "structure": s
    })
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    psa = PolaSurfaceAreaHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(ph=float(ph)) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if psa is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        if status != 200 :
            checkDiscard = True
        data = {
            'smiles' : s,
            'ph' : ph,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = PolaSurfaceAreaHistory.objects.create(**data)
        if status == 200 and version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = psa.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    print(rtn)
    return json.dumps(json_object)

def chemaxon_hbda(request) :
    #url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/hbda"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/hbda"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    ph = request.POST.get("p")
    payload = json.dumps({
        "excludeHalogens": True,
        "excludeSulfur": True,
        "inputFormat": "smiles",
        "outputFormat": "smiles",
        "outputStructureIncluded": False,
        "pH": float(ph),
        "structure": s
    })

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    hbda = HbondDonorHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(ph=float(ph)) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if hbda is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'ph' : ph,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = PolaSurfaceAreaHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = hbda.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    print(rtn)
    return json.dumps(json_object)

def chemaxon_hbda(request) :
    #url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/hbda"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/hbda"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    ph = request.POST.get("p")
    payload = json.dumps({
        "excludeHalogens": True,
        "excludeSulfur": True,
        "inputFormat": "smiles",
        "outputFormat": "smiles",
        "outputStructureIncluded": False,
        "pH": float(ph),
        "structure": s
    })

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    hbda = HbondDonorHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(ph=float(ph)) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if hbda is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'ph' : ph,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = HbondDonorHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = hbda.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    print("hbda", rtn)
    return json.dumps(json_object)

def chemaxon_elemental(request) :
    #url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/elemental-analysis"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/elemental-analysis"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    o = request.POST.get("o")
    payload = json.dumps({
        "inputFormat": "smiles",
        "operations": o,
        "structure": s,
        "symbolID": True
    })

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    elemental = ElementalAnalysisHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(operations=o) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if elemental is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'operations' : o,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = ElementalAnalysisHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = elemental.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    print("elemental", rtn)
    return json.dumps(json_object)

def chemaxon_cns(request) :
    #url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/cns-mpo"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/cns-mpo"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "structure": s
    })

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    cns = CnsMpoHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if cns is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = CnsMpoHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = cns.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    print("CNS", rtn)
    return json.dumps(json_object)

def chemaxon_cns_by_smiles(smiles) :
    #url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/cns-mpo"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/cns-mpo"

    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "structure": s
    })

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    cns = CnsMpoHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if cns is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = CnsMpoHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = cns.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))

    print("CNS", rtn)
    return json.dumps(json_object)

def chemaxon_tautomer_domi(request) :
    # url = "https://jchem-microservices.chemaxon.com/jws-calculations/rest-v1/calculator/calculate/tautomerization-dominant"
    url = "https://api.calculators.cxn.io/rest-v1/calculator/calculate/tautomerization-dominant"

    smiles = request.POST.get('s')
    mol = Chem.MolFromSmiles(smiles)
    s = Chem.MolToSmiles(mol)
    payload = json.dumps({
        "inputFormat": "smiles",
        "resultMoleculeFormat": "smiles",
        "structure": s
    })


    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'x-api-key': 'iHMKLxgl0N7afsOd3YCmujTSh4kaB1jo80zCr3RY'
    }

    apiVersion = ChemaxonVersion.objects.filter(Q(check_discard=False)).last()
    tautomer = TautomerizationDominantHistory.objects.filter(Q(check_discard=False) & Q(smiles=s) & Q(api_version=apiVersion.api_version)).last()

    rtn = {}
    version = ''
    if tautomer is None :
        response = requests.request("POST", url, headers=headers, data=payload)
        rtn = response.text
        json_object = json.loads(rtn)
        version = json_object.get('version')
        status = json_object.get('status')
        checkDiscard = False
        # if status != 200 :
        #     checkDiscard = True
        data = {
            'smiles' : s,
            'response_data':response.text,
            'api_version':version,
            'check_discard':checkDiscard,
            'date_created':datetime.datetime.now(),
            'date_updated':datetime.datetime.now(),
        }
        obj = TautomerizationDominantHistory.objects.create(**data)
        # if status == 200 and version != apiVersion.api_version :
        if version != apiVersion.api_version :
            versionData = {
                'check_discard':True,
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.filter(Q(id=apiVersion.id)).update(**versionData)
            versionData = {
                'api_version':version,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now(),
            }
            obj = ChemaxonVersion.objects.create(**versionData)
    else :
        rtn = tautomer.response_data

    json_object = json.loads(rtn)
    # molFromSmiles = Chem.MolFromMolBlock(json_object.get('structure'))


    structures = json_object.get('structureDistribution')
    rtns = {}
    imgs = []
    for structure in structures :
        s = structure.get("S")
        molFromSmiles = Chem.MolFromSmiles(s)
        svg_img = moltosvg(molFromSmiles)
        imgs.append(svg_img)

    json_object['imgs'] = imgs

    print("Tautomerization Dominant", rtn)
    return json.dumps(json_object)
    # return json.dumps(rtns)


'''
def moltosvg(mol, kekulize=True):
    # print('moltosvg')
    mc = Chem.Mol(mol.ToBinary())
    if kekulize:
        try:
            Chem.Kekulize(mc)
        except:
            mc = Chem.Mol(mol.ToBinary())
    if not mc.GetNumConformers():
        rdDepictor.Compute2DCoords(mc)
    drawer = rdMolDraw2D.MolDraw2DSVG(500, 500)
    rdMolDraw2D.PrepareAndDrawMolecule(drawer, mol)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText()
    svg = svg.replace('500px', '100%', 2)
    return svg.replace('svg:','')
'''
########################################################
#                         API                          #
########################################################
def getCalculatorAPI(request):
    if request.user.is_superuser :
        data = CalculatorApiToken.objects.filter(Q(check_discard=False) ).all()
    else :
        data = CalculatorApiToken.objects.filter(Q(check_discard=False) & Q(owner_id=request.user.id)).all()

    return data


def createCalculatorToken(request) :
    data = {
        'name' : request.POST.get('api_name'),
        'token' : makeRandomString(32),
        'status' : 'active',
        'owner_name' : request.user.member.member_name,
        'owner_id' : request.user.id,
        'comment' : '',
        'limit_count' : 10000,
        'check_discard' : False,
        'date_created' : datetime.datetime.now(),
        'date_updated' : datetime.datetime.now(),
    }
    CalculatorApiToken.objects.create(**data)
    return data

def makeRandomString(len) :
    _LENGTH = len
    string_pool = string.ascii_letters + string.digits

    result = ""
    for i in range(_LENGTH) :
        result += random.choice(string_pool)
    return result


def getApiTokenCheck(token) :
    obj = CalculatorApiToken.objects.filter(Q(check_discard=False) & Q(token=token) & Q(status='active')).last()
    if obj == None :
        return False, None, 0
    else :
        return True, obj, obj.limit_count

def setApiTokenUseCount(token, count) :
    data = {
        'limit_count':count - 1
    }
    CalculatorApiToken.objects.filter(Q(check_discard=False) & Q(token=token) & Q(status='active')).update(**data)


def setApiStatus(token_obj, api_type, smiles, ip) :
    data = {
        'api_id':token_obj.id,
        'api_type':api_type,
        'smiles':smiles,
        'owner_id':token_obj.owner_id,
        'ip_addr':ip,
        'check_discard' : False,
        'date_created' : datetime.datetime.now(),
        'date_updated' : datetime.datetime.now(),
    }
    CalculatorApiStatus.objects.create(**data)

def updateApiToken(request) :
    api_id = request.POST.get('id')
    status = request.POST.get('st')
    limit_cnt = request.POST.get('l_cnt')
    api_name = request.POST.get('name')

    data = {
        'name':api_name,
        'status':status,
        'limit_count':limit_cnt,
        'date_updated' : datetime.datetime.now(),
    }
    CalculatorApiToken.objects.filter(Q(id=api_id)).update(**data)

def deleteApiToken(request) :
    api_id = request.POST.get('id')

    data = {
        'check_discard':True,
        'date_updated' : datetime.datetime.now(),
    }
    CalculatorApiToken.objects.filter(Q(id=api_id)).update(**data)

def getCalculatorToken(request) :
    api_id = request.POST.get('id')
    obj = CalculatorApiToken.objects.filter(Q(id=api_id)).last()
    data = {
        'name' : obj.name,
        'token' : obj.token,
        'status' : obj.status,
        'owner_id' : obj.owner_id,
        'comment' : obj.comment,
        'limit_count' : obj.limit_count,
    }
    return data

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


############################################################################
############          compound v2 preperty calculator           ############
############################################################################
def compound_v2_property_caclulate(request) :
    if request.user.email != "k3363@voronoi.io" :
        return {
            "code":"1111",
            "msg":"This account can't use this function."
        }

    # compounds = Design_Compound_V2.objects.all().filter(Q(id__gt=13516) & Q(num_h_bond_donors_site=None)).order_by('id')
    compounds = Design_Compound_V2.objects.all().filter( Q(compound_code__in=['BTS002974','BTS002975']) ).order_by('id')

    i = 0
    for compound in compounds :
        # # # 배포전 주석처리해야 함.
        # if i > 10 :
        #     break

        # vehicle
        if compound.compound_code == "VNA100000" or compound.compound_code == "VNA000000" :
            continue
        try:
            with transaction.atomic():
                compound_code = compound.compound_code
                smiles = decryptSmiles(compound.canonical_smiles)
                # encode_smiles = parse.quote(smiles, safe='()', encoding="utf-8")
                request.POST._mutable = True
                request.POST['s'] = smiles
                request.POST['o'] = None
                print("#############################################################################################################")
                print("compound_code::", compound_code)
                print("smiles::",smiles)
                #=====================================================================================================================
                # heavy_atom_count, fsp3, num_rotatable_bonds
                #=====================================================================================================================
                data = {
                    'heavy_atom_count': Descriptors.HeavyAtomCount(Chem.MolFromSmiles(smiles)),
                    'fsp3': Descriptors.FractionCSP3(Chem.MolFromSmiles(smiles)),
                    'num_rotatable_bonds': Descriptors.NumRotatableBonds(Chem.MolFromSmiles(smiles))
                }

                #=====================================================================================================================
                print(" chemaxon_solubility") # logS pH:7.4
                #=====================================================================================================================
                result = json.loads(chemaxon_solubility(request))
                for elem in result['phDependentSolubilities']:
                    if (elem['pH'] == 7.4):
                        data['log_s'] = elem['value']
                        break

                #=====================================================================================================================
                print(" chemaxon_pka") #  pKa(Basic), (Acidic)
                #=====================================================================================================================
                result = json.loads(chemaxon_pka(request)[0])
                print(result)
                data['basic_pka'] = result['maxBasicValue'] if 'maxBasicValue' in result else None
                data['acidic_pka'] = result['minAcidicValue'] if 'minAcidicValue' in result else None

                #=====================================================================================================================
                print(" chemaxon_cns") # logp, logd, mw, tpsa, CNS MPO score, pka
                #=====================================================================================================================
                result = json.loads(chemaxon_cns(request))

                data['cns_mpo_score'] = result['score']

                for elem in result['properties']:
                    if elem['name'] == 'logp':
                        data['log_p'] = elem['value']

                    elif elem['name'] == 'logd':
                        data['log_d'] = elem['value']

                    elif elem['name'] == 'mw':
                        data['molecular_weight'] = elem['value']

                    elif elem['name'] == 'tpsa':
                        data['topological_polar_surface_area'] = elem['value']

                    elif elem['name'] == 'hbd':
                        data['num_h_bond_donors'] = elem['value']

                    elif elem['name'] == 'pka':
                        data['pka'] = elem['value']

                #=====================================================================================================================
                print(" chemaxon_elemental") #  formula, exactMass, composition
                #=====================================================================================================================
                request.POST['o'] = "formula,exactMass,composition"
                result = json.loads(chemaxon_elemental(request))

                data['exact_mass'] = result['exactMass']
                data['chemical_formula'] = result['formula']
                composition = {}
                for elem in result['composition'].split(', '):
                    chemical = elem.split(' ')[0]
                    ratio = elem.split(' ')[1]
                    composition[chemical] = ratio

                data['composition'] = composition

                request.POST['o'] = None

                #=====================================================================================================================
                print(" chemaxon_hbda") # H-bond donors: 'donorAtomCount', H-bond acceptors: 'acceptorAtomCount'
                #=====================================================================================================================
                request.POST['p'] = 7.4
                result = json.loads(chemaxon_hbda(request))

                data['num_h_bond_donors'] = result['donorAtomCount']
                data['num_h_bond_donors_site'] = result['donorSiteCount']
                data['num_h_bond_acceptors'] = result['acceptorAtomCount']
                data['num_h_bond_acceptors_site'] = result['acceptorSiteCount']
                request.POST['p'] = None

                #=====================================================================================================================
                # Lipinski Rule of 5
                #=====================================================================================================================
                data['num_rule_of_5_violations'] = 0

                if data['exact_mass'] <= 500:
                    data['num_rule_of_5_violations'] += 1

                if data['log_p'] <= 5:
                    data['num_rule_of_5_violations'] += 1

                if data['num_h_bond_donors'] <= 5:
                    data['num_rule_of_5_violations'] += 1

                if data['num_h_bond_acceptors'] <= 10:
                    data['num_rule_of_5_violations'] += 1

                data['date_updated'] = datetime.datetime.now()
                print("properties from utils:", data)

                Design_Compound_V2.objects.filter(Q(compound_code=compound_code)).update(**data)

                '''
                objs = Design_Compound_Batch.objects.filter(Q(compound_code=compound_code))

                # mol_wt = cddResponse['molecule']['molecular_weight']
                mol_wt = data['molecular_weight']

                batch_list = []
                for obj in objs:
                    if obj.saltform_code == 'FREE' or obj.saltform_code == 'UNKNOWN':
                        formula_wt = mol_wt
                    else:
                        print("saltform_code:", obj.saltform_code)
                        saltfomObj = Design_Saltform.objects.filter(Q(check_discard=False) & Q(saltform_code=obj.saltform_code)).last()
                        if saltfomObj == None:
                            raise ValidationError("An error occurred with object: %(message)s", params={'result': False, 'message': 'saltform does not exist', 'saltform_code': obj.saltform_code})

                        mol_salt = Chem.MolFromSmiles(saltfomObj.smiles)
                        salt_wt = Descriptors.MolWt(mol_salt)
                        formula_wt = mol_wt + (1 if obj.saltform_count == None else obj.saltform_count) * salt_wt

                    obj.formular_weight = formula_wt
                    obj.salt_factor = formula_wt / mol_wt
                    obj.save()

                    batch_list.append({'batch_no': obj.batch_no, 'formular_weight': formula_wt, 'salt_factor': formula_wt / mol_wt})

                data['batch_list'] = batch_list
                '''

                print('data', data)
                rtn = {
                    'code':'0000',
                    'result': data,
                }

        except ValidationError as e:
            pass
            print("saveUtilityData::ValidationError", e.message)
            # return {
            #     'code': '2222',
            #     'msg': e
            # }
        except Exception as e :
            pass
            print("saveUtilityData::Exception:", e)
            # return {
            #     'code': '3333',
            #     'msg': e
            # }

        i+=1


    return {
        'code':'0000',
        'msg':i
    }


############################################################################
############              compound caco2 calculator             ############
############################################################################
def compound_caco2_caclulate(request) :
    if request.user.email != "k3363@voronoi.io" :
        return {
            "code":"1111",
            "msg":"This account can't use this function."
        }

    # compounds = Design_Compound_V2.objects.all().filter(Q(caco2=None)).order_by('id')
    # compounds = Design_Compound_V2.objects.all().filter(Q(canonical_smiles__isnull=False) & Q(molecular_weight__isnull=False)).order_by('id')
    compounds = Design_Compound_V2.objects.all().filter(Q(canonical_smiles__isnull=False) & Q(caco2__isnull=True)).order_by('id')
    # compounds = Design_Compound_V2.objects.all().filter(Q(canonical_smiles__isnull=False) & Q(vss__isnull=True)).order_by('id')
    i = 0

    url = ""
    if 'voronoi.app' in request.build_absolute_uri():
        # Prod
        url = "http://172.16.1.30:10001/api"
    elif '110.15.60.66:30080' in request.build_absolute_uri():
        # Stage
        url = "http://172.16.1.31:10001/api"
    else :
        # Devel
        url = "http://192.168.1.250:10001/api"

    for compound in compounds :
        # # 배포시 주석처리 해야 함.
        # if i > 20 :
        #     break

        compound_code = compound.compound_code
        if compound_code == "VNA100000" or compound_code == "VNA000000" :
            continue

        try:
            with transaction.atomic():

                print("############################################################################")
                print("compound_code::",compound_code)

                if compound.acidic_pka == None :
                    acidic_pka = "None"
                else :
                    acidic_pka = str(compound.acidic_pka)

                smiles = decryptSmiles(compound.canonical_smiles)
                print("smiles::",smiles)
                encode_smiles = parse.quote(smiles, safe='()', encoding="utf-8")
                payload = 'smiles='+encode_smiles+'&molwt='+str(compound.molecular_weight)+'&logd='+str(compound.log_d)+'&acidic_pka='+acidic_pka+'&basic_pka='+str(compound.basic_pka)+'&tpsa='+str(compound.topological_polar_surface_area)+'&logs='+str(compound.log_s)
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                print(payload)
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

                caco2_return = json.loads(response.text)
                caco2_return_code = caco2_return.get('result_code')

                if caco2_return_code == "0000" :
                    return_data = caco2_return.get('result')
                    caco2 = float(return_data[0])
                    hia = float(return_data[1])
                    vss = float(return_data[2])

                    if compound.caco2 == None :
                        data = {
                            'caco2' : caco2,
                            'hia' : hia,
                            'vss' : vss
                        }
                    else :
                        data = {
                            'hia' : hia,
                            'vss' : vss
                        }
                    Design_Compound_V2.objects.filter(Q(compound_code=compound_code)).update(**data)

        except ValidationError as e:
            pass
            print("compound_caco2_caclulate::ValidationError", e.message)
            # return {
            #     'code': '2222',
            #     'msg': e
            # }
        except Exception as e :
            pass
            print("compound_caco2_caclulate::Exception:", e)
            # return {
            #     'code': '3333',
            #     'msg': e
            # }

        i += 1

    return {
        'code':'0000',
        'msg':i
    }


def enzyme_lle_caclulate(request) :
    if request.user.email != "k3363@voronoi.io" :
        return {
            "code":"1111",
            "msg":"This account can't use this function."
        }

    enzymes = AssayEnzymeRequestDtl.objects.all().filter(Q(result_lle=None)).order_by("id")

    i = 0
    for enzyme in enzymes :
        # # 배포전 주석처리 해야 함.
        # if i > 10 :
        #     break

        try:
            with transaction.atomic():
                data = {}
                compound_name = enzyme.compound_name
                print("################################################################")
                print("compound::", compound_name)
                compound = Design_Compound_V2.objects.filter(Q(compound_code=compound_name)).last()

                if compound != None :
                    logD = compound.log_d
                    ic50 = enzyme.result

                    lle = 6-math.log10(ic50)-logD
                    print("lle::", lle)

                    data = {
                        'result_lle':lle,
                    }
                    AssayEnzymeRequestDtl.objects.filter(Q(id=enzyme.id)).update(**data)
                else :
                    print("Compound Not Found!!!!!!!!!")

        except Exception as e :
            pass
            print("enzyme_lle_caclulate::Exception:", e)

        i += 1

    return {
        'code':'0000',
        'msg':i
    }


############################################################################
############           compound solubility calculator           ############
############################################################################
def compound_solubility_caclulate(request) :
    if request.user.email != "k3363@voronoi.io" :
        return {
            "code":"1111",
            "msg":"This account can't use this function."
        }

    # compounds = Design_Compound_V2.objects.all().filter(Q(caco2=None)).order_by('id')
    # compounds = Design_Compound_V2.objects.all().filter(Q(canonical_smiles__isnull=False) & Q(molecular_weight__isnull=False)).order_by('id')
    compounds = Design_Compound_V2.objects.all().filter(Q(canonical_smiles__isnull=False) & Q(solubility__isnull=True)).order_by('id')
    # compounds = Design_Compound_V2.objects.all().filter(Q(canonical_smiles__isnull=False) & Q(vss__isnull=True)).order_by('id')
    i = 0

    url = ""
    if 'voronoi.app' in request.build_absolute_uri():
        # Prod
        url = "http://172.16.1.237:10007/api/solubility_predit"
    elif '110.15.60.66:30025' in request.build_absolute_uri():
        # Stage
        url = "http://172.16.1.237:10007/api/solubility_predit"
    else :
        # Devel
        url = "http://192.168.1.250:10007/api/solubility_predit"

    for compound in compounds :
        # # 배포시 주석처리 해야 함.
        # if i > 20 :
        #     break

        compound_code = compound.compound_code
        if compound_code == "VNA100000" or compound_code == "VNA000000" :
            continue

        try:
            with transaction.atomic():

                print("############################################################################")
                print("compound_code::",compound_code)

                smiles = decryptSmiles(compound.canonical_smiles)
                print("smiles::",smiles)
                encode_smiles = parse.quote(smiles, safe='()', encoding="utf-8")
                payload = 'smiles='+encode_smiles
                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }
                print(payload)
                response = requests.request("POST", url, headers=headers, data=payload)
                print(response.text)

                caco2_return = json.loads(response.text)
                caco2_return_code = caco2_return.get('result_code')

                if caco2_return_code == "0000" :
                    solubility = caco2_return.get('result')

                    data = {
                        'solubility' : solubility,
                    }

                    Design_Compound_V2.objects.filter(Q(compound_code=compound_code)).update(**data)

        except ValidationError as e:
            pass
            print("compound_solubility_caclulate::ValidationError", e.message)
            # return {
            #     'code': '2222',
            #     'msg': e
            # }
        except Exception as e :
            pass
            print("compound_solubility_caclulate::Exception:", e)
            # return {
            #     'code': '3333',
            #     'msg': e
            # }

        i += 1

    return {
        'code':'0000',
        'msg':i
    }


############################################################################
############              cell mutation                         ############
############################################################################

def searchCellMutation(request):
    cur = connection.cursor()
    numRowsPerPage = int(request.POST.get('num-rows-per-page'))
    pageNum = int(request.POST.get('page-no'))
    offset = (pageNum - 1) * numRowsPerPage

    filter_dict = json.loads(request.POST.get('filter_dict'))
    filter_str = ''

    target_column = request.POST.get('target_column')

    filter_group_conjunction_list = json.loads(request.POST.get('filter_group_conjunction_list'))

    print("searchCellMutation::numRowsPerPage:", str(numRowsPerPage),", pageNum:", str(pageNum),", offset:", str(offset))
    # print("filter_dict:", filter_dict)

    order_dict = json.loads(request.POST.get('order_dict'))
    order_str = ''

    for i, elem in enumerate(order_dict):
        column_name = elem['column_name']
        order = elem['order']

        expression = column_name + ' ' + order

        order_str += f" {expression} " + ('' if i == len(order_dict) - 1 else ',')
    print('order:"'+ order_str + '"')

    if target_column == 'cell_name':
        i = 0
        for key, filter_group in filter_dict.items():
            filter_group_str = ''
            print(key, ' : ', filter_group)
            if len(filter_group) > 0:
                for idx, elem in enumerate(filter_group):
                    print(elem)
                    column_type = elem['filter_column'].split('#')[0]
                    column_name = elem['filter_column'].split('#')[1]
                    column_name = column_name.split('.')[0] + str(i) + '.' + column_name.split('.')[1]
                    filter_condition = elem['filter_condition']
                    filter_conjunction = elem['filter_conjunction']
                    filter_value = elem['filter_value']
                    filter_group_condition = elem['filter_group_condition']

                    expression = filter_condition % (column_name, filter_value)
                    filter_group_str += f" {expression} " + ('' if idx == len(filter_group) - 1 else filter_conjunction)

                filter_str += f'''
                    {filter_group_condition} EXISTS (
                        SELECT 1 FROM cell_mutation mut{i}
                        LEFT JOIN cell_mutation_info info{i} ON mut{i}.cell_name=info{i}.cell_name
                        LEFT JOIN cell_mutation_hrd hrd{i} ON mut{i}.cell_name=hrd{i}.cell_name
                        LEFT JOIN cell_mutation_msi msi{i} ON mut{i}.cell_name=msi{i}.cell_name
                        WHERE mut.cell_name = mut{i}.cell_name
                        AND ({filter_group_str})
                    ) {('' if i == len(filter_dict) - 1 else filter_group_conjunction_list[i])}
                '''
            i += 1

        query = f"""
            SELECT mut.*
            FROM (
                SELECT DISTINCT ON (mut_inner.cell_name) info_inner.* FROM cell_mutation mut_inner
	            INNER JOIN cell_mutation_info info_inner ON info_inner.cell_name=mut_inner.cell_name
            ) mut
            LEFT JOIN cell_mutation_info info ON mut.cell_name=info.cell_name
            LEFT JOIN cell_mutation_hrd hrd ON mut.cell_name=hrd.cell_name
            LEFT JOIN cell_mutation_msi msi ON mut.cell_name=msi.cell_name
            WHERE mut.cell_name IS NOT NULL {' AND (' + filter_str + ') ' if filter_str != '' else ''}
            {'' if order_str == '' else 'ORDER BY ' + order_str}
            LIMIT {numRowsPerPage} OFFSET {offset};
        """
    elif target_column == 'all':
        i = 0
        for key, filter_group in filter_dict.items():
            filter_group_str = ''

            print(key, ' : ', filter_group)
            if len(filter_group) > 0:
                for idx, elem in enumerate(filter_group):
                    print(elem)
                    column_type = elem['filter_column'].split('#')[0]
                    column_name = elem['filter_column'].split('#')[1]
                    filter_condition = elem['filter_condition']
                    filter_value = elem['filter_value']
                    filter_conjunction = elem['filter_conjunction']

                    expression = filter_condition % (column_name, filter_value)
                    # filter_str += f" ({expression}) " + ('' if i == len(filter_dict) - 1 and idx == len(filter_group) - 1 else filter_conjunction)
                    filter_group_str += f" {expression} " + ('' if idx == len(filter_group) - 1 else filter_conjunction)

                filter_str += f''' ({filter_group_str}) {('' if i == len(filter_dict) - 1 else filter_group_conjunction_list[i])} '''
            i += 1

        query = f"""
            SELECT
                mut.cell_name, mut.gene, mut.chrom, mut.start_pos, mut.end_pos, mut.protein_change, mut.reference_allele,
                mut.tumor_seq_allele2, mut.variant_info, mut.variant_classification, mut.mutation_effect,
                mut.oncogenic, mut.source, info.lineage, info.subtype, info.mutation_data, info.cn_data, info.fusion_gene,
                info.in_house, hrd.loh_score, hrd.tai_score, hrd.lst_score, hrd.hrd_score, msi.gdsc_msi, msi.ccle_msi
            FROM cell_mutation mut
            LEFT JOIN cell_mutation_info info ON info.cell_name=mut.cell_name
            LEFT JOIN cell_mutation_hrd hrd ON info.cell_name=hrd.cell_name
            LEFT JOIN cell_mutation_msi msi ON info.cell_name=msi.cell_name
            {'WHERE ' + filter_str + ' ' if filter_str != '' else ''}
            {'' if order_str == '' else 'ORDER BY ' + order_str}
            LIMIT {numRowsPerPage} OFFSET {offset};
        """
    print(query)
    cur.execute(query)

    data_list = dictfetchall(cur)

    if cur != None :
        cur.close()

    return True, True, {'data':data_list}

def totalSearchCellMutation(request):
    cur = connection.cursor()
    filter_dict = json.loads(request.POST.get('filter_dict'))
    filter_str = ''

    filter_group_conjunction_list = json.loads(request.POST.get('filter_group_conjunction_list'))

    target_column = request.POST.get('target_column')

    if target_column == 'cell_name':
        i = 0
        for key, filter_group in filter_dict.items():
            filter_group_str = ''

            if len(filter_group) > 0:
                for idx, elem in enumerate(filter_group):
                    column_type = elem['filter_column'].split('#')[0]
                    column_name = elem['filter_column'].split('#')[1]
                    column_name = column_name.split('.')[0] + str(i) + '.' + column_name.split('.')[1]
                    filter_condition = elem['filter_condition']
                    filter_conjunction = elem['filter_conjunction']
                    filter_value = elem['filter_value']
                    filter_group_condition = elem['filter_group_condition']

                    expression = filter_condition % (column_name, filter_value)
                    filter_group_str += f" {expression} " + ('' if idx == len(filter_group) - 1 else filter_conjunction)

                filter_str += f'''
                    {filter_group_condition} EXISTS (
                        SELECT 1 FROM cell_mutation mut{i}
                        LEFT JOIN cell_mutation_info info{i} ON mut{i}.cell_name=info{i}.cell_name
                        LEFT JOIN cell_mutation_hrd hrd{i} ON mut{i}.cell_name=hrd{i}.cell_name
                        LEFT JOIN cell_mutation_msi msi{i} ON mut{i}.cell_name=msi{i}.cell_name
                        WHERE mut.cell_name=mut{i}.cell_name
                        AND ({filter_group_str})
                    ) {('' if i == len(filter_dict) - 1 else filter_group_conjunction_list[i])}
                '''
            i += 1

        cur.execute(f"""
            SELECT count(mut.cell_name) as total
            FROM (
                SELECT DISTINCT ON (mut_inner.cell_name) mut_inner.cell_name FROM cell_mutation mut_inner
	            INNER JOIN cell_mutation_info info_inner ON info_inner.cell_name=mut_inner.cell_name
            ) mut
            LEFT JOIN cell_mutation_info info ON mut.cell_name=info.cell_name
            LEFT JOIN cell_mutation_hrd hrd ON mut.cell_name=hrd.cell_name
            LEFT JOIN cell_mutation_msi msi ON mut.cell_name=msi.cell_name
            WHERE mut.cell_name IS NOT NULL {' AND (' + filter_str + ') ' if filter_str != '' else ''}
        """)

    elif target_column == 'all':
        # for i, filter_group in enumerate(filter_dict):
        i = 0
        for key, filter_group in filter_dict.items():
            filter_group_str = ''

            if len(filter_group) > 0:
                for idx, elem in enumerate(filter_group):
                    # print(elem)
                    column_type = elem['filter_column'].split('#')[0]
                    column_name = elem['filter_column'].split('#')[1]
                    filter_condition = elem['filter_condition']
                    filter_value = elem['filter_value']
                    filter_conjunction = elem['filter_conjunction']

                    expression = filter_condition % (column_name, filter_value)
                    # filter_str += f" ({expression}) " + ('' if i == len(filter_dict) - 1 and idx == len(filter_group) - 1 else filter_conjunction)
                    filter_group_str += f" {expression} " + ('' if idx == len(filter_group) - 1 else filter_conjunction)

                filter_str += f''' ({filter_group_str}) {('' if i == len(filter_dict) - 1 else filter_group_conjunction_list[i])} '''
            i += 1

        cur.execute(f"""
            SELECT count(mut.id) as total
            FROM cell_mutation mut
            LEFT JOIN cell_mutation_info info ON mut.cell_name=info.cell_name
            LEFT JOIN cell_mutation_hrd hrd ON mut.cell_name=hrd.cell_name
            LEFT JOIN cell_mutation_msi msi ON mut.cell_name=msi.cell_name
            {'WHERE ' + filter_str + ' ' if filter_str != '' else ''}
        """)

    total_rows = dictfetchall(cur)
    print('total rows:', total_rows[0]['total'])
    if cur != None :
        cur.close()

    return True, True, {'total':total_rows[0]['total']}

def uploadCellMutation(request):
    actionType = request.POST.get('actionType')
    owner_id = request.user.id

    try:
        with transaction.atomic():
            cell_info = request.FILES.get('cell_info')
            mutation = request.FILES.get('mutation')
            cnv_depmap = request.FILES.get('cnv_depmap')
            cnv_inhouse = request.FILES.get('cnv_inhouse')
            cn_depmap = request.FILES.get('cn_depmap')
            ycc_cell_cnv = request.FILES.get('ycc_cell_cnv')
            hrd = request.FILES.get('hrd')
            msi = request.FILES.get('msi')

            if (cell_info != None and not '.txt' in cell_info.name.lower()) or (mutation != None and not '.txt' in mutation.name.lower()) or (cn_depmap != None and not '.txt' in cn_depmap.name.lower()) or (ycc_cell_cnv != None and not '.txt' in ycc_cell_cnv.name.lower()) or (hrd != None and not '.txt' in hrd.name.lower()) or (msi != None and not '.txt' in msi.name.lower()):
                return False, False, '.txt 파일만 올려주세요.'

            if cell_info != None:
                path = default_storage.save("raw_datas/"+cell_info.name, cell_info)
                cell_info.seek(0)

                for i, line in enumerate(cell_info.read().decode('euc-kr').split('\r\n')):
                    columns = line.split('\t')
                    print(i, columns)
                    if i == 0 or len(columns) == 1:
                        continue

                    CellMutationInfo.objects.create(**{
                        'cell_name': columns[0],
                        'lineage': None if columns[1] == '.' else columns[1],
                        'subtype': None if columns[2] == '.' else columns[2],
                        'mutation_data': True if columns[3] == 'Y' else False,
                        'cn_data': True if columns[4] == 'Y' else False,
                        'fusion_gene': True if columns[5] == 'Y' else False,
                        'in_house': True if columns[6] == 'Y' else False,
                        'file_name': path
                    })

            if mutation != None:
                print("mutation")
                path = default_storage.save("raw_datas/"+mutation.name, mutation)
                mutation.seek(0)

                # for i, line in enumerate(mutation.read().decode('euc-kr').split('\r\n')):
                for i, line in enumerate(mutation.read().decode('euc-kr').split('\n')):
                    columns = line.split('\t')

                    if i == 0 or len(columns) == 1:
                        continue

                    chrom = None if columns[0] == '' or columns[0] == '.' else columns[0]
                    start_pos = None if columns[1] == '' or columns[1] == '.' else columns[1]
                    end_pos = None if columns[2] == '' or columns[2] == '.' else columns[2]
                    variant_info = None if columns[3] == '' or columns[3] == '.' else columns[3]
                    reference_allele = None if columns[4] == '' or columns[4] == '.' else columns[4]
                    tumor_seq_allele1 = None if columns[5] == '' or columns[5] == '.' else columns[5]
                    tumor_seq_allele2 = None if columns[6] == '' or columns[6] == '.' else columns[6]
                    cell_name = None if columns[7] == '' or columns[7] == '.' else columns[7]
                    variant_classification = None if columns[8] == '' or columns[8] == '.' else columns[8]
                    protein_change = None if columns[9] == '' or columns[9] == '.' else columns[9]
                    gene = None if columns[10] == '' or columns[10] == '.' else columns[10]
                    mutation_effect = None if columns[11] == '' or columns[11] == '.' else columns[11]
                    oncogenic=None if columns[12] == '' or columns[12] == '.' else columns[12]
                    source= None if columns[13] == '' or columns[13] == '.' else columns[13]

                    data = {
                        'chrom': chrom, 'start_pos': start_pos, 'end_pos': end_pos, 'variant_info': variant_info,
                        'reference_allele': reference_allele, 'tumor_seq_allele1': tumor_seq_allele1, 'tumor_seq_allele2': tumor_seq_allele2,
                        'variant_classification': variant_classification, 'protein_change': protein_change,
                        'gene': gene, 'mutation_effect': mutation_effect,
                        'oncogenic': oncogenic, 'cell_name': cell_name, 'source': source, 'file_name': path
                    }
                    print(i, data)

                    old_obj = CellMutation.objects.filter(
                        Q(cell_name=cell_name) & Q(protein_change=protein_change) &
                        Q(gene=gene) & Q(chrom=chrom) &
                        Q(start_pos=start_pos) & Q(end_pos=end_pos) &
                        Q(reference_allele=reference_allele) &
                        Q(tumor_seq_allele1=tumor_seq_allele1) &
                        Q(tumor_seq_allele2=tumor_seq_allele2)
                    ).last()

                    if old_obj != None:
                        # 중복처리: MUTATION_EFFECT 가 unknown 이 아닌걸로 남겨주시고
                        if old_obj.mutation_effect == mutation_effect:
                            if old_obj.source == 'Depmap':
                                continue
                            elif source == 'Depmap':
                                CellMutation.objects.filter(id=old_obj.id).update(**data)
                                continue
                            else:
                                print("")
                                raise Exception("중복처리 에러::old_obj.source != Depmap & new_obj.source != Depmap")
                        else:
                            if old_obj.mutation_effect != 'Unknown':
                                continue
                            elif mutation_effect != 'Unknown':
                                CellMutation.objects.filter(id=old_obj.id).update(**data)
                                continue
                            else:
                                raise Exception("중복처리 에러::old_obj.mutation_effect == Depmap & new_obj.mutation_effect == Depmap")

                    CellMutation.objects.create(**data)

                    if i % 10000 == 0:
                        print(i)

            if cnv_depmap != None:
                print("cnv_depmap")
                path = default_storage.save("raw_datas/"+cnv_depmap.name, cnv_depmap)
                cnv_depmap.seek(0)

                lines = cnv_depmap.read().decode('euc-kr').split('\n')[1:]
                # lines = cnv_depmap.read().decode('euc-kr').split('\r\n')[1:]
                lines_per_chunk = 100000

                # for i, line in enumerate(mutation.read().decode('euc-kr').split('\r\n')):
                for chunk_start in range(0, len(lines), lines_per_chunk):
                    data_list = []
                    for i, line in enumerate(lines[chunk_start:chunk_start + lines_per_chunk], start=chunk_start):
                        columns = line.split('\t')
                        # print(i, columns)

                        if len(columns) == 1:
                            print("len(columns) == 1::continue")
                            continue

                        chrom = None if columns[0] == '' or columns[0] == '.' else columns[0]
                        start_pos = None if columns[1] == '' or columns[1] == '.' else columns[1]
                        end_pos = None if columns[2] == '' or columns[2] == '.' else columns[2]
                        variant_info = None if columns[3] == '' or columns[3] == '.' else columns[3]
                        reference_allele = None if columns[4] == '' or columns[4] == '.' else columns[4]
                        tumor_seq_allele1 = None if columns[5] == '' or columns[5] == '.' else columns[5]
                        tumor_seq_allele2 = None if columns[6] == '' or columns[6] == '.' else columns[6]
                        cell_name = None if columns[7] == '' or columns[7] == '.' else columns[7]
                        variant_classification = None if columns[8] == '' or columns[8] == '.' else columns[8]
                        protein_change = None if columns[9] == '' or columns[9] == '.' else columns[9]
                        gene = None if columns[10] == '' or columns[10] == '.' else columns[10]
                        mutation_effect = None if columns[11] == '' or columns[11] == '.' else columns[11]
                        oncogenic=None if columns[12] == '' or columns[12] == '.' else columns[12]
                        source= None if columns[13] == '' or columns[13] == '.' else columns[13]

                        # CellMutation.objects.create(**data)
                        data_list.append(CellMutation(
                            chrom=chrom, start_pos=start_pos, end_pos=end_pos, variant_info=variant_info,
                            reference_allele=reference_allele, tumor_seq_allele1=tumor_seq_allele1, tumor_seq_allele2=tumor_seq_allele2,
                            cell_name=cell_name, variant_classification=variant_classification,
                            protein_change=protein_change, gene=gene,
                            mutation_effect=mutation_effect, oncogenic=oncogenic,
                            source=source, file_name=path
                        ))

                    print(chunk_start, len(data_list))
                    CellMutation.objects.bulk_create(data_list)

            if cnv_inhouse != None:
                print(cnv_inhouse)
                path = default_storage.save("raw_datas/"+cnv_inhouse.name, cnv_inhouse)
                cnv_inhouse.seek(0)
                lines = cnv_inhouse.read().decode('euc-kr').split('\n')[1:]
                # lines = cnv_inhouse.read().decode('euc-kr').split('\r\n')[1:]
                lines_per_chunk = 100000

                # for i, line in enumerate(cnv_inhouse.read().decode('euc-kr').split('\r\n')):
                for chunk_start in range(0, len(lines), lines_per_chunk):
                    data_list = []
                    for i, line in enumerate(lines[chunk_start:chunk_start + lines_per_chunk], start=chunk_start):
                        columns = line.split('\t')
                        # print(i, columns)

                        if len(columns) == 1:
                            print("len(columns) == 1::continue")
                            continue

                        chrom = None if columns[0] == '' or columns[0] == '.' else columns[0]
                        start_pos = None if columns[1] == '' or columns[1] == '.' else columns[1]
                        end_pos = None if columns[2] == '' or columns[2] == '.' else columns[2]
                        variant_info = None if columns[3] == '' or columns[3] == '.' else columns[3]
                        reference_allele = None if columns[4] == '' or columns[4] == '.' else columns[4]
                        tumor_seq_allele1 = None if columns[5] == '' or columns[5] == '.' else columns[5]
                        tumor_seq_allele2 = None if columns[6] == '' or columns[6] == '.' else columns[6]
                        cell_name = None if columns[7] == '' or columns[7] == '.' else columns[7]
                        variant_classification = None if columns[8] == '' or columns[8] == '.' else columns[8]
                        protein_change = None if columns[9] == '' or columns[9] == '.' else columns[9]
                        gene = None if columns[10] == '' or columns[10] == '.' else columns[10]
                        mutation_effect = None if columns[11] == '' or columns[11] == '.' else columns[11]
                        oncogenic=None if columns[12] == '' or columns[12] == '.' else columns[12]
                        source= None if columns[13] == '' or columns[13] == '.' else columns[13]

                        # CellMutation.objects.create(**data)
                        data_list.append(CellMutation(
                            chrom=chrom, start_pos=start_pos, end_pos=end_pos, variant_info=variant_info,
                            reference_allele=reference_allele, tumor_seq_allele1=tumor_seq_allele1, tumor_seq_allele2=tumor_seq_allele2,
                            cell_name=cell_name, variant_classification=variant_classification,
                            protein_change=protein_change, gene=gene,
                            mutation_effect=mutation_effect, oncogenic=oncogenic,
                            source=source, file_name=path
                        ))

                    print(chunk_start, len(data_list))
                    CellMutation.objects.bulk_create(data_list)

            if hrd != None:
                path = default_storage.save("raw_datas/"+hrd.name, hrd)
                hrd.seek(0)

                for i, line in enumerate(hrd.read().decode('euc-kr').split('\r\n')):

                    columns = line.split('\t')
                    print(i, columns)

                    if i == 0 or len(columns) == 1:
                        continue

                    CellMutationHRD.objects.create(**{
                        'cell_name': columns[0],
                        'loh_score': float(columns[-4]) if columns[-4] != '' and columns[-4] != '.' else None,
                        'tai_score': float(columns[-3]) if columns[-3] != '' and columns[-3] != '.' else None,
                        'lst_score': float(columns[-2]) if columns[-2] != '' and columns[-2] != '.' else None,
                        'hrd_score': float(columns[-1]) if columns[-1] != '' and columns[-1] != '.' else None,
                        'file_name': path
                    })

            if msi != None:
                path = default_storage.save("raw_datas/"+msi.name, msi)
                msi.seek(0)

                for i, line in enumerate(msi.read().decode('euc-kr').split('\r\n')):

                    columns = line.split('\t')
                    print(i, columns)

                    if i == 0 or len(columns) == 1:
                        continue

                    CellMutationMSI.objects.create(**{
                        'cell_name': columns[0],
                        'gdsc_msi': None if columns[1] == '' or columns[1] == '.' else columns[1],
                        'ccle_msi': None if columns[2] == '' or columns[2] == '.' else columns[2],
                        'file_name': path
                    })

    except Exception as e:
        print("Exception::", e)
        return False, False, e
    return True, False, 'success'

def downloadCellMutation(request):
    cur = connection.cursor()
    filter_dict = json.loads(request.POST.get('filter_dict'))
    filter_str = ''

    filter_group_conjunction_list = json.loads(request.POST.get('filter_group_conjunction_list'))

    order_dict = json.loads(request.POST.get('order_dict'))
    order_str = ''

    target_column = request.POST.get('target_column')

    for i, elem in enumerate(order_dict):
        column_name = elem['column_name']
        order = elem['order']

        expression = column_name + ' ' + order

        order_str += f" {expression} " + ('' if i == len(order_dict) - 1 else ',')
    print('order:"'+order_str + '"')

    if target_column == 'cell_name':
        i = 0
        for key, filter_group in filter_dict.items():
            filter_group_str = ''

            if len(filter_group) > 0:
                for idx, elem in enumerate(filter_group):
                    column_type = elem['filter_column'].split('#')[0]
                    column_name = elem['filter_column'].split('#')[1]
                    column_name = column_name.split('.')[0] + str(i) + '.' + column_name.split('.')[1]
                    filter_condition = elem['filter_condition']
                    filter_conjunction = elem['filter_conjunction']
                    filter_value = elem['filter_value']
                    filter_group_condition = elem['filter_group_condition']

                    expression = filter_condition % (column_name, filter_value)
                    filter_group_str += f" {expression} " + ('' if idx == len(filter_group) - 1 else filter_conjunction)

                filter_str += f'''
                    {filter_group_condition} EXISTS (
                        SELECT 1 FROM cell_mutation mut{i}
                        LEFT JOIN cell_mutation_info info{i} ON mut{i}.cell_name=info{i}.cell_name
                        LEFT JOIN cell_mutation_hrd hrd{i} ON mut{i}.cell_name=hrd{i}.cell_name
                        LEFT JOIN cell_mutation_msi msi{i} ON mut{i}.cell_name=msi{i}.cell_name
                        WHERE mut.cell_name=mut{i}.cell_name
                        AND ({filter_group_str})
                    ) {('' if i == len(filter_dict) - 1 else filter_group_conjunction_list[i])}
                '''
            i += 1

        cur.execute(f"""
            SELECT
                mut.cell_name, mut.lineage, mut.subtype, mut.mutation_data, mut.cn_data, mut.fusion_gene, mut.in_house
            FROM (
                SELECT DISTINCT ON (mut_inner.cell_name) info_inner.* FROM cell_mutation mut_inner
	            INNER JOIN cell_mutation_info info_inner ON info_inner.cell_name=mut_inner.cell_name
            ) mut
            LEFT JOIN cell_mutation_info info ON mut.cell_name=info.cell_name
            LEFT JOIN cell_mutation_hrd hrd ON mut.cell_name=hrd.cell_name
            LEFT JOIN cell_mutation_msi msi ON mut.cell_name=msi.cell_name
            WHERE mut.cell_name IS NOT NULL {' AND (' + filter_str + ') ' if filter_str != '' else ''}
            {'ORDER BY ' + order_str if order_str != '' else f'''ORDER BY
                mut.cell_name, mut.lineage, mut.subtype, mut.mutation_data, mut.cn_data, mut.fusion_gene, mut.in_house
            '''}
        """)

    elif target_column == 'all':
        # for i, filter_group in enumerate(filter_dict):
        i = 0
        for key, filter_group in filter_dict.items():
            filter_group_str = ''

            if len(filter_group) > 0:
                for idx, elem in enumerate(filter_group):
                    # print(elem)
                    column_type = elem['filter_column'].split('#')[0]
                    column_name = elem['filter_column'].split('#')[1]
                    filter_condition = elem['filter_condition']
                    filter_value = elem['filter_value']
                    filter_conjunction = elem['filter_conjunction']

                    expression = filter_condition % (column_name, filter_value)
                    # filter_str += f" ({expression}) " + ('' if i == len(filter_dict) - 1 and idx == len(filter_group) - 1 else filter_conjunction)
                    filter_group_str += f" {expression} " + ('' if idx == len(filter_group) - 1 else filter_conjunction)

                filter_str += f''' ({filter_group_str}) {('' if i == len(filter_dict) - 1 else filter_group_conjunction_list[i])} '''
            i += 1

        cur.execute(f"""
            SELECT
                mut.cell_name, mut.gene, mut.protein_change, mut.chrom, mut.start_pos, mut.end_pos, mut.reference_allele,
                mut.tumor_seq_allele2, mut.variant_info, mut.variant_classification, mut.mutation_effect,
                mut.oncogenic, mut.source, info.lineage, info.subtype, info.mutation_data, info.cn_data, info.fusion_gene,
                info.in_house, hrd.loh_score, hrd.tai_score, hrd.lst_score, hrd.hrd_score, msi.gdsc_msi, msi.ccle_msi
            FROM cell_mutation mut
            LEFT JOIN cell_mutation_info info ON mut.cell_name=info.cell_name
            LEFT JOIN cell_mutation_hrd hrd ON mut.cell_name=hrd.cell_name
            LEFT JOIN cell_mutation_msi msi ON mut.cell_name=msi.cell_name
            {'WHERE ' + filter_str + ' ' if filter_str != '' else ''}
            {'ORDER BY ' + order_str if order_str != '' else f'''ORDER BY
                mut.cell_name, mut.gene, mut.protein_change, mut.chrom, mut.start_pos, mut.end_pos, mut.reference_allele,
                mut.tumor_seq_allele2, mut.variant_info, mut.variant_classification, mut.mutation_effect,
                mut.oncogenic, mut.source, info.lineage, info.subtype, info.mutation_data, info.cn_data, info.fusion_gene,
                info.in_house, hrd.loh_score, hrd.tai_score, hrd.lst_score, hrd.hrd_score, msi.gdsc_msi, msi.ccle_msi
            '''}
        """)

    # 엑셀 워크북 생성
    wb = Workbook()
    ws = wb.active

    # data_list = []
    rows = cur.fetchall()

    if target_column == 'cell_name':
        columns = ['cell_name', 'lineage', 'subtype', 'mutation_data', 'cn_data', 'fusion_gene', 'in_house']
    elif target_column == 'all':
        columns = [
            'cell_name', 'gene', 'protein_change', 'chrom', 'start_pos', 'end_pos', 'reference_allele',
            'tumor_seq_allele2', 'variant_info', 'variant_classification', 'mutation_effect',
            'oncogenic', 'source', 'lineage', 'subtype', 'mutation_data', 'cn_data', 'fusion_gene',
            'in_house', 'loh_score', 'tai_score', 'lst_score', 'hrd_score', 'gdsc_msi', 'ccle_msi'
        ]
    ws.append(columns)

    for row in rows:
        if target_column == 'cell_name':
            ws.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

        elif target_column == 'all':
            ws.append([
                row[0], row[1], row[2], row[3], row[4], row[5], row[6],
                row[7], row[8], row[9], row[10], row[11], row[12], row[13],
                row[14], row[15], row[16], row[17], row[18], row[19], row[20],
                row[21], row[22], row[23], row[24]
            ])

    if cur != None :
        cur.close()

    # HTTP 응답 설정
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # 엑셀 파일 저장
    wb.save(response)

    return response

def getAutocompleteList(request):
    cur = connection.cursor()

    keyword = request.POST.get('keyword')

    cur.execute(f"""
        SELECT cell_name FROM cell_mutation_info
        WHERE cell_name ilike '%{keyword}%'
        ORDER BY cell_name
    """)

    rows = dictfetchall(cur)

    if cur != None :
        cur.close()

    return True, True, {'data': rows}

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

def getCellMutationColumns(request):
    return {
        'columns': [
            ###################################################################################################
            ## cell_mutation
            ###################################################################################################
            {'column_name':'cell_name', 'table_column_name': 'mut.cell_name', 'type': 'str'},
            {'column_name':'gene', 'table_column_name': 'mut.gene', 'type': 'str'},
            {'column_name':'protein_change', 'table_column_name': 'mut.protein_change', 'type': 'str'},
            {'column_name':'chrom', 'table_column_name': 'mut.chrom', 'type': 'str'},
            {'column_name':'start_pos', 'table_column_name': 'mut.start_pos', 'type': 'str'},
            {'column_name':'end_pos', 'table_column_name': 'mut.end_pos', 'type': 'str'},
            {'column_name':'reference_allele', 'table_column_name': 'mut.reference_allele', 'type': 'str'},
            # {'column_name':'tumor_seq_allele1', 'table_column_name': 'mut.tumor_seq_allele1', 'type': 'str'},
            {'column_name':'tumor_seq_allele2', 'table_column_name': 'mut.tumor_seq_allele2', 'type': 'str'},
            {'column_name':'variant_info', 'table_column_name': 'mut.variant_info', 'type': 'str'},
            {'column_name':'variant_classification', 'table_column_name': 'mut.variant_classification', 'type': 'str'},
            {'column_name':'mutation_effect', 'table_column_name': 'mut.mutation_effect', 'type': 'select'},
            {'column_name':'oncogenic', 'table_column_name': 'mut.oncogenic', 'type': 'select'},
            {'column_name':'source', 'table_column_name': 'mut.source', 'type': 'str'},

            ###################################################################################################
            ## cell_mutation_info
            ###################################################################################################
            {'column_name':'lineage', 'table_column_name': 'info.lineage', 'type': 'select'},
            {'column_name':'subtype', 'table_column_name': 'info.subtype', 'type': 'select'},
            {'column_name':'mutation_data', 'table_column_name': 'info.mutation_data', 'type': 'bool'},
            {'column_name':'cn_data', 'table_column_name': 'info.cn_data', 'type': 'bool'},
            {'column_name':'fusion_gene', 'table_column_name': 'info.fusion_gene', 'type': 'bool'},
            {'column_name':'in_house', 'table_column_name': 'info.in_house', 'type': 'bool'},

            {'column_name':'loh_score', 'table_column_name': 'hrd.loh_score', 'type': 'num'},
            {'column_name':'tai_score', 'table_column_name': 'hrd.tai_score', 'type': 'num'},
            {'column_name':'lst_score', 'table_column_name': 'hrd.lst_score', 'type': 'num'},
            {'column_name':'hrd_score', 'table_column_name': 'hrd.hrd_score', 'type': 'num'},

            {'column_name':'gdsc_msi', 'table_column_name': 'msi.gdsc_msi', 'type': 'select'},
            {'column_name':'ccle_msi', 'table_column_name': 'msi.ccle_msi', 'type': 'select'},
        ],
        'lineages': {
            'Adrenal Gland': [ 'Adrenocortical Carcinoma'],
            'Ampulla of Vater': [ 'Ampullary Carcinoma'],
            'Biliary Tract': [ 'Intracholecystic Papillary Neoplasm','Intraductal Papillary Neoplasm of the Bile Duct'],
            'Bladder/Urinary Tract': [ 'Bladder Urothelial Carcinoma','Bladder Squamous Cell Carcinoma','Urethral Cancer'],
            'Bone': [ 'Ewing Sarcoma','Osteosarcoma','Chondrosarcoma','Chordoma'],
            'Bowel': [ 'Colorectal Adenocarcinoma','Small Bowel Cancer'],
            'Breast': [ 'Invasive Breast Carcinoma','Breast Ductal Carcinoma In Situ','Breast Neoplasm, NOS'],
            'CNS/Brain': [ 'Meningothelial Tumor','Diffuse Glioma','Embryonal Tumor'],
            'Cervix': [ 'Cervical Squamous Cell Carcinoma','Cervical Adenocarcinoma','Mixed Cervical Carcinoma','Glassy Cell Carcinoma of the Cervix','Small Cell Carcinoma of the Cervix'],
            'Esophagus/Stomach': [ 'Esophagogastric Adenocarcinoma','Esophageal Squamous Cell Carcinoma'],
            'Eye': [ 'Retinoblastoma','Ocular Melanoma','Non-Cancerous'],
            'Fibroblast': [ 'Non-Cancerous'],
            'Head and Neck': [ 'Head and Neck Squamous Cell Carcinoma','Head and Neck Carcinoma, Other','Salivary Carcinoma'],
            'Kidney': [ 'Renal Cell Carcinoma','Rhabdoid Cancer','Non-Cancerous'],
            'Liver': [ 'Hepatocellular Carcinoma','Hepatoblastoma','Hepatocellular Carcinoma plus Intrahepatic Cholangiocarcinoma'],
            'Lung': [ 'Non-Small Cell Lung Cancer','Lung Neuroendocrine Tumor'],
            'Lymphoid': [ 'B-Lymphoblastic Leukemia/Lymphoma','Mature B-Cell Neoplasms','Mature T and NK Neoplasms','Non-Hodgkin Lymphoma','Hodgkin Lymphoma','T-Lymphoblastic Leukemia/Lymphoma'],
            'Myeloid': [ 'Acute Myeloid Leukemia','Myeloproliferative Neoplasms','Myelodysplastic Syndromes','Non-Cancerous','Acute Leukemias of Ambiguous Lineage','Hereditary Spherocytosis'],
            'Normal': [ 'Non-Cancerous'],
            'Other': [ 'Extra Gonadal Germ Cell Tumor'],
            'Ovary/Fallopian Tube': [ 'Ovarian Epithelial Tumor','Ovarian Germ Cell Tumor','Ovarian Cancer, Other','Sex Cord Stromal Tumor'],
            'Pancreas': [ 'Pancreatic Adenocarcinoma','Adenosquamous Carcinoma of the Pancreas','Pancreatic Neuroendocrine Tumor'],
            'Peripheral Nervous System': [ 'Neuroblastoma','Nerve Sheath Tumor'],
            'Pleura': [ 'Pleural Mesothelioma'],
            'Prostate': [ 'Prostate Adenocarcinoma','Prostate Small Cell Carcinoma','Non-Cancerous'],
            'Skin': [ 'Melanoma','Merkel Cell Carcinoma','Cutaneous Squamous Cell Carcinoma'],
            'Soft Tissue': [ 'Sarcoma, NOS','Rhabdomyosarcoma','Fibrosarcoma','Leiomyosarcoma','Undifferentiated Pleomorphic Sarcoma/Malignant Fibrous Histiocytoma/High-Grade Spindle Cell Sarcoma','Synovial Sarcoma','Epithelioid Sarcoma','Liposarcoma'],
            'Testis': [ 'Non-Seminomatous Germ Cell Tumor'],
            'Thyroid': [ 'Well-Differentiated Thyroid Cancer','Anaplastic Thyroid Cancer','Poorly Differentiated Thyroid Cancer','Medullary Thyroid Cancer'],
            'Uterus': [ 'Endometrial Carcinoma','Uterine Sarcoma/Mesenchymal','Gestational Trophoblastic Disease'],
            'Vulva/Vagina': [ 'Squamous Cell Carcinoma of the Vulva/Vagina','Mucosal Melanoma of the Vulva/Vagina']
        }
    }

############################################################################
############              cell line selector                         ############
############################################################################
def checkPresavedData(request):

    actionType = request.POST.get('action_type')
    list_to_req = json.loads(request.POST.get('list_to_req'))
    dependency = False if request.POST.get('dependency') == '' else True
    effect = False if request.POST.get('effect') == '' else True
    # dep_or_eff = request.POST.get('dependency/effect')
    target_name = request.POST.get('main-search-keyword').upper()

    check_all = False if request.POST.get('check_all') == '' or request.POST.get('check_all') == None else True
    print('check_all:', check_all)

    methods = {}
    if dependency and effect:
        dep_or_eff = 'Both'
        methods['Dependency'] = { 'rows': [], 'ask_data': True }
        methods['Effect'] = { 'rows': [], 'ask_data': True }
    elif dependency:
        dep_or_eff = 'Dependency'
        methods['Dependency'] = { 'rows': [], 'ask_data': True }
        methods['Effect'] = { 'rows': [], 'ask_data': False }
    elif effect:
        dep_or_eff = 'Effect'
        methods['Dependency'] = { 'rows': [], 'ask_data': False }
        methods['Effect'] = { 'rows': [], 'ask_data': True }

    # target_name = 'TP53'

    left_num = request.POST.get('left_num')
    right_num = request.POST.get('right_num')
    # left_num = '49'
    # right_num = '60'

    print('target_name:', target_name,', dep_or_eff:', dep_or_eff, ', effect:')
    print('left_num:', left_num, ', right_num:', right_num)
    print('list_to_req:', list_to_req)

    title_list = []

    if check_all:
        title_list.append('df_depmap_all')

    for elem in list_to_req:
        for item in elem['checked_list']:

            if elem['category'] == 'addgene':
                preprocessed_file_name = 'df_' + elem['category'] + '_' + item['value']
            elif elem['category'] == 'hallmark':
                preprocessed_file_name = 'df_' + item['value']
            elif elem['category'] == 'oncogene':
                preprocessed_file_name = 'df_' + item['value']
            elif elem['category'] == 'wikipathways':
                preprocessed_file_name = 'df_' + item['value']
            elif elem['category'] == 'gene_ontology':
                preprocessed_file_name = 'df_' + item['value'].replace(':', '_')
            else:
                preprocessed_file_name = 'df_' + item['value']

            title_list.append(preprocessed_file_name)

    print('num_sets:', title_list)
    if len(title_list) == 0:
        return False, False, 'Gene Set을 하나 이상 선택해주세요.'

    for key, item in methods.items():
        if item['ask_data'] == False:
            continue
    
        print(f"""
            SELECT id, title, feature_ranks FROM cell_line_selector_info
            WHERE target ilike '{target_name}' and {key} is true AND { 'is_best_combo is TRUE AND ' if actionType == 'SEARCH' else (' "left"=' + left_num + ' AND "right"=' + right_num + ' AND ') }
            gene_set_list @> '{str(title_list).replace("'", '"')}'::jsonb AND jsonb_array_length(gene_set_list) = {len(title_list)};
        """)

        item['rows'] = CellLineSelectorInfo.objects.raw(f"""
            SELECT id, title, feature_ranks FROM cell_line_selector_info
            WHERE target ilike '{target_name}' and {key} is true AND { 'is_best_combo is TRUE AND ' if actionType == 'SEARCH' else (' "left"=' + left_num + ' AND "right"=' + right_num + ' AND ') }
            gene_set_list @> '{str(title_list).replace("'", '"')}'::jsonb AND jsonb_array_length(gene_set_list) = {len(title_list)};
        """)

        item['ask_data'] = True if len(item['rows']) == 0 else False

        print(key, ': ', item['ask_data'], ': rows:', len(item['rows']))
    
    if methods['Dependency']['ask_data'] or methods['Effect']['ask_data']:
        print('checkPresavedData::Case 1::generate new data')
        return True, True, '해당 조합으로 검색시 시간이 1~5분 정도 소요될 수 있습니다.\n계속 진행하시겠습니까?'
    else:
        print('checkPresavedData::Case 2::get from db')
        return True, True, ''

def cellLineSelectorSearch(request):
    if platform == 'win32':
        # url = "http://192.168.1.250:10015/api"
        url = "http://localhost:10015/api"
    else :
        url = "http://172.16.1.30:10015/api"

    cur = connection.cursor()

    actionType = request.POST.get('actionType')
    list_to_req = json.loads(request.POST.get('list_to_req'))
    dependency = False if request.POST.get('dependency') == '' else True
    effect = False if request.POST.get('effect') == '' else True
    # dep_or_eff = request.POST.get('dependency/effect')
    target_name = request.POST.get('main-search-keyword').upper()

    check_all = False if request.POST.get('check_all') == '' or request.POST.get('check_all') == None else True
    print('check_all:', check_all)

    methods = {}
    if dependency and effect:
        dep_or_eff = 'Both'
        methods['Dependency'] = { 'rows': [], 'ask_data': True }
        methods['Effect'] = { 'rows': [], 'ask_data': True }
    elif dependency:
        dep_or_eff = 'Dependency'
        methods['Dependency'] = { 'rows': [], 'ask_data': True }
        methods['Effect'] = { 'rows': [], 'ask_data': False }
    elif effect:
        dep_or_eff = 'Effect'
        methods['Dependency'] = { 'rows': [], 'ask_data': False }
        methods['Effect'] = { 'rows': [], 'ask_data': True }

    left_num = request.POST.get('left_num')
    right_num = request.POST.get('right_num')
    # left_num = '49'
    # right_num = '60'

    print('target_name:', target_name,', dep_or_eff:', dep_or_eff, ', effect:')
    print('left_num:', left_num, ', right_num:', right_num)
    print('list_to_req:', list_to_req)

    data = {}

    title_list = []

    if check_all:
        title_list.append('df_depmap_all')

    for elem in list_to_req:
        for item in elem['checked_list']:
            if elem['category'] == 'addgene':
                preprocessed_file_name = 'df_' + elem['category'] + '_' + item['value']
            elif elem['category'] == 'hallmark':
                preprocessed_file_name = 'df_' + item['value']
            elif elem['category'] == 'oncogene':
                preprocessed_file_name = 'df_' + item['value']
            elif elem['category'] == 'wikipathways':
                preprocessed_file_name = 'df_' + item['value']
            elif elem['category'] == 'gene_ontology':
                preprocessed_file_name = 'df_' + item['value'].replace(':', '_')
            else:
                preprocessed_file_name = 'df_' + item['value']

            # title_list.append('df_' + elem['category'] + '_' + item['value'])
            title_list.append(preprocessed_file_name)

    CellLineSelectorTracking.objects.create(**{
        'owner_id': request.user.id,
        'action_type': request.POST.get('actionType'),
        'search_content': {
            'target': target_name,
            'left_num': left_num,
            'right_num': right_num,
            'check_depmap_all': check_all,
            'dependency': dependency,
            'effect': effect,
            'title_list': title_list
        }
    })

    print('num_sets:', title_list)
    if len(title_list) == 0:
        return False, False, 'Gene Set을 하나 이상 선택해주세요.'

    for key, item in methods.items():
        if item['ask_data'] == False:
            continue
    
        print(f"""
            SELECT id, title, feature_ranks FROM cell_line_selector_info
            WHERE target ilike '{target_name}' and {key} is true AND { 'is_best_combo is TRUE AND ' if actionType == 'SEARCH' else (' "left"=' + left_num + ' AND "right"=' + right_num + ' AND ') }
            gene_set_list @> '{str(title_list).replace("'", '"')}'::jsonb AND jsonb_array_length(gene_set_list) = {len(title_list)};
        """)

        item['rows'] = CellLineSelectorInfo.objects.raw(f"""
            SELECT id, title, feature_ranks FROM cell_line_selector_info
            WHERE target ilike '{target_name}' and {key} is true AND { 'is_best_combo is TRUE AND ' if actionType == 'SEARCH' else (' "left"=' + left_num + ' AND "right"=' + right_num + ' AND ') }
            gene_set_list @> '{str(title_list).replace("'", '"')}'::jsonb AND jsonb_array_length(gene_set_list) = {len(title_list)};
        """)

        item['ask_data'] = True if len(item['rows']) == 0 else False

        print(key, ': ', item['ask_data'], ': rows:', len(item['rows']))
    
    # return True, True, ''
    data_to_send = {'gene_set_list': title_list, 'Dependency': {}, 'Effect': {}}
    
    if (dependency and effect) or methods['Dependency']['ask_data'] or methods['Effect']['ask_data']:
        print(' Case 1::generate new data')

        try:
            response = requests.request("POST", url, headers={ 'Content-Type': 'application/x-www-form-urlencoded' }, data={
                'state': 'INIT' if actionType == 'SEARCH' else 'CHANGE-PERCENTILE', 'operation': 'SEARCH', 'main_keyword': target_name, 'dependency': methods['Dependency']['ask_data'], 'effect': methods['Effect']['ask_data'],
                'asked_both': dependency and effect, 'left': left_num, 'right': right_num, 'titles': json.dumps(title_list)
            })
            response = json.loads(response.text)
            # print(response)

            if response.get('result_code') == "0000" :
                result = response.get('result')
            else :
                print('error : ' + response.get('result'))
                result = None
                return False, False, str(response.get('result'))
            
            # return True, True, result['result']

            if methods['Dependency']['ask_data']:
                data_to_send['Dependency'] = result['result']['data']['Dependency']
                data_to_send['Dependency']['ask_data'] = True
            
            if methods['Effect']['ask_data']:
                data_to_send['Effect'] = result['result']['data']['Effect']
                data_to_send['Effect']['ask_data'] = True
            
            if dependency and effect:
                data_to_send['Both'] = result['result']['data']['Both']

        except requests.exceptions.HTTPError as err:
            print('error : ' + str(err))
            return False, False, str(err)

    if (dependency and len(methods['Dependency']['rows']) > 0) or (effect and len(methods['Effect']['rows']) > 0):
        print(' Case 2::get from db')
        for key, item in methods.items():
            if (key == 'Dependency' and (dependency == False or methods['Dependency']['ask_data'])) or (key == 'Effect' and (effect == False or methods['Effect']['ask_data'])):
                continue
            print(key + '::',len(item['rows']))

            first_feature = ''
            second_feature = ''

            feature_ranks = item['rows'][0].feature_ranks

            for k, v in feature_ranks.items():
                if v == 0:
                    first_feature = k
                
                if v == 1:
                    second_feature = k
                
                if first_feature != '' and second_feature != '':
                    break

            print(f"""
                select id, title, histogram_data, default_img as img, cell_data, marker_data, "left", "right",
                    scatter_group0_data->>'cell_name' as group0_cell_name,
                    scatter_group0_data->>'{first_feature}' as group0_first_feature,
                    scatter_group0_data->>'{second_feature}' as group0_second_feature,
                    scatter_group1_data->>'cell_name' as group1_cell_name,
                    scatter_group1_data->>'{first_feature}' as group1_first_feature,
                    scatter_group1_data->>'{second_feature}' as group1_second_feature
                from cell_line_selector_info
                WHERE target ILIKE '{target_name}' AND {key} IS TRUE AND { 'is_best_combo is TRUE AND ' if actionType == 'SEARCH' else (' "left"=' + left_num + ' AND "right"=' + right_num + ' AND ') }
                gene_set_list @> '{str(title_list).replace("'", '"')}'::jsonb AND jsonb_array_length(gene_set_list) = {len(title_list)};
            """)

            cur.execute(f"""
                select id, title, histogram_data, default_img as img, cell_data, marker_data, "left", "right",
                    scatter_group0_data->>'cell_name' as group0_cell_name,
                    scatter_group0_data->>'{first_feature}' as group0_first_feature,
                    scatter_group0_data->>'{second_feature}' as group0_second_feature,
                    scatter_group1_data->>'cell_name' as group1_cell_name,
                    scatter_group1_data->>'{first_feature}' as group1_first_feature,
                    scatter_group1_data->>'{second_feature}' as group1_second_feature
                from cell_line_selector_info
                WHERE target ILIKE '{target_name}' AND {key} IS TRUE AND { 'is_best_combo is TRUE AND ' if actionType == 'SEARCH' else (' "left"=' + left_num + ' AND "right"=' + right_num + ' AND ') }
                gene_set_list @> '{str(title_list).replace("'", '"')}'::jsonb AND jsonb_array_length(gene_set_list) = {len(title_list)};
            """)

            data = dictfetchall(cur)[0]
            data_to_send[ key ] = {
                'title': data['title'], 'img': data['img'], 'left': data['left'], 'right': data['right'],
                'histogram_data': json.loads(data['histogram_data']), 'cell_data': json.loads(data['cell_data']), 'marker_data': json.loads(data['marker_data']),
                'group0_cell_name': json.loads(data['group0_cell_name']), 'group0_first_feature': json.loads(data['group0_first_feature']), 'group0_second_feature': json.loads(data['group0_second_feature']), 
                'group1_cell_name': json.loads(data['group1_cell_name']), 'group1_first_feature': json.loads(data['group1_first_feature']), 'group1_second_feature': json.loads(data['group1_second_feature'])
            }

            minX = data_to_send[ key ]['group0_first_feature'][0]
            # minX = data_to_send[ key ]['group0_second_feature'][0]
            maxX = 0
            minY = data_to_send[ key ]['group0_second_feature'][0]
            # minY = data_to_send[ key ]['group0_first_feature'][0]
            maxY = 0

            # for value in data_to_send[ key ]['group0_second_feature'] + data_to_send[ key ]['group1_second_feature']:
            for value in data_to_send[ key ]['group0_first_feature'] + data_to_send[ key ]['group1_first_feature']:
                if maxX < value:
                    maxX = value
                if minX > value:
                    minX = value
            
            # for value in data_to_send[ key ]['group0_first_feature'] + data_to_send[ key ]['group1_first_feature']:
            for value in data_to_send[ key ]['group0_second_feature'] + data_to_send[ key ]['group1_second_feature']:
                if maxY < value:
                    maxY = value
                if minY > value:
                    minY = value
            
            data_to_send[ key ]['minX'] = minX
            data_to_send[ key ]['maxX'] = maxX
            data_to_send[ key ]['minY'] = minY
            data_to_send[ key ]['maxY'] = maxY

            max_value = 0
            for value in data_to_send[ key ]['marker_data']['Importance']:
                if max_value < value:
                    max_value = value
            data_to_send[ key ]['marker_max'] = max_value
            data_to_send[ key ]['first_feature'] = first_feature
            data_to_send[ key ]['second_feature'] = second_feature
            
    # else:
    #     print(' Case 3')
    #     return False, False, '[Too Many Rows]::오류가 발생했습니다. 관리자에게 문의 바랍니다.'

    return True, True, {'data': data_to_send}

def saveFileData(file_data):
    n = CellLineSelectorInfo.objects.create(**file_data)

def presaveResults(request):
    if platform == 'win32':
        # url = "http://192.168.1.250:10015/api"
        url = "http://localhost:10015/api"
    else :
        url = "http://172.16.1.30:10015/api"

    cur = connection.cursor()

    actionType = request.POST.get('actionType')
    dependency = True if request.POST.get('dependency').upper() == 'TRUE' else False
    effect = True if request.POST.get('effect').upper() == 'TRUE' else False
    target_name = request.POST.get('main-search-keyword').upper()
    titles = request.POST.get('titles')

    is_best_combo = True if request.POST.get('is_best_combo').upper() == 'TRUE' else False

    left_num = request.POST.get('left_num')
    right_num = request.POST.get('right_num')
    # left_num = '49'
    # right_num = '60'

    print('target_name:', target_name)
    
    try:
        response = requests.request("POST", url, headers={ 'Content-Type': 'application/x-www-form-urlencoded' }, data={
            'state': '', 'operation': 'PRESAVE-RESULT', 'main_keyword': target_name, 'dependency': dependency, 'effect': effect,
            'asked_both': dependency and effect, 'left': left_num, 'right': right_num, 'titles': titles
        })
        
        print(response)

        with zipfile.ZipFile(io.BytesIO(response.content), 'r') as zip_ref:
            file_data = {}
            
            prev_index = ''

            for file_info in zip_ref.infolist():

                cur_index = file_info.filename.split('/')[0]
                filename = file_info.filename.split('/')[1]

                if prev_index != cur_index:
                    print('=========================================================================')
                    print(f" Entering folder: [{cur_index}]:", filename)
                    print('=========================================================================')

                    if len(file_data) > 0:
                        try:
                            with transaction.atomic():
                                saveFileData(file_data)

                        except Exception as e:
                            print('failed::', filename, ':', str(e))

                        file_data = {}

                print(filename)

                with zip_ref.open(file_info) as file: 
                
                    if filename.endswith('.csv'):
                        df = pd.read_csv(file)
                    elif filename.endswith('.json'):
                        data = json.load(file)
                    elif filename.endswith('.txt'):
                        content = file.read().decode('utf-8')
                    
                    if filename == 'a.txt':
                        print("a.txt:", content)
                        
                        file_data['title'] = content
                        file_data['gene_set_list'] = []

                        if 'df_depmap_all_minus_df' in file_data['title']:
                            file_data['gene_set_list'].append('df_depmap_all')
                            parts = file_data['title'].replace('_df_depmap_all_minus_', '_').split('_')
                        else:
                            parts = file_data['title'].split('_')
                        
                        gene_set_list= '_'.join(parts[4:]).split('_and_df_')
                        for i, gene_set in enumerate(gene_set_list):
                            if i == 0:
                                file_data['gene_set_list'].append(gene_set)
                            else:
                                file_data['gene_set_list'].append('df_' + gene_set)
                        
                        file_elements = file_data['title'].split('_')
                        file_data['target'] = file_elements[0]
                        file_data['dep_or_eff'] = file_elements[1]
                        file_data['dependency'] = True if file_elements[1] == 'Dependency' else False
                        file_data['effect'] = True if file_elements[1] == 'Effect' else False
                        file_data['left'] = float(file_elements[2])
                        file_data['right'] = float(file_elements[3])
                        file_data['is_best_combo'] = is_best_combo

                        print('target:', file_data['target'], ', dep_or_eff:', file_data['dep_or_eff'], ', dependency:', file_data['dependency'], ', effect:', file_data['effect'], ', left:', file_data['left'], ', right:', file_data['right'])
                        print('gene_set_list:',file_data['gene_set_list'])

                    elif filename == 'section2_important_features.json':
                        print("if filename == 'section2_important_features.json':")
                        file_data['feature_ranks'] = data
                    
                    elif filename == 'section2_top_marker_separation.txt':
                        print("elif filename == 'section2_top_marker_separation.txt':")
                        file_data['default_img'] = content

                    elif filename == 'section1_histogram.csv':
                        print("elif filename == 'section1_histogram.csv':")
                        file_data['histogram_data'] = {
                            "Bin_Left": df["Bin_Left"].tolist(),
                            "Bin_Right": df["Bin_Right"].tolist(),
                            "Count": df["Count"].tolist()
                        }

                    elif filename == 'section3_cells.csv':
                        print("elif filename == 'section3_cells.csv':")
                        # file_data['cell_data'] = {
                        #     "Cell name": df["Cell name"].tolist(),
                        #     "Lineage": df["Lineage"].tolist(),
                        #     "Relevance": [ round(float(elem), 3) for elem in df["Relevance"].tolist() ],
                        #     "Gene " + file_data['dep_or_eff']: [ round(elem, 3) for elem in df["Gene " + file_data['dep_or_eff']].tolist() ]
                        # }
                        file_data['cell_data'] = {
                            "Cell name": df["Cell name"].tolist(),
                            "Lineage": df["Lineage"].tolist(),
                            "Relevance": [ round(elem, 3) if not pd.isna(elem) else None for elem in df["Relevance"].tolist() ],
                            "Gene " + file_data['dep_or_eff']: [ round(elem, 3) if not pd.isna(elem) else None for elem in df["Gene " + file_data['dep_or_eff']].tolist() ],
                            'total_score': [ round(elem, 3) if not pd.isna(elem) else None for elem in df["Total Score"].tolist() ]
                        }
                    
                    elif filename == 'section4_markers.csv':
                        print("elif filename == 'section4_markers.csv':")

                        if len(df) > 2000:
                            df = df.iloc[:2000]
                        file_data['marker_data'] = {
                            "Feature": df["Feature"].tolist(),
                            # "Importance": df["Importance"].tolist()
                            "Importance": [ round(float(elem), 3) for elem in df["Importance"].tolist() ]
                        }
                        print('marker done')
                    
                    elif filename == 'section2_df.csv':
                        print("elif filename == 'section2_df.csv':")
                        # data = {column: df[column].tolist() for column in df.columns}

                        section2_labels_info = [info for info in zip_ref.infolist() if cur_index + '/section2_labels' in info.filename]
                        with zip_ref.open(section2_labels_info[0]) as section2_labels_file:
                            # 파일 내용 읽기
                            section2_labels_df = pd.read_csv(section2_labels_file)
                            section2_label_list = section2_labels_df["Label"].tolist()
                        
                        section2_chosen_info = [info for info in zip_ref.infolist() if cur_index + '/section2_chosen_cells' in info.filename]
                        with zip_ref.open(section2_chosen_info[0]) as section2_chosen_info_file:
                            # 파일 내용 읽기
                            section2_chosen_cells_df = pd.read_csv(section2_chosen_info_file)
                            section2_chosen_cell_list = section2_chosen_cells_df["0"].tolist()
                        
                        # section2_chosen_info = [info for info in zip_ref.infolist() if 'section2_chosen_cells' in info.filename]
                        section2_important_features = [info for info in zip_ref.infolist() if cur_index + '/section2_important_features' in info.filename]

                        # with zip_ref.open(section2_chosen_info[0]) as section2_chosen_info_file:
                        with zip_ref.open(section2_important_features[0]) as section2_important_features_file:
                            feature_ranks = json.load(section2_important_features_file)
                        
                        # print('feature_ranks:')
                        # print(feature_ranks)

                        # feature_ranks에 따라 열을 정렬
                        sorted_columns = sorted(feature_ranks, key=feature_ranks.get)
                        
                        df = df[sorted_columns]

                        print()
                        print()
                        print()
                        print('sorted df:')
                        print(df)
                        
                        
                        with zip_ref.open(file_info) as file:

                            group0_data = {'cell_name': []}
                            group1_data = {'cell_name': []}

                            # DataFrame의 각 행을 반복
                            for i, row in df.iterrows():

                                color_flag = section2_label_list[i]
                                chosen_cell = section2_chosen_cell_list[i]

                                if color_flag == 0:
                                    group0_data[ 'cell_name' ].append(chosen_cell)
                                elif color_flag == 1:
                                    group1_data[ 'cell_name' ].append(chosen_cell)

                                for column_name, item in row.items():
                                    item = round(item, 3)

                                    if color_flag == 0:                            
                                        if column_name in group0_data:
                                            group0_data[ column_name ].append(item)
                                            
                                        else:
                                            group0_data[ column_name ] = [ item ]
                                            

                                    elif color_flag == 1:
                                        if column_name in group1_data:
                                            group1_data[ column_name ].append(item)
                                            
                                        else:
                                            group1_data[ column_name ] = [ item ]
                                            

                                # print('group0_data:', group0_data)
                                # print('group1_data:', group1_data)

                                file_data['scatter_group0_data'] = group0_data
                                file_data['scatter_group1_data'] = group1_data
                prev_index = cur_index
            print('got out of loop')

            if len(file_data) > 0:
                try:
                    with transaction.atomic():

                        if CellLineSelectorInfo.objects.filter(title=file_data['title']).exists():
                            print(file_data['title'], 'already exists')
                        else:
                            saveFileData(file_data)
                        
                except Exception as e:
                    print('failed::', filename, ':', str(e))

            print('process done')

        return True, True, ''

    except requests.exceptions.HTTPError as err:
        print('error : ' + str(err))

def uploadCellLineSelectorGene(request):
    print('uploadCellLineSelectorGene')
    try:
        with transaction.atomic():
            normal_format = request.FILES.get('normal_format')
            tree_format = request.FILES.get('tree_format')
            
            if normal_format != None:
                # path = default_storage.save("raw_datas/"+cell_info.name, cell_info)
                # cell_info.seek(0)

                df = pd.read_csv(normal_format).drop_duplicates()

                for i, row in df.iterrows():
                    CellLineSelectorGeneNormalStructure.objects.create(**{
                        'category': df.at[i, 'category'],
                        'set': None if df.at[i, 'set'] == '' else df.at[i, 'set'],
                        'gene': None if df.at[i, 'genes'] == '' else df.at[i, 'genes'],
                    })

            if tree_format != None:
                df = pd.read_csv(tree_format).drop_duplicates()

                # for i, line in enumerate(tree_format.read().decode('euc-kr').split('\r\n')):
                for i, row in df.iterrows():
                    # print(i, '::', df.at[i, 'ID'], df.at[i, 'Genes'], df.at[i, 'Gene_Symbol'])
                    # print(ast.literal_eval(df.at[i, 'Gene_Symbol']))

                    CellLineSelectorGeneTreeStructure.objects.create(**{
                        'category': df.at[i, 'category'],
                        'code': df.at[i, 'code'],
                        'name': None if df.at[i, 'name'] == '' else df.at[i, 'name'],
                        'namespace': None if df.at[i, 'namespace'] == '' else df.at[i, 'namespace'],
                        'level': int(df.at[i, 'level']) if df.at[i, 'level'] != '' and df.at[i, 'level'] != None else None,
                        'parents': ast.literal_eval(df.at[i, 'parents']) if df.at[i, 'parents'] != '' and df.at[i, 'parents'] != None else [],
                        'children': ast.literal_eval(df.at[i, 'children']) if df.at[i, 'children'] != '' and df.at[i, 'children'] != None else [],
                        'definition': df.at[i, 'definition'] if df.at[i, 'definition'] != '' and df.at[i, 'definition'] != None else None,
                        'genes': ast.literal_eval(df.at[i, 'genes']) if df.at[i, 'genes'] != '' and df.at[i, 'genes'] != None else [],
                        'gene_symbols': ast.literal_eval(df.at[i, 'gene_symbol']) if df.at[i, 'gene_symbol'] != '' and df.at[i, 'gene_symbol'] != None else []
                    })
    except Exception as e:
        print("Exception::", e)
        return False, False, e

    try:
        with transaction.atomic():
            normal_format_to_display = request.FILES.get('normal_format_to_display')
            tree_format_to_display = request.FILES.get('tree_format_to_display')
            cell_names_map = request.FILES.get('cell_names_map')
            depmap_all_gene_list = request.FILES.get('depmap_all_gene_list')

            if normal_format_to_display != None:
                df = pd.read_csv(normal_format_to_display).drop_duplicates()

                for i, row in df.iterrows():
                    CellLineSelectorGeneNormalStructure.objects.filter(Q(category=df.at[i, 'category']) & Q(set=df.at[i, 'set'])).update(**{
                        'check_display': True
                    })
            
            if tree_format_to_display != None:
                df = pd.read_csv(tree_format_to_display).drop_duplicates()

                for i, row in df.iterrows():
                    CellLineSelectorGeneTreeStructure.objects.filter(Q(category=df.at[i, 'category']) & Q(code=df.at[i, 'code'])).update(**{
                        'check_display': True
                    })
            
            if depmap_all_gene_list != None:
                df = pd.read_csv(depmap_all_gene_list).drop_duplicates()

                for i, row in df.iterrows():
                    CellLineSelectorCellDepmapAllGene.objects.create(**{
                        'gene': df.at[i, 'gene'],
                    })
            
            if cell_names_map != None:
                df = pd.read_csv(cell_names_map).drop_duplicates()

                for i, row in df.iterrows():
                    CellLineSelectorCellMappingId.objects.create(**{
                        'cell_name': df.at[i, 'CellLineName'],
                        'model_id': df.at[i, 'ModelID']
                    })

    except Exception as e:
        print("Exception::", e)
        return False, False, e

    count_nodes = request.POST.get('count-nodes')
    print('count_nodes:', count_nodes)
    if count_nodes != None:
        CellLineSelectorGeneCount.objects.all().delete()

        rows = CellLineSelectorGeneNormalStructure.objects.raw(f"""
            select 1 as id, category, "set", count(gene) from cell_line_selector_gene_normal_structure
            where check_display=true
            group by category, "set"
            order by category, "set";
        """)

        for row in rows:
            descendants = get_descendant_list(structure='normal', category=row.category, set_name=row.set, code='')

            CellLineSelectorGeneCount.objects.create(**{
                'structure': 'normal', 'category': row.category, 'node': row.set, 'num_children': len(descendants), 'gene_list': descendants
            })

        rows = CellLineSelectorGeneTreeStructure.objects.filter(Q(check_display=True) & Q(check_discard=False))

        for row in rows:
            descendants = get_descendant_list(structure='tree', category=row.category, set_name='', code=row.code)
            # descendants = get_descendant_list(structure=structure, category=category, set_name='', code='GO:0003774')
            
            CellLineSelectorGeneCount.objects.create(**{
                'structure': 'tree', 'category': row.category, 'node': row.code, 'num_children': len(descendants), 'gene_list': descendants
            })

    try:
        with transaction.atomic():
            data_to_presave = request.FILES.get('data_to_presave')

            if data_to_presave:
                # 메모리에서 ZIP 파일 열기
                with zipfile.ZipFile(BytesIO(data_to_presave.read()), 'r') as zip_ref:
                    file_data = {}
                    current_folder = None
                    for file_info in zip_ref.infolist():
                        
                        if file_info.is_dir():
                            # 디렉토리 이름 출력
                            current_folder = file_info.filename
                            print('=========================================================================')
                            print(f" Entering folder: {current_folder}")
                            print('=========================================================================')
                            # print('file_data:', len(file_data))
                            
                            if len(file_data) > 0:
                                CellLineSelectorInfo.objects.create(**file_data)
                                file_data = {}

                        else:
                            
                            print(' file:', file_info.filename)
                            
                            file_data['title'] = file_info.filename.split('/')[1]

                            parts = file_data['title'].split('_')
                            file_data['gene_set_list'] = ['_'.join(parts[4:])]
                            
                            file_elements = file_data['title'].split('_')
                            file_data['target'] = file_elements[0]
                            file_data['dep_or_eff'] = file_elements[1]
                            file_data['dependency'] = True if file_elements[1] == 'Dependency' else False
                            file_data['effect'] = True if file_elements[1] == 'Effect' else False
                            file_data['left'] = float(file_elements[2])
                            file_data['right'] = float(file_elements[3])
                            file_data['is_best_combo'] = True

                            filename = file_info.filename.split('/')[2]

                            with zip_ref.open(file_info) as file:
                            
                                if filename.endswith('.csv'):
                                    df = pd.read_csv(file)
                                elif filename.endswith('.json'):
                                    data = json.load(file)
                                elif filename.endswith('.txt'):
                                    content = file.read().decode('utf-8')
                                
                                if filename == 'section2_important_features.json':
                                    file_data['feature_ranks'] = data
                                
                                elif filename == 'section2_top_marker_separation.txt':
                                    file_data['default_img'] = content

                                elif filename == 'section1_histogram.csv':
                                    file_data['histogram_data'] = {
                                        "Bin_Left": df["Bin_Left"].tolist(),
                                        "Bin_Right": df["Bin_Right"].tolist(),
                                        "Count": df["Count"].tolist()
                                    }

                                elif filename == 'section3_cells.csv':
                                    file_data['cell_data'] = {
                                        "Cell name": df["Cell name"].tolist(),
                                        "Lineage": df["Lineage"].tolist(),
                                        "Relevance": [ round(elem, 3) for elem in df["Relevance"].tolist() ],
                                        "Gene " + file_data['dep_or_eff']: [ round(elem, 3) for elem in df["Gene " + file_data['dep_or_eff']].tolist() ]
                                    }
                                
                                elif filename == 'section4_markers.csv':
                                    file_data['marker_data'] = {
                                        "Feature": df["Feature"].tolist()[:1000],
                                        "Importance": [ round(elem, 3) for elem in df["Importance"].tolist()[:1000] ]
                                    }
                                
                                elif filename == 'section2_df.csv':
                                    # data = {column: df[column].tolist() for column in df.columns}

                                    section2_labels_info = [info for info in zip_ref.infolist() if 'section2_labels' in info.filename]
                                    with zip_ref.open(section2_labels_info[0]) as section2_labels_file:
                                        # 파일 내용 읽기
                                        section2_labels_df = pd.read_csv(section2_labels_file)
                                        section2_label_list = section2_labels_df["Label"].tolist()
                                    
                                    section2_chosen_info = [info for info in zip_ref.infolist() if 'section2_chosen_cells' in info.filename]
                                    with zip_ref.open(section2_chosen_info[0]) as section2_chosen_info_file:
                                        # 파일 내용 읽기
                                        section2_chosen_cells_df = pd.read_csv(section2_chosen_info_file)
                                        section2_chosen_cell_list = section2_chosen_cells_df["0"].tolist()                                    

                                    group0_data = {'cell_name': []}
                                    group1_data = {'cell_name': []}

                                    # DataFrame의 각 행을 반복
                                    for i, row in df.iterrows():

                                        color_flag = section2_label_list[i]
                                        chosen_cell = section2_chosen_cell_list[i]

                                        if color_flag == 0:
                                            group0_data[ 'cell_name' ].append(chosen_cell)
                                        elif color_flag == 1:
                                            group1_data[ 'cell_name' ].append(chosen_cell)

                                        for column_name, item in row.items():
                                            item = round(item, 3)

                                            if color_flag == 0:                            
                                                if column_name in group0_data:
                                                    group0_data[ column_name ].append(item)
                                                    
                                                else:
                                                    group0_data[ column_name ] = [ item ]
                                                    

                                            elif color_flag == 1:
                                                if column_name in group1_data:
                                                    group1_data[ column_name ].append(item)
                                                    
                                                else:
                                                    group1_data[ column_name ] = [ item ]
                                                    

                                        # print('group0_data:', group0_data)
                                        # print('group1_data:', group1_data)

                                        file_data['scatter_group0_data'] = group0_data
                                        file_data['scatter_group1_data'] = group1_data

                    # print('=========================================================================')
                    # print(f" EOF")
                    # print('=========================================================================')
                    # print('file_data:', len(file_data))
                    if len(file_data) > 0:
                        CellLineSelectorInfo.objects.create(**file_data)

    except Exception as e:
        print("Exception::", e)
        return False, False, e


    return True, False, 'success'

def getCellLineSelectorGeneList(structure, category):
    # structure = request.POST.get('structure')
    # category = request.POST.get('category')

    print(structure, structure == 'normal')
    if structure == 'normal':
        print('category:', category)
        # 모든 엔트리를 모델에서 가져옵니다.
        entries = CellLineSelectorGeneNormalStructure.objects.filter(Q(category=category) & Q(check_display=True) & Q(check_discard=False)).distinct('category', 'set')
        print(len(entries))

        # 중첩된 딕셔너리를 만듭니다: tree[category][set_name] = genes의 집합
        tree = defaultdict(lambda: defaultdict(set))

        for entry in entries:
            # None이거나 빈 값들을 처리하여 기본 값 할당
            category = entry.category.strip() if entry.category and entry.category.strip() else 'Uncategorized'
            set_name = entry.set.strip() if entry.set and entry.set.strip() else 'No Set'
            gene = entry.gene.strip() if entry.gene and entry.gene.strip() else 'Unknown Gene'

            # 트리 구조에 데이터 추가
            tree[category][set_name].add(gene)

        # 원하는 포맷의 리스트로 변환
        result = []

        for category in sorted(tree.keys()):
            sets = tree[category]
            category_node = {
                'id': f"category_{category}",
                'text': category,
                # 'text': f'<span class="tree-label" category="{category}">{category} <span class="set-count" category="{category}"></span></span>',
                'children': [],
                'attributes': {'level': 0}
            }
            for set_name in sorted(sets.keys()):
                genes = sets[set_name]
                set_node = {
                    'id': set_name,
                    'text': f'<span class="tree-label" set="{ set_name }"><span class="tree-label-text">{ set_name }</span><b class="tree-num-children" set="{ set_name }"></b> <a href="#" class="show-genes" structure="normal" category="{category}" value="{ set_name }">보기</a></span>',
                    'children': [],
                    'attributes': {'level': 1}
                }
                # for gene in sorted(genes):
                #     gene_node = {
                #         'id': f"gene_{category}_{set_name}_{gene}",
                #         'text': gene,
                #         'children': [] # Gene은 리프 노드입니다.
                #     }
                    # set_node['children'].append(gene_node)
                category_node['children'].append(set_node)
            result.append(category_node)

        # return True, False, result
        return result

    if structure == 'tree':

        # Retrieve all nodes from the model
        nodes = CellLineSelectorGeneTreeStructure.objects.filter(Q(category=category) & Q(check_display=True) & Q(check_discard=False)).order_by('name')

        # Create a mapping from code to node instance for easy access
        code_to_node = {node.code: node for node in nodes}

        # Build a mapping from parent codes to their children codes
        code_to_children = defaultdict(list)
        for node in nodes:
            for parent_code in node.parents or []:
                code_to_children[parent_code].append(node.code)

        # Identify root nodes (nodes without parents)
        root_codes = [code for code, node in code_to_node.items() if not node.parents]

        # Recursive function to build the tree
        def build_subtree(code, parent_code):
            node = code_to_node[code]
            children_codes = code_to_children.get(code, [])
            return {
                'id': node.code,
                # 'text': node.name,
                'text': f'<span class="tree-label" code="{node.code}"><span class="tree-label-text">({ node.code }) { node.name }</span><b class="tree-num-children" code="{ node.code }"></b> <a href="#" class="show-genes" structure="tree" category="{category}" node_name="{ node.name }" value="{ node.code }">보기</a></span>',
                'children': [build_subtree(child_code, code) for child_code in children_codes],
                'attributes': {'level': node.level, 'parent': parent_code}
            }

        # Build the tree starting from root nodes
        tree = [build_subtree(code, None) for code in root_codes]

        # # If you want to include a single root node with id 0
        # tree_with_root = [{
        #     'id': 0,
        #     'text': 'Root',
        #     'children': tree
        # }]

        # return True, False, tree
        return tree

def checkKeywordFromDepmap(request):
    keyword = request.POST.get('keyword')
    print('checkKeywordFromDepmap::keyword:', keyword)

    CellLineSelectorTracking.objects.create(**{
        'owner_id': request.user.id,
        'action_type': request.POST.get('actionType'),
        'search_content': {
            'target': keyword,
        }
    })

    if CellLineSelectorCellDepmapAllGene.objects.filter(gene__iexact=keyword).exists():
        return True, True, ''
    else:
        return True, True, '해당 단백질은 존재하지 않습니다.'

def filterCellLineSelectorGeneList(request):
    keyword = request.POST.get('keyword')
    print('keyword:', keyword)

    CellLineSelectorTracking.objects.create(**{
        'owner_id': request.user.id,
        'action_type': request.POST.get('actionType'),
        'search_content': {
            'target': keyword,
        }
    })

    cur = connection.cursor()

    #===================================================================================================
    # gene이 있는 set list
    #===================================================================================================
    cur.execute(f"""
        select category, count("set") from (
            select distinct on (category, "set") * from cell_line_selector_gene_normal_structure
            where check_display=true and gene ilike '{keyword}' and check_discard=false
        ) t1
        group by category;
    """)

    set_list = [{'category': row[0], 'count': row[1]} for row in cur.fetchall()]

    cur.execute(f"""
        select category, "set", count(gene) from (
            select distinct on (category, "set", gene) * from cell_line_selector_gene_normal_structure
            where check_display=true and gene ilike '{keyword}' and check_discard=false
        ) t1
        group by category, "set";
    """)

    normal_list = [{'category': row[0], 'set': row[1], 'count': row[2]} for row in cur.fetchall()]

    #===================================================================================================
    # gene이 있는 code list
    #===================================================================================================
    # cur.execute(f"""
    #     select category, code from (
    #         select * from cell_line_selector_gene_tree_structure
    #         where check_display=true and gene_symbols::text ilike '%"{keyword}"%'
    #     ) t1;
    # """)

    cur.execute(f"""
        select category, node as code from cell_line_selector_gene_count
        where structure='tree' and gene_list::text ilike '%"{keyword}"%';
    """)

    code_list = [{'category': row[0], 'code': row[1]} for row in cur.fetchall()]

    # cur.execute(f"""
    #     select category, count(code) from (
    #         select * from cell_line_selector_gene_tree_structure
    #         where check_display=true and gene_symbols::text ilike '%"{keyword}"%'
    #     ) t1
    #     group by category;
    # """)

    cur.execute(f"""        
        select category, count(node) from cell_line_selector_gene_count
        where structure='tree' and gene_list::text ilike '%"{keyword}"%'
        group by category;
    """)

    tree_list = [{'category': row[0], 'count': row[1]} for row in cur.fetchall()]

    return True, True, {'set_list': set_list, 'normal_list': normal_list, 'code_list': code_list, 'tree_list': tree_list}
    
def get_descendant_list(structure='', category='', set_name='', code=''):

    if structure == 'normal':
        rows = CellLineSelectorGeneNormalStructure.objects.raw(f"""
            select distinct on (gene) 1 as id, category, "set", gene from cell_line_selector_gene_normal_structure
            where category='{category}' and "set"='{set_name}' and check_discard=false
        """)

        return [row.gene for row in rows]

    if structure == 'tree':
        visited = set()

        def dfs(current_code):
            if current_code in visited:
                return []
            visited.add(current_code)
            try:
                node = CellLineSelectorGeneTreeStructure.objects.get(code=current_code)
            except CellLineSelectorGeneTreeStructure.DoesNotExist:
                return []
            # count = 0
            gene_symbol_list = []
            if current_code != code and node.category == category:
                # count += 1
                # gene_symbol_list.append(node.gene_symbols)
                gene_symbol_list = list(set(gene_symbol_list) | set(node.gene_symbols))

            if node.children:
                for child_code in node.children:
                    gene_symbol_list = list(set(dfs(child_code)) | set(gene_symbol_list))
            return gene_symbol_list

        gene_symbol_list = dfs(code)
        return gene_symbol_list
    
def compare_requests(cur_req, prev_req):
    new_req = []
    del_req = []

    # Convert lists to dictionaries for easier comparison
    cur_dict = {item['category']: item for item in cur_req}
    prev_dict = {item['category']: item for item in prev_req}

    # Find new requests
    for category, cur_item in cur_dict.items():
        prev_item = prev_dict.get(category, {'checked_list': []})
        cur_values = {item['value'] for item in cur_item['checked_list']}
        prev_values = {item['value'] for item in prev_item['checked_list']}

        new_values = cur_values - prev_values
        if new_values:
            new_req.append({
                'structure': cur_item['structure'],
                'category': category,
                'checked_list': [item for item in cur_item['checked_list'] if item['value'] in new_values]
            })

    # Find deleted requests
    for category, prev_item in prev_dict.items():
        cur_item = cur_dict.get(category, {'checked_list': []})
        cur_values = {item['value'] for item in cur_item['checked_list']}
        prev_values = {item['value'] for item in prev_item['checked_list']}

        del_values = prev_values - cur_values
        if del_values:
            del_req.append({
                'structure': prev_item['structure'],
                'category': category,
                'checked_list': [item for item in prev_item['checked_list'] if item['value'] in del_values]
            })

    return new_req, del_req

def update_prev_req_with_new_and_del(prev_req, new_req, del_req):
    # Convert prev_req to a dictionary for easier manipulation
    prev_dict = {item['category']: item for item in prev_req}

    # Add new requests to prev_req
    for new_item in new_req:
        category = new_item['category']
        if category in prev_dict:
            # Update existing category with new items
            existing_values = {item['value'] for item in prev_dict[category]['checked_list']}
            for new_checked_item in new_item['checked_list']:
                if new_checked_item['value'] not in existing_values:
                    prev_dict[category]['checked_list'].append(new_checked_item)
        else:
            # Add new category
            prev_dict[category] = new_item

    # Remove deleted requests from prev_req
    for del_item in del_req:
        category = del_item['category']
        if category in prev_dict:
            prev_checked_list = prev_dict[category]['checked_list']
            del_values = {item['value'] for item in del_item['checked_list']}
            prev_dict[category]['checked_list'] = [
                item for item in prev_checked_list if item['value'] not in del_values
            ]

    # Convert back to list
    updated_prev_req = list(prev_dict.values())
    return updated_prev_req

def getMatchingCellLineSelectorGeneNum(request):
    list_to_req = json.loads(request.POST.get('list_to_req'))
    prev_req = json.loads(request.POST.get('prev_req'))
    prevGeneList = json.loads(request.POST.get('prevGeneList'))

    # print("=====================================================================================")
    # print("=====================================================================================")
    print("   getMatchingCellLineSelectorGeneNum")
    # print("=====================================================================================")
    # print("=====================================================================================")
    
    # print('cur_req:', list_to_req)
    # print('prev_req:', prev_req)

    if prev_req != None:
        new_req, del_req = compare_requests(list_to_req, prev_req)
        print('new_req:', new_req)
        print('del_req:', del_req)

    #================================================================================================
    #================================================================================================
    # set/code 별 gene count
    #================================================================================================
    #================================================================================================
    for elem in list_to_req if prev_req == None else new_req:
        structure = elem['structure']
        category = elem['category']
        checked_list = elem['checked_list']

        if len(checked_list) == 0:
            continue
    
        for i, item in enumerate(checked_list):

            obj = CellLineSelectorGeneCount.objects.filter(Q(structure=structure) & Q(category=category) & Q(node=item['value'])).last()

            if obj != None:
                descendants = obj.gene_list
            else:
                if structure == 'normal':
                    
                    descendants = get_descendant_list(structure=structure, category=category, set_name=item['value'], code='')
                else:
                    descendants = get_descendant_list(structure=structure, category=category, set_name='', code=item['value'])
                    # descendants = get_descendant_list(structure=structure, category=category, set_name='', code='GO:0003774')

            item['count'] = len(descendants)
            prevGeneList += descendants

    if prev_req != None:
        gene_to_delete = []
        for elem in del_req:
            structure = elem['structure']
            category = elem['category']
            checked_list = elem['checked_list']

            if len(checked_list) == 0:
                continue
            
            for i, item in enumerate(checked_list):

                obj = CellLineSelectorGeneCount.objects.filter(Q(structure=structure) & Q(category=category) & Q(node=item['value'])).last()

                if obj != None:
                    descendants = obj.gene_list
                else:
                    if structure == 'normal':
                        descendants = get_descendant_list(structure=structure, category=category, set_name=item['value'], code='')
                    else:
                        descendants = get_descendant_list(structure=structure, category=category, set_name='', code=item['value'])
                
                gene_to_delete += descendants

        count_a = Counter(prevGeneList)
        count_b = Counter(gene_to_delete)
        result_counter = count_a - count_b
        prevGeneList = list(result_counter.elements())
    
    #================================================================================================
    #================================================================================================
    # category 별 gene count
    #================================================================================================
    #================================================================================================
    if prev_req != None:
        updated_prev_req = update_prev_req_with_new_and_del(prev_req, new_req, del_req)
        # print('updated_prev_req:', updated_prev_req)

    gene_list_per_cat = {}
    for elem in list_to_req if prev_req == None else updated_prev_req:
        structure = elem['structure']
        category = elem['category']
        checked_list = elem['checked_list']
        gene_list_per_cat[ elem['category'] ] = 0

        if len(checked_list) == 0:
            continue

        if structure == 'tree':
            code_str = ''
            
            for i, item in enumerate(checked_list):
                code_str += "'" + item['value'] + "'" + ("" if i == len(checked_list) - 1 else ",")
            print('code_str:', code_str)
            
            rows = CellLineSelectorGeneNormalStructure.objects.raw(f'''
                SELECT 1 AS id, COUNT(distinct gene) FROM (
                    SELECT jsonb_array_elements_text(gene_list) AS gene FROM cell_line_selector_gene_count 
                    WHERE node IN ({code_str})
                ) t1
            ''')
            print('count:', rows[0].count)

        elif structure == 'normal':
            
            set_str = ''
            for i, item in enumerate(checked_list):
                set_str += "'" + item['value'] + "'" + ("" if i == len(checked_list) - 1 else ",")

            rows = CellLineSelectorGeneNormalStructure.objects.raw(f'''
                select 1 as id, count(gene) from (
                    select distinct on (gene) gene from cell_line_selector_gene_normal_structure
                    where category='{category}' AND "set" IN ({set_str}) 
                ) genes;
            ''')

        gene_list_per_cat[ category ] = rows[0].count
    
    return True, True, {
        'list_to_req': list_to_req if prev_req == None else updated_prev_req, 
        'gene_list_per_cat': gene_list_per_cat, 
        'total_list': prevGeneList, 
        'gene_set_list': list(set(prevGeneList))
    }

def getChildrenGeneList(request):
    structure = request.POST.get('structure')
    category = request.POST.get('category')
    value = request.POST.get('value')

    CellLineSelectorTracking.objects.create(**{
        'owner_id': request.user.id,
        'action_type': request.POST.get('actionType'),
        'search_content': {
            'structure': structure,
            'category': category,
            'value': value,
        }
    })

    print("getChildrenGeneList:", structure, category, value)

    descendant_list = []

    obj = CellLineSelectorGeneCount.objects.filter(Q(structure=structure) & Q(category=category) & Q(node=value)).last()

    if obj != None:
        descendant_list = obj.gene_list
    else:
        if structure == 'tree':
            descendant_list = get_descendant_list(structure=structure, category=category, set_name='', code=value)
            # descendant_count = get_descendant_list(structure=structure, category=category, set_name='', code='GO:0003774')
        else:
            descendant_list = get_descendant_list(structure=structure, category=category, set_name=value, code='')
    
    descendant_list.sort()
    
    return True, True, descendant_list

def getGptMessages(request):
    thread_id = request.POST.get('thread_id')
    print("getGptMessages:", thread_id)

    CellLineSelectorTracking.objects.create(**{
        'owner_id': request.user.id,
        'action_type': request.POST.get('actionType'),
        'search_content': {
            'thread_id': thread_id
        }
    })
    
    return True, True, {'thread_title': CellLineSelectorChatGptThread.objects.get(id=thread_id).title, 'message_list':[ {'role': row.role, 'content': row.content} for row in CellLineSelectorChatGptMessage.objects.filter(Q(thread_id=thread_id)).exclude(role='system').order_by('id')]}

def cellLineSelectorChatGpt(request):

    if platform == 'win32':
        # url = "http://192.168.1.250:10015/api"
        url = "http://localhost:10015/api"
    else :
        url = "http://172.16.1.30:10015/api"

    try:
        state = request.POST.get('state')
        operation = request.POST.get('operation')
        main_keyword = request.POST.get('main-search-keyword').upper()
        chatgpt_keyword = request.POST.get('chatgpt-keyword')
        new_content = request.POST.get('content')

        CellLineSelectorTracking.objects.create(**{
            'owner_id': request.user.id,
            'action_type': request.POST.get('actionType'),
            'search_content': {
                'state': state,
                'target': main_keyword,
                'operation': operation,
                'chatgpt_keyword': chatgpt_keyword
            }
        })

        if operation == 'GPT-BIOMARKER' or operation == 'GPT-CELL':
            if state == 'NEW':
                title = '단백질 "' + main_keyword + '"과 ' + request.POST.get('type') + ' "' + chatgpt_keyword + '" 에 대한 논문'
                thread_id = CellLineSelectorChatGptThread.objects.create(**{
                    'title': title,
                    'owner_id': request.user.id
                }).id

                messages = []
                
            elif state == 'ONGOING':
                thread_id = request.POST.get('thread_id')
                title = CellLineSelectorChatGptThread.objects.get(id=thread_id).title

                messages = [ {'role': row.role, 'content': row.content} for row in CellLineSelectorChatGptMessage.objects.filter(Q(thread_id=thread_id)) ]
                messages.append({'role': 'user', 'content': new_content})

            # print('messages:', messages)
            response = requests.request("POST", url, headers={ 'Content-Type': 'application/x-www-form-urlencoded' }, data={
                'state': state, 'operation': operation, 'main_keyword': main_keyword, 'chatgpt_keyword': chatgpt_keyword,
                'messages': json.dumps(messages)
            })
            response = json.loads(response.text)

            if response.get('result_code') == "0000" :
                result = response.get('result')

                if state == 'NEW':
                    for elem in result['messages']:
                        CellLineSelectorChatGptMessage.objects.create(**{
                            'thread_id': thread_id, 'role': elem['role'], 'owner_id': request.user.id,
                            'content': f"GPT야, Protein '{main_keyword}'과 {request.POST.get('type')} '{chatgpt_keyword}'과 같이 초록에 등장하는 논문을 검색해줘."
                        })
                elif state == 'ONGOING':
                    CellLineSelectorChatGptMessage.objects.create(**{
                        'thread_id': thread_id, 'role': 'user', 'content': new_content, 'owner_id': request.user.id
                    })
                
                CellLineSelectorChatGptMessage.objects.create(**{
                    'thread_id': thread_id, 'role': 'assistant', 'content': result['result'], 'owner_id': request.user.id
                })

                result['title'] = title
                result['thread_id'] = thread_id
                
                print('success cellLineSelectorApi')
                # print(result)
            else :
                print('error : ' + response.get('result'))
                result = None

    except requests.exceptions.HTTPError as err:
        print('error : ' + str(err))

    return True, True, result

def cellLineSelectorChangeFeatures(request):
    cur = connection.cursor()

    if platform == 'win32':
        # url = "http://192.168.1.250:10015/api"
        url = "http://localhost:10015/api"
    else :
        url = "http://172.16.1.30:10015/api"

    try:
        state = request.POST.get('state')
        operation = request.POST.get('operation')
        first_feature = request.POST.get('first_feature')
        second_feature = request.POST.get('second_feature')
        main_keyword = request.POST.get('main-search-keyword')
        current_searched_title = request.POST.get('current_searched_title')

        CellLineSelectorTracking.objects.create(**{
            'owner_id': request.user.id,
            'action_type': request.POST.get('actionType'),
            'search_title': current_searched_title,
            'search_content': {
                'first_feature': first_feature,
                'second_feature': second_feature
            }
        })

        # print('messages:', messages)
        response = requests.request("POST", url, headers={ 'Content-Type': 'application/x-www-form-urlencoded' }, data={
            'state': state, 'operation': 'CHANGE-FEATURE', 'title': current_searched_title, 'messages': [],
            'first_feature': first_feature, 'second_feature': second_feature, 
            # 'feature_dict': json.dumps({
            #     first_feature: data['group0_first_feature'] + data['group1_first_feature'],
            #     second_feature: data['group0_second_feature'] + data['group1_second_feature']
            # }), 'labels': json.dumps({'Label': [ 0 for i in range(len(data['group0_second_feature']))] + [ 1 for i in range(len(data['group1_second_feature']))]})
        })
        response = json.loads(response.text)

        if response.get('result_code') == "0000":
            # print("response.get('result'):", response.get('result'))
            result = response.get('result')

            print('success cellLineSelectorChangeFeatures')
            # print(result)
            # result['result']['data']['first_feature'] = first_feature
            # result['result']['data']['second_feature'] = second_feature
            # result['result']['data']['minX'] = minX
            # result['result']['data']['maxX'] = maxX
            # result['result']['data']['minY'] = minY
            # result['result']['data']['maxY'] = maxY

            # result['result']['data']['group0_first_feature'] = data['group0_first_feature']
            # result['result']['data']['group0_second_feature'] = data['group0_second_feature']
            # result['result']['data']['group0_cell_name'] = data['group0_cell_name']
            # result['result']['data']['group1_first_feature'] = data['group1_first_feature']
            # result['result']['data']['group1_second_feature'] = data['group1_second_feature']
            # result['result']['data']['group1_cell_name'] = data['group1_cell_name']
        else:
            print('error : ' + response.get('result'))
            result = None
            return False, False, str(response.get('result'))

    except requests.exceptions.HTTPError as err:
        print('error : ' + str(err))
        return False, False, str(err)

    return True, True, result

def downloadSection(request):
    if platform == 'win32':
        # url = "http://192.168.1.250:10015/api"
        url = "http://localhost:10015/api"
    else :
        url = "http://172.16.1.30:10015/api"
    
    # target_gene = request.POST.get('target_gene')
    # gene_set = json.loads(request.POST.get('genes'))
    # use_dependency = True if request.POST.get('dependency') != '' else False
    # use_effect = True if request.POST.get('effect') != '' else False

    dependency = None if request.POST.get('dependency') == '' else request.POST.get('dependency')
    effect = None if request.POST.get('effect') == '' else request.POST.get('effect')

    print('effect:', effect, ', dependency:', dependency)

    # data = json.loads(request.POST.get('data'))

    CellLineSelectorTracking.objects.create(**{ 'owner_id': request.user.id, 'action_type': request.POST.get('actionType'), 'search_content': { 'dependency': dependency, 'effect': effect } })

    try:
        response = requests.request("POST", url, headers={ 'Content-Type': 'application/x-www-form-urlencoded' }, data={
            'state': '', 'operation': 'DOWNLOAD-EXCEL', 'main_keyword': '', 'dependency': dependency, 'effect': effect,
            'asked_both': None, 'left': None, 'right': None, 'titles': None
        })
        # response = json.loads(response.text)
        # print(response)

        response.raise_for_status()

        # 바이너리 응답을 Django HttpResponse로 감싸기
        django_response = HttpResponse(
            response.content,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        django_response['Content-Disposition'] = 'attachment; filename="gene_analysis.xlsx"'

        return django_response

    except requests.exceptions.HTTPError as err:
        print('error : ' + str(err))
        return False, False, str(err)

    # return save_sections34(target_gene, gene_list, use_dependency, use_effect, section3_df, section4_df)

def addTrackingData(request):
    action_type = request.POST.get('action_type')
    track_data = json.loads(request.POST.get('track_data'))

    CellLineSelectorTracking.objects.create(**{
        'owner_id': request.user.id,
        'action_type': action_type,
        'search_content': track_data
    })

    return True, True, ''

########################################################
#           Solublility Deep Learning                  #
########################################################
# 내부 API
def getSolubilityPreditFile(request) :
    file = request.FILES["file"]
    try :
        read = file.read().decode('utf8')
        readLine = read.split('\n')

        solubility_predits = []
        for line in readLine :
            if line == "" : continue

            arr = line.split(',')
            name = arr[0]
            smiles = arr[1]

            molFromSmiles = Chem.MolFromSmiles(smiles)
            svg_img = moltosvg(molFromSmiles)

            solubility_predit = getSolubilityPreditApi(smiles)
            solubility_predits.append({
                "name": name,
                "value": solubility_predit,
                "smiles": smiles,
                "img": svg_img,
            })
    except Exception as e :
        print("Exception::", e)
        return False, e

    return solubility_predits

def getSolubilityPredit(request) :
    data = json.loads(request.body)["data"]

    smiles = data["smiles"]
    solubility_predit = getSolubilityPreditApi(smiles)

    solubility_predits = []
    molFromSmiles = Chem.MolFromSmiles(smiles)
    svg_img = moltosvg(molFromSmiles)

    solubility_predits.append({
        "name": "",
        "value": solubility_predit,
        "smiles": smiles,
        "img": svg_img,
    })
    return solubility_predits

'''
def getSolubilityPreditApi(smiles) :
    hostname = socket.gethostname()
    if "VN-LeeSeunghwan" == hostname or "VN-JeongJaeheon" == hostname or "VORONOI-STAGE" == hostname:
        url = "http://192.168.1.250:10005/api/solubility_predit"
    else :
        url = "http://172.16.1.237:10007/api/solubility_predit"

    solubility_predit = ""

    try:
        encode_smiles = parse.quote(smiles, safe='()', encoding="utf-8")
        payload = 'smiles='+encode_smiles
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        #response = "{\"result\": \"5.55555\", \"result_code\":\"0000\"}"
        #result = json.loads(response)

        if result.get('result_code') == "0000" :
            solubility_predit = result.get('result')
            print('success getSolubilityPreditApi')
        else :
            print('error : ' + result.get('result'))

    except requests.exceptions.HTTPError as err:
        print('error : ' + str(err))

    return solubility_predit
'''

#############################################################################
############################### 3DPSA S #####################################
#############################################################################
def get3dpsaDatas(request) :
    cur = connection.cursor()

    keyword = request.POST.get('keyword')
    smiles = request.POST.get('smile')

    where = f"AND u.owner_id = {request.user.id} "
    if keyword != None and keyword != "" :
        where += f"AND u.name ilike '%{keyword}%' "
    
    start = request.POST.get('start')
    length = request.POST.get('length')
    orderArr = []
    orderDirArr = []
    for i in range(20) :
        order = request.POST.get('order['+str(i)+'][column]')
        if order != None :
            orderArr.append(order)
            orderDirArr.append(request.POST.get('order['+str(i)+'][dir]'))

    orderPos = get3dpsaOrderMulti(orderArr, orderDirArr)

    orderStr = " ORDER BY " + orderPos
    limitStr = " LIMIT " + length + " OFFSET " + start
    
    cur.execute(f"select u.id as id, name, smiles, svg_img, status, result, date_created, comment, mem.mem_name \
                from utility_3dpsa_info u \
                LEFT JOIN vw_member_info mem ON u.owner_id = mem.owner_id \
                WHERE NOT check_discard \
                {where} \
                {orderStr} \
                {limitStr} \
                ", )
    
    dataList = dictfetchall(cur)

    index = 0
    if smiles != None and smiles != '':
        dataList1 = []
        mol_block = request.POST.get('mol_block')
        mol = Chem.MolFromMolBlock(mol_block)
        normalSmiles = Chem.MolToSmiles(mol)
        mol = SaltRemover().StripMol(mol)
        strippedSmiles = Chem.MolToSmiles(mol)    

        smilesFromUser = request.POST.get('smile')
        searchType = request.POST.get('radio_search_type')
        minSimilarity = float(request.POST.get('minSimilarity'))
        maxSimilarity = float(request.POST.get('maxSimilarity'))

        molFromUser = Chem.MolFromSmiles(smilesFromUser)

        tq = rdTautomerQuery.TautomerQuery(molFromUser)

        for data in dataList :
            molFromDb = Chem.MolFromSmiles(data.get('smiles'))

            if searchType == 'substructure' and tq.IsSubstructOf(molFromDb):
                dataList1.append(data)
                index += 1
            elif searchType == 'identical' and is_same_mol(molFromUser, molFromDb):
                dataList1.append(data)
                index += 1
            elif searchType == 'similarity':
                fp_morgan_user = AllChem.GetMorganFingerprint(molFromUser, 2)
                fp_morgan_db = AllChem.GetMorganFingerprint(molFromDb, 2)
                realSimilarity = DataStructs.DiceSimilarity(fp_morgan_user, fp_morgan_db) * 100
                if (minSimilarity <= realSimilarity and realSimilarity <= maxSimilarity):
                    dataList1.append(data)
                    index += 1
        

    cur.execute(f"select count(id) as cnt \
                from utility_3dpsa_info u \
                where not check_discard \
                {where} \
            ", )
    countResult = dictfetchall(cur)
    
    cnt = countResult[0].get('cnt')
    if smiles != None and smiles != '' :
        cnt = index
        dataList = dataList1
    list_search_ids = []
    message = ""
    search_history = []

    returnVal = {"data":dataList, "recordsTotal":cnt, "recordsFiltered": cnt, "list_search_ids":list_search_ids, "message":message, "search_history":search_history}
    if cur != None :
        cur.close()
    return returnVal

def is_same_mol(mol1, mol2, useChirality=True):
    return mol1.HasSubstructMatch(mol2, useChirality=useChirality) and mol2.HasSubstructMatch(mol1, useChirality=useChirality)

def set3dpsaData(request) :
    url = "http://172.16.1.30:10009//api/calculate"
    # url = "http://192.168.1.250:10009//api/calculate"

    mol_block = request.POST.get('mol_block')
    smiles = request.POST.get('smile')
    psa_name = request.POST.get("psa_name")
    comment = request.POST.get("comment")

    mol = Chem.MolFromMolBlock(mol_block)
    normalSmiles = Chem.MolToSmiles(mol)
    mol = SaltRemover().StripMol(mol)
    strippedSmiles = Chem.MolToSmiles(mol)

    mol = get_scaled_mol(mol)
    svg_img = moltosvg(mol)    

    rtn = {}
    try :
        with transaction.atomic():
            data = {
                'owner_id':request.user.id,
                'name':psa_name,
                'smiles':strippedSmiles,
                'svg_img':svg_img,
                'mol_block':mol_block,
                'status':'PENDING',
                'comment':comment,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now()
            }

            _3dpsa = Utility3DPSAInfo.objects.create(**data)
            payload = json.dumps({
                # "unique_key": psa_name + "@_@" + str(_3dpsa.id),
                "unique_key": str(_3dpsa.id),
                "smiles": strippedSmiles,
                "tp" : "PSA"
            })
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            rtn = {
                'result_code':'0000',
                'result_msg':'success'
            }
    except Exception as e :
        pass
        rtn = {
            'result_code':'9999',
            'result_msg':str(e)
        }

    return rtn


# def get3dpsaData(request) :

#     dataList = []
#     cnt = 0
#     list_search_ids = []
#     message = ""
#     search_history = []



#     returnVal = {"data":dataList, "recordsTotal":cnt, "recordsFiltered": cnt, "list_search_ids":list_search_ids, "message":message, "search_history":search_history}



def get3dpsaOrderMulti(posArr, dirArr) :
    columns = [
        'name', 'svg_img', 'status', 'result', 'mem_name', 'date_created', 'comment'
    ]
    returnOrder = ''
    i = 0
    for pos in posArr :
        if i != 0 :
            returnOrder += ", "

        if pos == '0' :
            returnOrder += 'name'
        elif pos == '1' :
            returnOrder += 'svg_img'
        elif pos == '2' :
            returnOrder += 'status'
        elif pos == '3' :
            returnOrder += 'result'
        elif pos == '4' :
            returnOrder += 'mem_name'
        elif pos == '5' :
            returnOrder += 'date_created'
        elif pos == '6' :
            returnOrder += 'comment'
        else :
            returnOrder += 'date_created'

        returnOrder += ' '+dirArr[i]
        i+=1

    return returnOrder



#############################################################################
############################### 3DPSA E #####################################
#############################################################################


#############################################################################
################################ ESOL S #####################################
#############################################################################
def getEsolDatas(request) :
    cur = connection.cursor()

    keyword = request.POST.get('keyword')
    smiles = request.POST.get('smile')

    start = request.POST.get('start')
    length = request.POST.get('length')
    orderArr = []
    orderDirArr = []
    for i in range(20) :
        order = request.POST.get('order['+str(i)+'][column]')
        if order != None :
            orderArr.append(order)
            orderDirArr.append(request.POST.get('order['+str(i)+'][dir]'))

    orderPos = getEsolOrderMulti(orderArr, orderDirArr)

    orderStr = " ORDER BY " + orderPos
    limitStr = " LIMIT " + length + " OFFSET " + start

    where = f"AND u.owner_id = {request.user.id} "
    if keyword != None and keyword != "" :
        where += f"AND u.name ilike '%{keyword}%' "
    
    cur.execute(f"select u.id as id, name, smiles, svg_img, status, result, date_created, comment, mem.mem_name \
                from utility_esol_info u \
                LEFT JOIN vw_member_info mem ON u.owner_id = mem.owner_id \
                WHERE NOT check_discard \
                {where} \
                {orderStr} \
                {limitStr} \
                ", )
    dataList = dictfetchall(cur)

    index = 0
    if smiles != None and smiles != '':
        dataList1 = []
        mol_block = request.POST.get('mol_block')
        mol = Chem.MolFromMolBlock(mol_block)
        normalSmiles = Chem.MolToSmiles(mol)
        mol = SaltRemover().StripMol(mol)
        strippedSmiles = Chem.MolToSmiles(mol)    

        smilesFromUser = request.POST.get('smile')
        searchType = request.POST.get('radio_search_type')
        minSimilarity = float(request.POST.get('minSimilarity'))
        maxSimilarity = float(request.POST.get('maxSimilarity'))

        molFromUser = Chem.MolFromSmiles(smilesFromUser)

        tq = rdTautomerQuery.TautomerQuery(molFromUser)

        for data in dataList :
            molFromDb = Chem.MolFromSmiles(data.get('smiles'))

            if searchType == 'substructure' and tq.IsSubstructOf(molFromDb):
                dataList1.append(data)
                index += 1
            elif searchType == 'identical' and is_same_mol(molFromUser, molFromDb):
                dataList1.append(data)
                index += 1
            elif searchType == 'similarity':
                fp_morgan_user = AllChem.GetMorganFingerprint(molFromUser, 2)
                fp_morgan_db = AllChem.GetMorganFingerprint(molFromDb, 2)
                realSimilarity = DataStructs.DiceSimilarity(fp_morgan_user, fp_morgan_db) * 100
                if (minSimilarity <= realSimilarity and realSimilarity <= maxSimilarity):
                    dataList1.append(data)
                    index += 1
        

    cur.execute(f"select count(id) as cnt \
                from utility_esol_info u \
                where not check_discard \
                {where} \
            ", )
    countResult = dictfetchall(cur)
    
    cnt = countResult[0].get('cnt')
    if smiles != None and smiles != '' :
        cnt = index
        dataList = dataList1
    list_search_ids = []
    message = ""
    search_history = []

    returnVal = {"data":dataList, "recordsTotal":cnt, "recordsFiltered": cnt, "list_search_ids":list_search_ids, "message":message, "search_history":search_history}
    if cur != None :
        cur.close()
    return returnVal

# def is_same_mol(mol1, mol2, useChirality=True):
#     return mol1.HasSubstructMatch(mol2, useChirality=useChirality) and mol2.HasSubstructMatch(mol1, useChirality=useChirality)

def setEsolData(request) :
    url = "http://172.16.1.30:10009//api/calculate"

    mol_block = request.POST.get('mol_block')
    smiles = request.POST.get('smile')
    psa_name = request.POST.get("psa_name")
    comment = request.POST.get("comment")

    mol = Chem.MolFromMolBlock(mol_block)
    normalSmiles = Chem.MolToSmiles(mol)
    mol = SaltRemover().StripMol(mol)
    strippedSmiles = Chem.MolToSmiles(mol)

    mol = get_scaled_mol(mol)
    svg_img = moltosvg(mol)    

    rtn = {}
    try :
        with transaction.atomic():
            data = {
                'owner_id':request.user.id,
                'name':psa_name,
                'smiles':strippedSmiles,
                'svg_img':svg_img,
                'mol_block':mol_block,
                'status':'PENDING',
                'comment':comment,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now()
            }

            esol = UtilityEsolInfo.objects.create(**data)
            payload = json.dumps({
                # "unique_key": psa_name + "@_@" + str(_3dpsa.id),
                "unique_key": str(esol.id),
                "smiles": strippedSmiles,
                "tp" : "ESOL"
            })
            headers = {
                'accept': 'application/json',
                'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
            rtn = {
                'result_code':'0000',
                'result_msg':'success'
            }
    except Exception as e :
        pass
        rtn = {
            'result_code':'9999',
            'result_msg':str(e)
        }

    return rtn


# def get3dpsaData(request) :

#     dataList = []
#     cnt = 0
#     list_search_ids = []
#     message = ""
#     search_history = []



#     returnVal = {"data":dataList, "recordsTotal":cnt, "recordsFiltered": cnt, "list_search_ids":list_search_ids, "message":message, "search_history":search_history}



def getEsolOrderMulti(posArr, dirArr) :
    columns = [
        'name', 'svg_img', 'status', 'result', 'mem_name', 'date_created', 'comment'
    ]
    returnOrder = ''
    i = 0
    for pos in posArr :
        if i != 0 :
            returnOrder += ", "

        if pos == '0' :
            returnOrder += 'name'
        elif pos == '1' :
            returnOrder += 'svg_img'
        elif pos == '2' :
            returnOrder += 'status'
        elif pos == '3' :
            returnOrder += 'result'
        elif pos == '4' :
            returnOrder += 'mem_name'
        elif pos == '5' :
            returnOrder += 'date_created'
        elif pos == '6' :
            returnOrder += 'comment'
        else :
            returnOrder += 'date_created'

        returnOrder += ' '+dirArr[i]
        i+=1

    return returnOrder




#############################################################################
################################ ESOL E #####################################
#############################################################################


#############################################################################
########################### Deep Solubility S ###############################
#############################################################################
def getDeepSolubilityDatas(request) :
    cur = connection.cursor()

    keyword = request.POST.get('keyword')
    smiles = request.POST.get('smile')

    start = request.POST.get('start')
    length = request.POST.get('length')
    orderArr = []
    orderDirArr = []
    for i in range(20) :
        order = request.POST.get('order['+str(i)+'][column]')
        if order != None :
            orderArr.append(order)
            orderDirArr.append(request.POST.get('order['+str(i)+'][dir]'))

    orderPos = getSolubilityOrderMulti(orderArr, orderDirArr)

    orderStr = " ORDER BY " + orderPos
    limitStr = " LIMIT " + length + " OFFSET " + start

    where = f"AND u.owner_id = {request.user.id} "
    if keyword != None and keyword != "" :
        where += f"AND u.name ilike '%{keyword}%' "
    
    cur.execute(f"select u.id as id, name, smiles, svg_img, status, result, date_created, comment, mem.mem_name \
                from utility_deep_solubility_info u \
                LEFT JOIN vw_member_info mem ON u.owner_id = mem.owner_id \
                WHERE NOT check_discard \
                {where} \
                {orderStr} \
                {limitStr} \
                ", )
    dataList = dictfetchall(cur)

    index = 0
    if smiles != None and smiles != '':
        dataList1 = []
        mol_block = request.POST.get('mol_block')
        mol = Chem.MolFromMolBlock(mol_block)
        normalSmiles = Chem.MolToSmiles(mol)
        mol = SaltRemover().StripMol(mol)
        strippedSmiles = Chem.MolToSmiles(mol)    

        smilesFromUser = request.POST.get('smile')
        searchType = request.POST.get('radio_search_type')
        minSimilarity = float(request.POST.get('minSimilarity'))
        maxSimilarity = float(request.POST.get('maxSimilarity'))

        molFromUser = Chem.MolFromSmiles(smilesFromUser)

        tq = rdTautomerQuery.TautomerQuery(molFromUser)

        for data in dataList :
            molFromDb = Chem.MolFromSmiles(data.get('smiles'))

            if searchType == 'substructure' and tq.IsSubstructOf(molFromDb):
                dataList1.append(data)
                index += 1
            elif searchType == 'identical' and is_same_mol(molFromUser, molFromDb):
                dataList1.append(data)
                index += 1
            elif searchType == 'similarity':
                fp_morgan_user = AllChem.GetMorganFingerprint(molFromUser, 2)
                fp_morgan_db = AllChem.GetMorganFingerprint(molFromDb, 2)
                realSimilarity = DataStructs.DiceSimilarity(fp_morgan_user, fp_morgan_db) * 100
                if (minSimilarity <= realSimilarity and realSimilarity <= maxSimilarity):
                    dataList1.append(data)
                    index += 1
        

    cur.execute(f"select count(id) as cnt \
                from utility_deep_solubility_info u \
                where not check_discard \
                {where} \
            ", )
    countResult = dictfetchall(cur)
    
    cnt = countResult[0].get('cnt')
    if smiles != None and smiles != '' :
        cnt = index
        dataList = dataList1
    list_search_ids = []
    message = ""
    search_history = []

    returnVal = {"data":dataList, "recordsTotal":cnt, "recordsFiltered": cnt, "list_search_ids":list_search_ids, "message":message, "search_history":search_history}
    if cur != None :
        cur.close()
    return returnVal

# def is_same_mol(mol1, mol2, useChirality=True):
#     return mol1.HasSubstructMatch(mol2, useChirality=useChirality) and mol2.HasSubstructMatch(mol1, useChirality=useChirality)

def setDeepSolubilityData(request) :
    url = "http://172.16.1.30:10009//api/calculate"

    mol_block = request.POST.get('mol_block')
    smiles = request.POST.get('smile')
    psa_name = request.POST.get("psa_name")
    comment = request.POST.get("comment")

    mol = Chem.MolFromMolBlock(mol_block)
    normalSmiles = Chem.MolToSmiles(mol)
    mol = SaltRemover().StripMol(mol)
    strippedSmiles = Chem.MolToSmiles(mol)

    solubility_predit = getSolubilityPreditApi(strippedSmiles)

    mol = get_scaled_mol(mol)
    svg_img = moltosvg(mol)    

    rtn = {}
    try :
        with transaction.atomic():
            data = {
                'owner_id':request.user.id,
                'name':psa_name,
                'smiles':strippedSmiles,
                'svg_img':svg_img,
                'mol_block':mol_block,
                'result':solubility_predit,
                'status':'Complete',
                'comment':comment,
                'check_discard':False,
                'date_created':datetime.datetime.now(),
                'date_updated':datetime.datetime.now()
            }

            deep_solubility = UtilityDeepSolubilityInfo.objects.create(**data)
            rtn = {
                'result_code':'0000',
                'result_msg':'success'
            }
    except Exception as e :
        pass
        rtn = {
            'result_code':'9999',
            'result_msg':str(e)
        }

    return rtn


def getSolubilityPreditApi(smiles) :
    hostname = socket.gethostname()
    if "VN-LeeSeunghwan" == hostname or "VN-JeongJaeheon" == hostname or "VORONOI-STAGE" == hostname or "VN-KimSeungchul" == hostname :
        url = "http://192.168.1.250:10006/api/solubility_predit"
    else :
        url = "http://172.16.1.237:10007/api/solubility_predit"

    solubility_predit = ""

    try:
        encode_smiles = parse.quote(smiles, safe='()', encoding="utf-8")
        payload = 'smiles='+encode_smiles
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        result = json.loads(response.text)
        #response = "{\"result\": \"5.55555\", \"result_code\":\"0000\"}"
        #result = json.loads(response)

        if result.get('result_code') == "0000" :
            solubility_predit = result.get('result')
            print('success getSolubilityPreditApi')
        else :
            print('error : ' + result.get('result'))

    except requests.exceptions.HTTPError as err:
        print('error : ' + str(err))

    return solubility_predit

# def get3dpsaData(request) :

#     dataList = []
#     cnt = 0
#     list_search_ids = []
#     message = ""
#     search_history = []



#     returnVal = {"data":dataList, "recordsTotal":cnt, "recordsFiltered": cnt, "list_search_ids":list_search_ids, "message":message, "search_history":search_history}

def getSolubilityOrderMulti(posArr, dirArr) :
    columns = [
        'name', 'svg_img', 'status', 'result', 'mem_name', 'date_created', 'comment'
    ]
    returnOrder = ''
    i = 0
    for pos in posArr :
        if i != 0 :
            returnOrder += ", "

        if pos == '0' :
            returnOrder += 'name'
        elif pos == '1' :
            returnOrder += 'svg_img'
        elif pos == '2' :
            returnOrder += 'status'
        elif pos == '3' :
            returnOrder += 'result'
        elif pos == '4' :
            returnOrder += 'mem_name'
        elif pos == '5' :
            returnOrder += 'date_created'
        elif pos == '6' :
            returnOrder += 'comment'
        else :
            returnOrder += 'date_created'

        returnOrder += ' '+dirArr[i]
        i+=1

    return returnOrder

#############################################################################
########################### Deep Solubility S ###############################
#############################################################################





def queryConv(queryArr) :
    listQuery = ''
    for queryStr in queryArr :
        listQuery += queryStr
    return listQuery

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]
