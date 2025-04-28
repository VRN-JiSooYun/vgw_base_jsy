from re_group.functions import *
from re_auth.models import *
from re_todo.models import *
from django.db import connection
from django.forms.models import model_to_dict
from django.conf import settings
from django.db.models import Q
from datetime import date, timedelta

def createTodo(request) :
    data = json.loads(request.body.decode('utf-8'))
    todo = data["todo"]
    try :
        reTodo = ReTodo(
            member_id = request.user.id,
            todo_name = todo["todo_name"],
            todo_desc = todo["todo_desc"],
            todo_date = todo["todo_date"],
            todo_priority = todo["todo_priority"],
        )
        reTodo.save()
        print("success create todo")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def getTodayTodos(memberId) :
    today = datetime.today().strftime("%Y-%m-%d")
    return ReTodo.objects.filter(Q(member_id = memberId) & Q(todo_date = today) & Q(check_discard = False)).order_by('todo_priority', 'todo_date').all()

def getTodos(request) :
    data = json.loads(request.body)["data"]
    memberIds = data["member_ids"]
    todoDate = data["todo_date"]

    memberIdsStr = ""
    for memberId in memberIds :
        if memberIdsStr == "" :
            memberIdsStr = memberId
        else :
            memberIdsStr += "," + memberId

    cur = connection.cursor()
    query = queryConv(settings.QUERY_INFO_LSH.re_todo.get_todos)
    query = query.replace('__TODO_DATE__', todoDate).replace('__MEMBER_IDS__', str(memberIdsStr))

    print(query)
    cur.execute(query)

    todos = dictfetchall(cur)
    if cur != None :
        cur.close()

    return todos

def getTodo(todoKey) :
    return ReTodo.objects.get(todo_key=todoKey)

def updateTodo(request, todoKey) :
    data = json.loads(request.body)["data"]
    try :
        reTodo = ReTodo.objects.get(todo_key = todoKey)
        reTodo.todo_name = data["todo_name"]
        reTodo.todo_desc = data["todo_desc"]
        reTodo.todo_date = data["todo_date"]
        reTodo.todo_priority = data["todo_priority"]

        ReTodo.save(reTodo)
        print("success update todo")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def updateCheckDone(request, todoKey) :
    check_done = json.loads(request.body)["check_done"]
    try :
        reTodo = ReTodo.objects.get(todo_key = todoKey)
        reTodo.check_done = check_done
        ReTodo.save(reTodo)
        print("success update check done")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

def deleteTodo(todoKey) :
    try :
        reTodo = ReTodo.objects.get(todo_key = todoKey)
        reTodo.check_discard = True
        ReTodo.save(reTodo)
        print("success delete todo")
    except Exception as e :
        print("Exception::", e)
        return False, e

    return True, "success"

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