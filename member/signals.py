from .models import *
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import *


##########################################################
# 아래 문구를 apps.py config class에 추가하여야 한다.
#
# def ready(self):
#         import appname.signals
#
# User  DB먼저 등록 > 다른 DB 자동생성  >> 다른 DB 업데이트
###########################################################

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # User가 생성되면 자동으로 Profile이 생성되도록
        Member.objects.create(user=instance)
        # Profile.objects.create(user=instance)
        # Career.objects.create(user=instance)
        # Education.objects.create(user=instance)
        # Winner.objects.create(user=instance)
        # Vacation.objects.create(user=instance)
        # EducationInternalTreatment.objects.create(user=instance)
        # print('Profile, Career, Education, Winner, Vacation is Created! by Signal!!')


@receiver(post_save, sender=User)
def update_profile(sender, instance, created, **kwargs):
    if created == False:
        instance.member.save()
        # instance.profile.save()
        # instance.career.save()
        # instance.education.save()
        # instance.winner.save()
        # instance.vacation.save()
        # instance.educationinternaltreatment.save()


# @receiver(post_save, sender=Bid)
# def update_auction_totals_for_bid(sender, instance, created, **kwargs):
#     if created:
#         auction = instance.auction
#         auction.bid_count = Bid.BidManager.current(auction).count()
#         auction.current_bid = instance.value
#         auction.save()
