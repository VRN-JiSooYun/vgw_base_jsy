from email.policy import default
from django.db import models

# Create your models here.
# from compound.models import SARDesign
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.json import JSONField
# from ip.models import PatentPublic
# from compoundbank.models import *
from member.models import *
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
import datetime

INQUIRY_TYPES = (
    ('qna', 'qna'),
    ('faq', 'faq'),
)

######################################################################################################################################################
# Inquiry Models
######################################################################################################################################################
class inquiry_page(models.Model):
    page_name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return str(self.page_name) + " (" + str(self.id) + ")"

class inquiry_category(models.Model):
    page = models.ForeignKey(inquiry_page, on_delete=models.CASCADE, null=True, blank=True)
    category = models.CharField(max_length=240, null=True, blank=True)

    # class Meta:
    #     unique_together = ("page_name", "category")
    def __str__(self):
        return "(app:" + str(self.page) + ") - [category:" + str(self.category) + "] (" + str(self.id) + ")"

def get_time():
    return str(datetime.datetime.now().strftime(("%Y.%m.%d<br>%H:%M:%S")))

class inquiry_post(models.Model):
    page = models.ForeignKey(inquiry_page, on_delete=models.CASCADE, null=True, blank=True)
    category = models.ForeignKey(inquiry_category, on_delete=models.CASCADE, null=True, blank=True)
    inquiry_type = models.CharField(max_length=50, choices=INQUIRY_TYPES, default="qna", null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=240, null=True, blank=True)
    title_en = models.CharField(max_length=240, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    
    create_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    modify_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    check_comment = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        page_name = inquiry_page.objects.get(id=self.page_id).page_name
        return "(" + str(self.id) + ") [" + page_name + "] " + self.title

class inquiry_post_comment(models.Model):
    post = models.ForeignKey(inquiry_post, on_delete=models.CASCADE, null=True, blank=True)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    parent_reply_id = models.IntegerField(null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    create_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    modify_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    is_reply = models.BooleanField(default=False, null=True, blank=True)
    check_best_comment = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "(" + str(self.id) + ") " + self.content

class inquiry_how_to(models.Model):
    inquiry_page = models.ForeignKey(inquiry_page, on_delete=models.CASCADE, null=True, blank=True)
    parent_how_to = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    order_value = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        page_name = inquiry_page.objects.get(id=self.inquiry_page_id).page_name
        return "(" + str(self.id) + ") [" + page_name + "] " + self.title

#####################################################################################################
# Blind Models
#####################################################################################################

class blind_category(models.Model):
    category = models.CharField(max_length=240, null=True, blank=True)

    # class Meta:
    #     unique_together = ("page_name", "category")
    def __str__(self):
        return str(self.category)

class blind_post(models.Model):
    category = models.ForeignKey(inquiry_category, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=240, null=True, blank=True)
    content = models.TextField(null=True, blank=True)

    check_hide = models.IntegerField(default=0, null=True, blank=True)
    password = models.CharField(max_length=10, null=True, blank=True)
    
    create_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    modify_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    check_comment = models.BooleanField(default=False, null=True, blank=True)
    check_discard = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "(" + str(self.id) + ") " + self.title

class blind_post_comment(models.Model):
    post = models.ForeignKey(blind_post, on_delete=models.CASCADE, null=True, blank=True)
    parent_comment = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)
    parent_reply_id = models.IntegerField(null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    create_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    modify_date = models.CharField(max_length=50, null=True, blank=True, default=get_time)
    is_reply = models.BooleanField(default=False, null=True, blank=True)
    check_best_comment = models.BooleanField(default=False, null=True, blank=True)
    check_anonymity = models.IntegerField(default=0, null=True, blank=True)
    check_discard = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return "(" + str(self.id) + ") " + self.content