import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
# from ai.mmpa_functions import ai_authority
# from ai.pdf2smiles_functions import pdf2smiles_authority
from hr.models import Authority
from hr.functions import initiate_authority_for_superuser
from home.functions import *
# from kpviewer.models import *
from member.models import *
# from program.models import *
# from dashboard.functions import *
# from compoundbank.new_functions import *


def get_authority_status(request, page_name) :
    q_authority = initiate_authority_for_superuser(request)
    q_authority = Authority.objects.filter(check_discard=False).last()

    page_array = page_name.split("/")
    if len(page_array) > 1 :
        page_name = page_array[0]
    print("page_name:" + page_name)
    if page_name == 'ai':
        # print("ai")
        if len(page_array) > 1 :
            # print("ai > "+page_array[1])
            if page_array[1] == "pdf2smiles" :
                return pdf2smiles_authority(request)
            else :
                return ai_authority(request)
        else :
            return ai_authority(request)
    elif page_name == 'dashboard':
        # print("dashboard")
        return dashboard_authority(request)
    elif page_name == 'compoundbank':
        # print("dashboard")
        return compound_authority(request)
    elif hasattr(q_authority, 'auth_' + page_name):
        # print("hasattr")
        auth_p = False
        auth_r = False
        auth_d = False
        auth_v = False
        try :
            # auth_p = q_authority.auth_kpviewer.index(request.user.member.id)
            auth_p = getattr(q_authority, 'auth_' + page_name).index(request.user.member.id)
            if auth_p >= 0 :
                auth_p = True
        except :
            pass
        try :
            # auth_r = q_authority.auth_kpviewer_register.index(request.user.member.id)
            auth_r = getattr(q_authority, 'auth_' + page_name + '_register').index(request.user.member.id)
            if auth_r >= 0 :
                auth_r = True
        except :
            pass
        try :
            # auth_v = q_authority.auth_kpviewer_validation.index(request.user.member.id)
            auth_v = getattr(q_authority, 'auth_' + page_name + '_validation').index(request.user.member.id)
            if auth_v >= 0 :
                auth_v = True
        except :
            pass
        try :
            # auth_d = q_authority.auth_kpviewer_design.index(request.user.member.id)
            auth_d = getattr(q_authority, 'auth_' + page_name + '_design').index(request.user.member.id)
            if auth_d >= 0 :
                auth_d = True
        except :
            pass

        if request.user.is_superuser :
            auth_p = True
            auth_r = True
            auth_d = True
            auth_v = True

        returnVal = {"P":auth_p, "R":auth_r, "D":auth_d, "V":auth_v}
    else:
        print("else")
        returnVal = {"P":False, "R":False, "D":False, "V":False}
    return returnVal

# def stem_tokens(tokens):
#     return [stemmer.stem(item) for item in tokens]

# '''remove punctuation, lowercase, stem'''
# def normalize(text):
#     return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

# def cosine_sim(text1, text2):
#     tfidf = vectorizer.fit_transform([text1, text2])
#     return ((tfidf * tfidf.T).A)[0,1]

# nltk.download('punkt') # if necessary...
# stemmer = nltk.stem.porter.PorterStemmer()
# remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
# vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')