from django.db import models

class ReTodo(models.Model) :
    # todo key
    todo_key = models.AutoField(db_column='todo_key', primary_key=True)
    # 회원 아이디
    member_id = models.IntegerField(db_column='member_id', blank=False, null=False, default=0)
    # todo 명
    todo_name = models.CharField(db_column='todo_name', max_length=100, blank=True, null=False)
    # todo 설명
    todo_desc = models.TextField(db_column='todo_desc', blank=True, null=True)
    # todo 일
    todo_date = models.CharField(db_column='todo_date', max_length=10, blank=True, null=True)
    # todo 우선순위
    todo_priority = models.IntegerField(db_column='todo_priority', blank=True, null=False, default=4)
    # 완료 여부
    check_done = models.BooleanField(db_column='check_done', default=False)
    # 삭제 여부
    check_discard = models.BooleanField(db_column='check_discard', default=False)
    # 생성일
    date_created = models.DateTimeField(db_column='date_created', blank=True, null=True, auto_now=False, auto_now_add=True)
    # 수정일
    date_updated = models.DateTimeField(db_column='date_updated', blank=True, null=True, auto_now=True, auto_now_add=False)

    class Meta:
        managed = True
        db_table = 're_todo'

