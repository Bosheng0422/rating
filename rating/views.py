from genericpath import exists
from django.http import HttpResponseBadRequest,HttpResponse
from rating.models import Module,Professor,Rate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
import json

# Create your views here.
def userregister(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'
    if(request.method != 'POST'):
        http_bad_response.content = 'Only POST requests are allowed for this resource\n'
        return http_bad_response
    data = json.loads(request.body)
    rusername = data['username']
    rpassword = data['password'] 
    remail = data['email']
    user = User.objects.filter(username=rusername)
    if user.exists() :
        http_bad_response.content = "username existed, register failed"
        return http_bad_response
    else:
        User.objects.create(username=rusername,password=make_password(rpassword),email=remail)
    httpresponse = HttpResponse()
    httpresponse['Content-Type'] = 'text/plain'
    httpresponse.content = "register successful"
    return httpresponse

def userlogin(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'
    data = json.loads(request.body)
    rusername= data['username']
    rpassword= data['password']
    user = User.objects.filter(username=rusername)
    if not user.exists() :
        http_bad_response.content = "Username is not existed, please register at first"
        return http_bad_response
    else:
        auth = authenticate(username=rusername,password=rpassword)
        if auth is not None:
            login(request,auth)
            httpresponse = HttpResponse()
            httpresponse['Content-Type'] = 'text/plain'
            httpresponse.content = "login successful"
            return httpresponse
        else:
            http_bad_response.content = "Password is incorrect"
            return http_bad_response

def userlogout(request):
    logout(request)
    httpresponse = HttpResponse()
    httpresponse['Content-Type'] = 'text/plain'
    httpresponse.content = "logout successful"
    return httpresponse


def show_module_list(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'

    if(request.method != 'GET'):
        http_bad_response.content = 'Only GET requests are allowed for this resource\n'
        return http_bad_response
    module_list = Module.objects.all()
    the_list = []
    for m in module_list:
        professors = Module.objects.get(code=m.code,name=m.name,year=m.year,semester=m.semester)
        p_list = []
        for p in professors.professor.all() :
            pitem=p.code+',Professor '+p.name
            p_list.append(pitem)
        item = {'code':m.code,'name':m.name,'year':m.year,'semester':m.semester,'professor':p_list}
        the_list.append(item)
    payload = {'module_list': the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application\json;charset=UTF-8'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response


def view(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'
    if(request.method != 'GET'):
        http_bad_response.content = 'Only GET requests are allowed for this resource\n'
        return http_bad_response
    professor_list = Professor.objects.all()
    the_list = []
    for p in professor_list.iterator():
        rates = Rate.objects.filter(professor = p)
        rate=0
        for r in rates.iterator():
            rate+=r.rate
        # the rate of professor with no rate record is 0
        # avoid devision by 0, set condition 
        if rates.count()>0:
            rate=round(rate/rates.count())
        item = {'professor':p.name+"("+p.code+")",'rate':rate}
        the_list.append(item)
    payload = {'professor_list': the_list}
    http_response = HttpResponse(json.dumps(payload))
    http_response['Content-Type'] = 'application\json;charset=UTF-8'
    http_response.status_code = 200
    http_response.reason_phrase = 'OK'
    return http_response


def average(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'
    data=json.loads(request.body)
    rprofessor=data['professor']
    rmodule=data['module']
    # code is unique
    professor=Professor.objects.get(code=rprofessor)
    module=Module.objects.filter(code=rmodule)
    rate=0
    rate_count=0
    for m in module:
        rates = Rate.objects.filter(professor=professor,module=m)
        if rates.count() ==0:
            http_bad_response.content='There is no rating for this professor in this module'
            return http_bad_response
        for r in rates.iterator():
            rate+=r.rate
            rate_count+=1
            # the rate of professor with no rate record is 0
            # avoid devision by 0, set condition 
    if rate_count>0:
        rate=round(rate/rate_count)
    re = "The rating of Professor "+professor.name+"("+professor.code+")"+"is "
    star = ""
    for i in range(rate):
        star=star+"*"
    http_response = HttpResponse()
    http_response['Content-Type'] = 'plain\text'
    http_response.content = re + star
    return http_response


def rate(request):
    http_bad_response = HttpResponseBadRequest()
    http_bad_response['Content-Type'] = 'text/plain'
    data=json.loads(request.body)
    pid=data['pid']
    mcode=data['mcode']
    year=data['year']
    semester=data['semester']
    rating=data['rating']
    user=data['user']
    rate_professor = Professor.objects.get(code=pid)
    rate_module = Module.objects.filter(code=mcode,year=year,semester=semester,professor=rate_professor)
    if not (rate_module.exists):
        http_bad_response.content("There is no specified module.")
        return http_bad_response
    r=Rate.objects.filter(professor=rate_professor.first(),module=rate_module.first(),fromw=user)
    if len(r)!=0:
        http_bad_response.content="You have rated, do not rate repeatedly."
        return http_bad_response
    else:
        Rate.objects.create(professor=rate_professor.first(),module=rate_module.first(),rate=rating,fromw=user)
        httpresponse = HttpResponse()
        httpresponse['Content-Type'] = 'text/plain'
        httpresponse.content = "Rate professor successfully"
        return httpresponse
