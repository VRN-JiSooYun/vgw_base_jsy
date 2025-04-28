from django.db import models

import json

class TreeNode() :
    def __init__(self, id, text) :
        self.id = id
        self.text = text
        self.children = []

    def id(self) :
        return self.id

    def name(self) :
        return self.name

    def children(self) :
        return self.children

    def addChildren(self, node) :
        self.children.append(node)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=False, indent=4, ensure_ascii=False)

class ReGroup(models.Model) :
    # 그룹키
    group_key = models.AutoField(db_column='group_key', primary_key=True)
    # 그룹명
    group_name = models.CharField(db_column='group_name', max_length=100, blank=False, null=False)
    # 그룹 부모 키
    parent_group_key = models.IntegerField(db_column='parent_group_key', blank=False, null=False, default=-1)
    # 그룹 종속 깊이
    group_depth = models.IntegerField(db_column='group_depth', blank=False, null=False, default=-1)
    # 그룹 타입
    group_type = models.CharField(db_column='group_type', max_length=6, blank=True, null=False)
    # 그룹 코드
    group_code = models.CharField(db_column='group_code', max_length=10, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_group'


class ReGroupMember(models.Model) :
    # 그룹 회원 키
    group_member_key = models.AutoField(db_column='group_member_key', primary_key=True)
    # 그룹 키
    group_key = models.IntegerField(db_column='group_key', blank=False, null=False)
    # 회원 키
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False)
    # 리더 여부
    is_leader = models.CharField(db_column='is_leader', blank=False, null=False, max_length=1, default="N")
    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_group_member'

class ReGroupHistory(models.Model) :
    # 그룹 히스토리 키
    group_history_key = models.CharField(db_column='group_history_key', max_length=20, blank=False, null=False)
    # 그룹키
    group_key = models.IntegerField(db_column='group_key', blank=False, null=False)
    # 그룹명
    group_name = models.CharField(db_column='group_name', max_length=100, blank=False, null=False)
    # 그룹 부모 키
    parent_group_key = models.IntegerField(db_column='parent_group_key', blank=False, null=False, default=-1)
    # 그룹 종속 깊이
    group_depth = models.IntegerField(db_column='group_depth', blank=False, null=False, default=-1)
    # 그룹 타입
    group_type = models.CharField(db_column='group_type', max_length=6, blank=True, null=False)
    # 그룹 코드
    group_code = models.CharField(db_column='group_code', max_length=10, blank=True, null=False)

    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)

    class Meta:
        managed = True
        db_table = 're_group_history'
