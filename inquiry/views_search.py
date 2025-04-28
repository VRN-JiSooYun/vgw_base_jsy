import datetime
import sys
import json
import base64
import itertools
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q, Count, F, Value
from django.views.generic import *
# from program.models import *
from django.apps import apps
from io import BytesIO
from rdkit import Chem
from rdkit.Chem import Draw, Descriptors, AllChem, rdDepictor, MolsFromPNGString
from rdkit.Chem.Draw import MolsToImage, MolsToGridImage, MolToFile, rdMolDraw2D, MolToImageFile
from django.db import connection
from django.core import serializers
from member.models import *
from django.db.models import F
from .models import *
from datetime import datetime
