from django.db import connection

def singleton(class_):
    instances = {}

    def get_instance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return get_instance


@singleton
class Code:
    codes = []
    codeDtls = []
    codeAliasMap = {}
    codeDtlAliasMap = {}
    codeDtlMap = {}

    def __init__(self):
        self.codes = getCodes()
        for code in self.codes :
            self.codeAliasMap[code["cd_alias"]] = code

        self.codeDtls = getCodeDtls()
        for codeDtl in self.codeDtls :
            self.codeDtlAliasMap[codeDtl["cd_dtl_alias"]] = codeDtl
            self.codeDtlMap[codeDtl["cd_dtl_no"]] = codeDtl

    def getCodes(self) :
        return self.codes

    def getCodeDtls(self) :
        return self.codeDtls

    def getCodeDtlNoByAlias(self, alias):
        return self.codeDtlAliasMap[alias]["cd_dtl_no"]

    def getCodeDtlNm(self, cdDtlNo):
        return self.codeDtlMap[cdDtlNo]["cd_dtl_nm"]

def getCodes() :
    cur = connection.cursor()
    query = "SELECT * FROM code"
    print(query)
    cur.execute(query)
    result = dictfetchall(cur)
    if cur != None :
        cur.close()
    return result

def getCodeDtls() :
    cur = connection.cursor()
    query = "SELECT * FROM code_dtl"
    print(query)
    cur.execute(query)
    result = dictfetchall(cur)
    if cur != None :
        cur.close()
    return result

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

