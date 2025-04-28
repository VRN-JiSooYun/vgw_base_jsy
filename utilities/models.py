from django.db import models
from django.dispatch import receiver
# Create your models here.

class ChemaxonVersion(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'utility_api_version'

class SolubilityHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    unit = models.CharField(db_column='unit', max_length=12, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_solubility_history'

class PkaHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_pka_history'

class PkaDistributionHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_pka_distribution_history'


class LogdHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_logd_history'

class LogpHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_logp_history'

class ChargeHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    ph = models.FloatField(db_column='ph', blank=True, null=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_charge_history'

class HergActivityHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_herg_activity_history'

class HergClassHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_herg_class_history'

class PolaSurfaceAreaHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    ph = models.FloatField(db_column='ph', blank=True, null=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_psa_history'

class HbondDonorHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    ph = models.FloatField(db_column='ph', blank=True, null=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_hbda_history'

class ElementalAnalysisHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    operations = models.CharField(db_column='operations', max_length=256, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_elemental_history'

class CnsMpoHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_cns_history'

class TautomerizationDominantHistory(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    req_id = models.IntegerField(db_column='req_id', blank=False, null=False, default=0)
    class Meta :
        managed = True
        db_table = 'utility_tautomer_dominant_history'



class CalculatorApiToken(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    name = models.CharField(db_column='name', max_length=255, null=True, blank=True)
    token = models.CharField(db_column='token', max_length=255, null=True, blank=True)
    status = models.CharField(db_column='status', max_length=24, null=True, blank=True)
    owner_name = models.CharField(db_column='owner_name', max_length=24, null=True, blank=True)
    owner_id = models.IntegerField(db_column='owner_id', null=True, blank=True)
    comment = models.TextField(db_column="comment", null=True, blank=True)
    limit_count = models.IntegerField(db_column='limit_count', null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'utility_api_token'

class CalculatorApiStatus(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    api_id = models.IntegerField(db_column='api_id', null=True, blank=True)
    smiles = models.CharField(db_column='smiles', max_length=1024, null=True, blank=True)
    api_type = models.CharField(db_column='api_type', max_length=64, null=True, blank=True)
    api_version = models.CharField(db_column='api_version', max_length=10, null=True, blank=True)
    request_data = models.JSONField(db_column='request_data',blank=True, null=True)
    response_data = models.JSONField(db_column='response_data',blank=True, null=True)
    owner_id = models.IntegerField(db_column='owner_id', null=True, blank=True)
    comment = models.TextField(db_column="comment", null=True, blank=True)
    ip_addr = models.CharField(db_column='ip_addr', max_length=32, null=True, blank=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'utility_api_status'



######################################################
################### CELL MUTATION ####################
######################################################
class CellMutationInfo(models.Model) :
    cell_name = models.CharField(db_column='cell_name', max_length=128, primary_key=True)
    lineage = models.CharField(db_column='lineage', max_length=64, blank=True, null=True)
    subtype = models.CharField(db_column='subtype', max_length=128, blank=True, null=True)
    mutation_data = models.BooleanField(db_column='mutation_data', default=False)
    cn_data = models.BooleanField(db_column='cn_data', default=False)
    fusion_gene = models.BooleanField(db_column='fusion_gene', default=False)
    in_house = models.BooleanField(db_column='in_house', default=False)
    file_name = models.CharField(db_column='file_name', max_length=256, blank=True, null=True )
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'cell_mutation_info'

class CellMutation(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    cell_name = models.CharField(db_column='cell_name', max_length=128, blank=False, null=False)
    protein_change = models.CharField(db_column='protein_change', max_length=256, blank=False, null=False, default='')
    gene = models.CharField(db_column='gene', max_length=64, blank=False, null=False)
    chrom = models.CharField(db_column='chrom', max_length=12, blank=True, null=True)
    start_pos = models.CharField(db_column='start_pos', max_length=128, blank=True, null=True)
    end_pos = models.CharField(db_column='end_pos', max_length=128, blank=True, null=True)
    reference_allele = models.CharField(db_column='reference_allele', max_length=512, blank=True, null=True)
    tumor_seq_allele1 = models.CharField(db_column='tumor_seq_allele1', max_length=512, blank=True, null=True)
    tumor_seq_allele2 = models.CharField(db_column='tumor_seq_allele2', max_length=512, blank=True, null=True)
    variant_info = models.CharField(db_column='variant_info', max_length=32, blank=True, null=True)
    variant_classification = models.CharField(db_column='variant_classification', max_length=128, blank=True, null=True)
    mutation_effect = models.CharField(db_column='mutation_effect', max_length=128, blank=True, null=True)
    oncogenic = models.CharField(db_column='oncogenic', max_length=128, blank=True, null=True)
    source = models.CharField(db_column='source', max_length=32, default=False)
    file_name = models.CharField(db_column='file_name', max_length=256, blank=True, null=True )

    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'cell_mutation'
        constraints = [
            models.UniqueConstraint(
                fields = ["cell_name", "protein_change", "gene", "chrom", "start_pos", "end_pos", "reference_allele", "tumor_seq_allele1", "tumor_seq_allele2"],
                name = "cell_mutation_uniquekey",
            ),
        ]

class CellMutationHRD(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    cell_name = models.CharField(db_column='cell_name', max_length=128, blank=False, null=False)

    loh_score = models.FloatField(db_column='loh_score', blank=True, null=True)
    tai_score = models.FloatField(db_column='tai_score', blank=True, null=True)
    lst_score = models.FloatField(db_column='lst_score', blank=True, null=True)
    hrd_score = models.FloatField(db_column='hrd_score', blank=True, null=True)
    file_name = models.CharField(db_column='file_name', max_length=256, blank=True, null=True )

    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'cell_mutation_hrd'
        constraints = [
            models.UniqueConstraint(
                fields = ["cell_name"],
                name = "cell_mutation_hrd_uniquekey",
            ),
        ]


class CellMutationMSI(models.Model) :
    id = models.BigAutoField(db_column='id', primary_key=True)
    cell_name = models.CharField(db_column='cell_name', max_length=128, blank=False, null=False)

    gdsc_msi = models.CharField(db_column='gdsc_msi', max_length=256, blank=True, null=True)
    ccle_msi = models.CharField(db_column='ccle_msi', max_length=256, blank=True, null=True)
    file_name = models.CharField(db_column='file_name', max_length=256, blank=True, null=True )

    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'cell_mutation_msi'
        constraints = [
            models.UniqueConstraint(
                fields = ["cell_name"],
                name = "cell_mutation_msi_uniquekey",
            ),
        ]


###########################################################
################### CELL LINE SELECTOR ####################
###########################################################
class CellLineSelectorCellDepmapAllGene(models.Model) :
    gene = models.CharField(db_column='cell_name', max_length=64, blank=True, null=True)
    
    class Meta :
        managed = True
        db_table = 'cell_line_selector_cell_depmap_all_gene'

class CellLineSelectorCellMappingId(models.Model) :
    cell_name = models.CharField(db_column='cell_name', max_length=64, blank=True, null=True)
    model_id = models.CharField(db_column='model_id', max_length=24, blank=True, null=True)
    
    class Meta :
        managed = True
        db_table = 'cell_line_selector_cell_mapping_id'

class CellLineSelectorGeneCount(models.Model) :
    structure = models.CharField(db_column='structure', max_length=6, blank=True, null=True) # normal, tree
    category = models.CharField(db_column='category', max_length=512, blank=True, null=True)
    node = models.TextField(db_column='node', blank=True, null=True)
    num_children = models.IntegerField(db_column='num_children', blank=True, null=True)
    gene_list = models.JSONField(db_column='gene_list', null=True, blank=True)

    class Meta :
        managed = True
        db_table = 'cell_line_selector_gene_count'

class CellLineSelectorGeneNormalStructure(models.Model) :
    category = models.CharField(db_column='category', max_length=512, blank=True, null=True)
    set = models.TextField(db_column='set', blank=True, null=True)
    gene = models.CharField(db_column='gene', max_length=128, blank=True, null=True)

    check_display = models.BooleanField(db_column='check_display', default=False)

    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'cell_line_selector_gene_normal_structure'

class CellLineSelectorGeneTreeStructure(models.Model) :

    category = models.CharField(db_column='category', max_length=512, blank=True, null=True)

    code = models.CharField(db_column='code', max_length=12, primary_key=True) # GO:0000001
    name = models.CharField(db_column='name', max_length=256, blank=True, null=True)
    namespace = models.CharField(db_column='namespace', max_length=64, blank=True, null=True)

    level = models.IntegerField(db_column='level', blank=False, null=False, default=0)
    parents = models.JSONField(db_column='parents', null=True, blank=True) # ['GO:0000001', 'GO:0000002']
    children = models.JSONField(db_column='children', null=True, blank=True) # ['GO:0000004', 'GO:0000005']

    definition = models.TextField(db_column='definition', null=True, blank=True)

    genes = models.JSONField(db_column='genes', null=True, blank=True)
    gene_symbols = models.JSONField(db_column='gene_symbols', null=True, blank=True)

    check_display = models.BooleanField(db_column='check_display', default=False)

    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'cell_line_selector_gene_tree_structure'

class CellLineSelectorInfo(models.Model) :

    title = models.TextField(db_column='title', blank=True, null=True)

    gene_set_list = models.JSONField(db_column='gene_set_list', null=True, blank=True)

    target = models.CharField(db_column='target', max_length=100, blank=True, null=True)
    dep_or_eff = models.CharField(db_column='dep_or_eff', max_length=12, blank=True, null=True) # Dependency/Effect

    dependency = models.BooleanField(db_column='dependency', blank=True, null=True, default=True)
    effect = models.BooleanField(db_column='effect', blank=True, null=True, default=False)

    left = models.FloatField(db_column='left', null=True, blank=True)
    right = models.FloatField(db_column='right', null=True, blank=True)

    is_best_combo = models.BooleanField(db_column='is_best_combo', blank=True, null=True, default=False)

    feature_ranks = models.JSONField(db_column='feature_ranks', null=True, blank=True)
    default_img = models.TextField(db_column='default_img', null=True, blank=True) # default background image for section2

    histogram_data = models.JSONField(db_column='histogram_data', null=True, blank=True) # section1
    scatter_group0_data = models.JSONField(db_column='scatter_group0_data', null=True, blank=True) # section2 blue
    scatter_group1_data = models.JSONField(db_column='scatter_group1_data', null=True, blank=True) # section2 red
    cell_data = models.JSONField(db_column='cell_data', null=True, blank=True) # section3
    marker_data = models.JSONField(db_column='marker_data', null=True, blank=True) # section4

    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta :
        managed = True
        db_table = 'cell_line_selector_info'

class CellLineSelectorScatterData(models.Model) :

    info_id = models.IntegerField(db_column='info_id', blank=True, null=True, default=0)

    title = models.TextField(db_column='title', blank=True, null=True)
    group_no = models.CharField(db_column='group_no', max_length=2, blank=True, null=True)

    rank_no = models.IntegerField(db_column='rank_no', blank=True, null=True, default=0)

    scatter_data = models.JSONField(db_column='scatter_data', null=True, blank=True)

    class Meta :
        managed = True
        db_table = 'cell_line_selector_scatter_data'

class CellLineSelectorChatGptThread(models.Model) :
    title = models.CharField(db_column='title', max_length=120, blank=True, null=False)

    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)

    check_discard = models.BooleanField(db_column='check_discard', default=False)

    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 'cell_line_selector_chatgpt_thread'

class CellLineSelectorChatGptMessage(models.Model) :

    thread_id = models.IntegerField(db_column='thread_id', blank=False, null=False, default=0)

    # system, user, assistant
    role = models.CharField(db_column='role', max_length=20, blank=True, null=False) 
    content = models.TextField(db_column='content', blank=True, null=True)

    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)

    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 'cell_line_selector_chatgpt_message'

class CellLineSelectorTracking(models.Model) :

    action_type = models.CharField(db_column='action_type', max_length=56, blank=True, null=True) 

    search_title = models.TextField(db_column='search_title', blank=True, null=True)
    search_content = models.JSONField(db_column='search_content', blank=True, null=True)

    owner_id = models.IntegerField(db_column='owner_id', blank=True, null=True)

    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 'cell_line_selector_tracking'



#################################################################################################################
############################################### Safety Panel ####################################################
#################################################################################################################
class SafetyPanelData(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    order_id = models.CharField(db_column='order_id', max_length=20, blank=False, null=False)
    sp_compound_name = models.CharField(db_column='sp_compound_name', max_length=64, blank=True, null=True)
    compound_code = models.CharField(db_column='compound_code', max_length=9, null=True, blank=True)
    batch_no = models.CharField(db_column='batch_no', max_length=25, null=True, blank=True)
    target_class = models.CharField(db_column='target_class', max_length=24, blank=True, null=True)
    assay_name = models.CharField(db_column='assay_name', max_length=64, blank=True, null=True)
    assay_target = models.CharField(db_column='assay_target', max_length=24, blank=True, null=True)
    mode = models.CharField(db_column='mode', max_length=16, blank=True, null=True)
    result_type = models.CharField(db_column='result_type', max_length=10, blank=True, null=True)
    value_prefix = models.CharField(db_column='value_prefix', max_length=5, blank=True, null=True)
    rc50 = models.FloatField(db_column='rc50', blank=True, null=True)
    hill = models.FloatField(db_column='hill', blank=True, null=True)
    curve_bottom = models.FloatField(db_column='curve_bottom', blank=True, null=True)
    curve_top = models.FloatField(db_column='curve_top', blank=True, null=True)
    max_response = models.FloatField(db_column='max_response', blank=True, null=True)
    check_reference = models.BooleanField(db_column='check_reference', default=False)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'safety_panel_data'

class SafetyPanelGene(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    assay_target = models.CharField(db_column='assay_target', max_length=24, blank=True, null=True)
    target = models.CharField(db_column='target', max_length=24, blank=True, null=True)
    gene_id = models.IntegerField(db_column='gene_id', blank=False, null=False, default=0)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'safety_panel_gene'

class SafetyPanelRaw(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    order_id = models.CharField(db_column='order_id', max_length=20, blank=False, null=False)
    sp_compound_name = models.CharField(db_column='sp_compound_name', max_length=64, blank=True, null=True)
    compound_code = models.CharField(db_column='compound_code', max_length=9, null=True, blank=True)
    batch_no = models.CharField(db_column='batch_no', max_length=25, null=True, blank=True)
    target_class = models.CharField(db_column='target_class', max_length=24, blank=True, null=True)
    assay_name = models.CharField(db_column='assay_name', max_length=64, blank=True, null=True)
    gene_symbol = models.CharField(db_column='gene_symbol', max_length=24, blank=True, null=True)
    mode = models.CharField(db_column='mode', max_length=16, blank=True, null=True)
    result_type = models.CharField(db_column='result_type', max_length=10, blank=True, null=True)
    concentration = models.FloatField(db_column='concentration', blank=True, null=True)
    percent_response = models.FloatField(db_column='percent_response', blank=True, null=True)
    replicate_id = models.IntegerField(db_column='replicate_id', blank=False, null=False, default=0)
    is_invalid = models.BooleanField(db_column='is_invalid', default=False)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'safety_panel_raw'


#################################################################################################################
###############################################     3DPSA     ###################################################
#################################################################################################################
class Utility3DPSAInfo(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)
    name = models.CharField(db_column='name', max_length=24, blank=False, null=False)
    smiles = models.CharField(db_column='smiles', max_length=1000, blank=False, null=False)
    svg_img = models.TextField(db_column='svg_img',blank=True, null=True)
    mol_block = models.TextField(db_column='mol_block',blank=True, null=True)
    status = models.CharField(db_column='status', max_length=24, blank=False, null=False)
    result = models.FloatField(db_column='result', blank=True, null=True)
    comment = models.TextField(db_column='comment',blank=True, null=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'utility_3dpsa_info'

class Utility3DPSAFavorite(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    _3dpsa_id = models.IntegerField(db_column='_3dpsa_id', blank=False, null=False, default=0)
    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'utility_3dpsa_favorite'


#################################################################################################################
###############################################     ESOL     ###################################################
#################################################################################################################
class UtilityEsolInfo(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)
    name = models.CharField(db_column='name', max_length=24, blank=False, null=False)
    smiles = models.CharField(db_column='smiles', max_length=1000, blank=False, null=False)
    svg_img = models.TextField(db_column='svg_img',blank=True, null=True)
    mol_block = models.TextField(db_column='mol_block',blank=True, null=True)
    status = models.CharField(db_column='status', max_length=24, blank=False, null=False)
    result = models.FloatField(db_column='result', blank=True, null=True)
    comment = models.TextField(db_column='comment',blank=True, null=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'utility_esol_info'

class UtilityEsolFavorite(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    esol_id = models.IntegerField(db_column='esol_id', blank=False, null=False, default=0)
    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'utility_esol_favorite'


#################################################################################################################
##########################################     Deel Solubility     ##############################################
#################################################################################################################
class UtilityDeepSolubilityInfo(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)
    name = models.CharField(db_column='name', max_length=24, blank=False, null=False)
    smiles = models.CharField(db_column='smiles', max_length=1000, blank=False, null=False)
    svg_img = models.TextField(db_column='svg_img',blank=True, null=True)
    mol_block = models.TextField(db_column='mol_block',blank=True, null=True)
    status = models.CharField(db_column='status', max_length=24, blank=False, null=False)
    result = models.FloatField(db_column='result', blank=True, null=True)
    comment = models.TextField(db_column='comment',blank=True, null=True)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'utility_deep_solubility_info'

class UtilityDeepSolubilityFavorite(models.Model) :
    id = models.BigAutoField(db_column='id', blank=False, null=False, primary_key=True)
    deep_solubility_id = models.IntegerField(db_column='deep_solubility_id', blank=False, null=False, default=0)
    owner_id = models.IntegerField(db_column='owner_id', blank=False, null=False, default=0)
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)
    class Meta :
        managed = True
        db_table = 'utility_deep_solubility_favorite'
