from django.urls import path, include
from utilities.views import *

urlpatterns = [
    path('', utilities_home_view, name='utilities-home'),
    path('solubility', utilities_solubility_view, name='utilities-solubility-view'),
    path('solubility/api', utilities_solubility_api, name='utilities-solubility-api'),

    path('pka', utilities_pka_view, name='utilities-pka-view'),
    path('pka/api', utilities_pka_api, name='utilities-pka-api'),

    path('logd', utilities_logd_view, name='utilities-logd-view'),
    path('logd/api', utilities_logd_api, name='utilities-logd-api'),

    path('combination', utilities_combination_view, name='utilities-combination-view'),

    path('charge', utilities_charge_view, name='utilities-charge-view'),
    path('charge/api', utilities_charge_api, name='utilities-charge-api'),

    path('herg', utilities_herg_view, name='utilities-herg-view'),
    path('herg/api', utilities_herg_api, name='utilities-herg-api'),

    path('psa', utilities_psa_view, name='utilities-psa-view'),
    path('psa/api', utilities_psa_api, name='utilities-psa-api'),

    path('hbda', utilities_hbda_view, name='utilities-hbda-view'),
    path('hbda/api', utilities_hbda_api, name='utilities-hbda-api'),

    path('cns', utilities_cns_view, name='utilities-cns-view'),
    path('cns/api', utilities_cns_api, name='utilities-cns-api'),

    path('elemental', utilities_elemental_view, name='utilities-elemental-view'),
    path('elemental/api', utilities_elemental_api, name='utilities-elemental-api'),

    path('tautomer_domi', utilities_tautomer_domi_view, name='utilities-tautomer_domi-view'),
    path('tautomer_domi/api', utilities_tautomer_domi_api, name='utilities-tautomer_domi-api'),

    path('api/view', utilities_api_view, name='utilities-api-view'),
    path('api/create', utilities_api_create, name='utilities-api-create'),
    path('api', utilities_api, name='utilities-api'),
    path('api/update', utilities_api_update, name='utilities-api-update'),
    path('api/del', utilities_api_delete, name='utilities-api-delete'),
    path('api/get', utilities_get_api, name='utilities-api-get'),

    path('etc/view', utilities_etc_view, name='utilities-etc-view'),
    path('etc/operation', utilities_etc_operation, name='utilities-etc-operation'),
    path('etc/caco2', utilities_etc_caco2, name='utilities-etc-caco2'),
    path('etc/enzyme_lle', utilities_etc_enzyme_lle, name='utilities-etc-enzyme_lle'),
    path('etc/solubility', utilities_etc_solubility, name='utilities-etc-solubility'),


    path('cell-mutation', cell_mutation_view, name='utilities-cell-mutation'),
    path('cell-mutation/download-excel', cell_mutation_download, name='utilities-cell-mutation-download-excel'),

    path('cell-line-selector', cell_line_selector_view, name='utilities-cell-line-selector'),
    path('cell-line-selector/download-excel', cell_line_selector_download, name='utilities-cell-line-selector-download-excel'),

    # Deep learning solubility
    path('deep_learning_solubility', utilities_deep_learning_solubility_view, name='utilities-deep-learning-solubility-view'),
    path('deep_learning_solubility/getSolubilityPredit', get_solubility_predit, name='utilities-get-solubility-predit'),
    path('deep_learning_solubility/getSolubilityPreditFile', get_solubility_predit_file, name='utilities-get-solubility-predit-file'),

    # 3DPSA
    #path('3dpsa', utilities_3dpsa_view, name='utilities-3dpsa-view'),
    #path('3dpsa/search', utilities_3dpsa_search, name='utilities-3dpsa-search'),
    #path('3dpsa/register', utilities_3dpsa_register, name='utilities-3dpsa-register'),
    # 3DPSA
    path('3dpsa', utilities_3dpsa_view, name='utilities-3dpsa-view'),
    path('3dpsa/search', utilities_3dpsa_search, name='utilities-3dpsa-search'),
    path('3dpsa/register', utilities_3dpsa_register, name='utilities-3dpsa-register'),
    # ESOL
    path('esol', utilities_esol_view, name='utilities-esol-view'),
    path('esol/search', utilities_esol_search, name='utilities-esol-search'),
    path('esol/register', utilities_esol_register, name='utilities-esol-register'),
    # Deep solubility
    path('deep_solubility', utilities_deep_solubility_view, name='utilities-deep_solubility-view'),
    path('deep_solubility/search', utilities_deep_solubility_search, name='utilities-deep_solubility-search'),
    path('deep_solubility/register', utilities_deep_solubility_register, name='utilities-deep_solubility-register'),
]