from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
import sqlite 

@api_view(['GET','POST'])
def add_problem(request):
    # sqlite.addAdmin(("Shakti","Shekhawat"))
    return JsonResponse(data={'msg':'add_data...'})



########  save user information if not already logged in

####### login user
@api_view(['GET','POST'])
def login(request):
    try:
        request.session['adminid']
        
    except KeyError:
        loginuser = request.data
        if loginuser:
            validdata = sqlite.uservalid(loginuser['username'])
        else:
            return render(request, 'login admin.html')
        if validdata:
            if validdata['password'] == loginuser['password']:
                request.session['adminid'] = validdata['id']
                request.session['fullname'] = validdata['fullname']
                request.session['adminemail'] = validdata['email']
                request.session['adminmobile'] = validdata['mobile']
                return redirect('/problems')
            return render(request, 'login admin.html',{'username':True, 'password':False, 'entereduser':validdata['username']})
        else:
            return render(request, 'login admin.html',{'username':False, 'password':True})
        
    else:
        return redirect('/problems')
       
        
@api_view(['GET','POST'])
def signup(request):
    print(request.data)
    try:
        request.session['adminid']
    except KeyError:
        if request.data:
            validdata = sqlite.uservalid(request.data['username'])
            if validdata:
                return render(request,'signup admin.html', {'username':True,'username':request.data['username'], 'fullname':request.data['fullname'], 'mobile':request.data['mobile'],'email':request.data['email']})
            new = sqlite.addAdmin((request.data['username'], request.data['password'],request.data['fullname'],request.data['mobile'], request.data['email'],))
            if new:
                return redirect('/login')
            return render(request, 'signup admin.html')
        return render(request, 'signup admin.html')
    return redirect('/problems')



@api_view(['GET','POST'])
def profileupdate(request):
    try:
        request.session['adminid']
    except KeyError:
        return redirect('/login')
    if request.data:
        update = sqlite.updateadmin(request.data, request.session['adminid'])
        print(">>>>>>>>",update)
        # request.session['adminid'] = update['id']
        request.session['fullname'] = update['fullname']
        request.session['adminemail'] = update['email']
        request.session['adminmobile'] = update['mobile']
        return redirect('/problems')
    return render(request, 'signup admin.html', {'update':True,'fullname':request.session['fullname'],'email':request.session['adminemail'],'mobile':request.session['adminmobile']})


@api_view(['GET','POST'])
def logout(request):
    del request.session['adminid']
    del request.session['fullname']
    del request.session['adminemail']
    del request.session['adminmobile']
    return render(request, 'login admin.html')


######   for render the form of add problem
@api_view(['GET','POST'])
def addProblem(request):
    companies = sqlite.getcompanies()
    data = []
    for company in companies:
        data.append(company[0])
    return render(request, 'problem form.html',{"company":data})

#######  add a problem 
@api_view(['GET','POST'])
def problemform(request):
    try:
        request.session['adminid']
    except KeyError:
        return redirect('/login')
    else:
        if request.data:
            userid = request.session['adminid']
            problem = request.data
            # print(problem)
            datatoadd = ( problem['title'], f"{problem['description']}", f"{problem['solution']}", problem['difficulty'], userid, problem['company'] )
            sqlite.addproblem(datatoadd)
            return redirect('/problems')
        else:
            companies = sqlite.getcompanies()
            data = []
            for company in companies:
                data.append(company[0])
            return render(request, 'problem form.html',{"company":data})


########    Add new Company
def setnewcompany(request,newcompany):
    sqlite.setcompany(newcompany)
    request.data = {}
    return redirect('/problemform')

########     Delete a single problem
def deleteproblem(request,id):
    sqlite.dropproblem(id)
    return redirect('/problems')

########    view a single problem
def viewproblem(request, id):
    # problem = sqlite.getoneproblem(id)
    cs = sqlite.getcompanies()
    companies = []
    for c in cs:
        companies.append(c[0])

    pr = sqlite.getoneproblem(id)
    print({"view":True,"id":pr[0],"title":pr[1],"description":pr[2],"solution":pr[3],"difficulty":pr[4],"com":pr[6],"company":companies})
    return render(request,'problem form.html',{"view":True,"id":pr[0],"title":pr[1],"description":pr[2],"solution":pr[3],"difficulty":pr[4],"ownerid":pr[5],"adminid":request.session['adminid'],"com":pr[6],"company":companies,})
    
########   Personal Problems
def personal(request):
    try:
        request.session['adminid']
    except KeyError:
        return redirect('/login')
    data = sqlite.getpersonal(request.session['adminid'])
    jsondata = []
    index = 1
    for item in data:
        jsondata.append({'index':index,'id':item[0], 'title':item[1],'solution':item[3],'difficulty':item[4],'ownerid':int(item[5]),'adminid':int(request.session['adminid'])})
        index+=1
    
    return render(request, 'problems.html',{'problems':jsondata, 'fullname':request.session['fullname'], 'email':request.session['adminemail'], 'mobile':request.session['adminmobile'], 'personal':True})



########  get all problems if user is logged in
@api_view(['GET','POST'])
def problems(request): 
    try:
        request.session['adminid']
    except KeyError:
        return redirect('/login')

    data = sqlite.getproblems()
    # print(data) 
    jsondata = []
    index = 1
    print(data)
    for item in data:
        jsondata.append({'index':index,'id':item[0], 'title':item[1],'solution':item[3],'difficulty':item[4],'ownerid':int(item[5]),'adminid':int(request.session['adminid'])})
        index+=1
    
    return render(request, 'problems.html',{'problems':jsondata, 'fullname':request.session['fullname'], 'email':request.session['adminemail'], 'mobile':request.session['adminmobile']})

########   search  problems according title
@api_view(['GET','POST'])
def searchproblem(request,search):
    data = sqlite.search(search)
    jsondata = []
    index = 1

    for item in data:
        jsondata.append({'index':index,'id':item[0], 'title':item[1],'solution':item[3],'difficulty':item[4],'ownerid':int(item[5]),'adminid':int(request.session['adminid'])})
        index+=1
    return render(request, 'problems.html',{'problems':jsondata,'search':True, 'searchvalue':search, 'fullname':request.session['fullname'], 'email':request.session['adminemail'], 'mobile':request.session['adminmobile']})



########  sort problems according there difficulity
@api_view(['GET','POST'])
def sorting(request,sort):
    
    data = sqlite.getproblems()
    tempdata = []
    index = 1
    for item in data:
        tempdata.append({'index':index,'id':item[0], 'title':item[1],'solution':item[3],'difficulty':item[4],'ownerid':int(item[5]),'adminid':int(request.session['adminid'])})
        index+=1

    jsondata = []
    def diffs(problem):
        # data = ['easy','medium','hard']
        if sort in problem['difficulty']:
            jsondata.append(problem)
        
    def additionals(problem):
        if sort not in problem['difficulty']:
            jsondata.append(problem)
        
    for problem in tempdata:
        diffs(problem)

    for problem in tempdata:
        additionals(problem)

    index = 1
    for problem in jsondata:
        problem.update({'index':index})
        index+=1
    return render(request, 'problems.html',{'problems':jsondata, 'sorted':sort, 'fullname':request.session['fullname'], 'email':request.session['adminemail'], 'mobile':request.session['adminmobile']})
    

@api_view(['GET','POST'])
def problemupdate(request, id):
    try:
        request.session['adminid']
    except KeyError:
        return redirect('/login')
    else:
        if request.data:
            userid = request.session['adminid']
            problem = request.data
            # print(problem)
            datatoupdate = ( problem['title'], f"{problem['description']}", f"{problem['solution']}", problem['difficulty'], problem['company'] )
            sqlite.updateproblem(datatoupdate,id)
            return redirect('/problems')
        else:
            companies = sqlite.getcompanies()
            data = []
            for company in companies:
                data.append(company[0])
            return render(request, 'problem form.html',{"company":data})
