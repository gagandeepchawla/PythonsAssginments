from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from sqlalchemy.exc import DBAPIError
from pyramid.renderers import render_to_response

from ..models import User
from ..models import FriendList
from ..models import FriendBlogs
from pyramid.security import forget
from pyramid.security import forget
@view_config(route_name = 'login',renderer = '../templates/login.jinja2')
def login(request):
    return{}

@view_config(route_name = 'addnewuser',renderer = '../templates/addnewuser.jinja2')
def addnewuser(request):
    return{}

@view_config(route_name = 'checkuser',request_method = 'POST' )
def checkuser(request):
    session = request.session
    username = request.params['form-username']
    password = request.params['form-password']
    cradentials = request.dbsession.query(User).filter_by(username = username).first()
    if cradentials.username == username  and cradentials.password == password:
        session['username_name'] = cradentials.username
        return HTTPFound(location = request.route_url('home'))
       
    else:
        return HTTPFound(location = request.route_url('login'))





@view_config(route_name = 'home',renderer = '../templates/home.jinja2')
def home(request):
    session = request.session
    username = session['username_name']
    cradentials = request.dbsession.query(User).filter_by(username = username).first()
    if username != '':
        username = session['username_name']
        cradentials = request.dbsession.query(User).filter_by(username = username).first()
        myid = cradentials.id
        selectname = ''
        alluser = request.dbsession.query(User).all()
        filteruser,friends,select = [],[],[]
        query = request.dbsession.query(FriendList,User.username).join(User, User.id==FriendList.friend_id).all()
    
        
        selectfriend = request.dbsession.query(FriendList).all()
        for value in selectfriend:
            if int(myid) == value.my_id:
                 selectname = request.dbsession.query(User).filter_by(id= value.friend_id).first()
                 select.append(selectname.username)   
                 
        # for n in range(0,len(query)-1):
        #     if not query[n][1] in friends:
        #         friends.append(query[n][1]);n+1
        for user in alluser:
            if user.username!=username:
                if user.username not in select:
                    filteruser.append(user)
                
        # import ipdb;ipdb.set_trace()   
        return dict(UserName = cradentials.username  , user_id =  cradentials.id,alluser = filteruser)

    else:
        return HTTPFound(location = request.route_url('login'))


        

@view_config(route_name = 'addfriend')
def addfriend(request):
    session = request.session
    username = session['username_name']
    cradentials = request.dbsession.query(User).filter_by(username = username).first()
    if username != '':
        myid = request.params['myid']
        friendid = request.params['friendid']
        request.dbsession.add(FriendList(friend_id = friendid,my_id = myid))
        return HTTPFound(location = request.route_url('home'))
    else:
        return HTTPFound(location = request.route_url('login'))

@view_config(route_name = 'myprofile',renderer = '../templates/myprofile.jinja2')
def myprofile(request):
    session = request.session
    username = session['username_name']
    cradentials = request.dbsession.query(User).filter_by(username = username).first()
    if username != '':
        myid = request.params['myid']
        friendid = ''
        friends,select = [],[]
        cradentials = request.dbsession.query(FriendList).filter_by(my_id =myid).all()
        for userid in cradentials:
             if userid.my_id == int(myid.encode("utf-8")):
                friendid = myid
        query = request.dbsession.query(FriendList,User.username).join(User, User.id==FriendList.friend_id).all()
        myusername = request.dbsession.query(FriendList,User.username).join(User, User.id==FriendList.my_id).first()
        # friends = query[0][1]
        for n in range(0,len(query)-1):
            if not query[n][1] in friends:
                friends.append(query[n][1]);n+1

        selectfriend = request.dbsession.query(FriendList).all()
        for value in selectfriend:
            if int(myid.encode("utf-8")) == value.my_id:
                 selectname = request.dbsession.query(User).filter_by(id= value.friend_id).first()
                 select.append(selectname)   
        # import ipdb;ipdb.set_trace()

        return dict(myid= myid,select = select,myusername = username)
    else:
        return HTTPFound(location = request.route_url('login'))
    

@view_config(route_name = 'deletefriend',renderer = '../templates/myprofile.jinja2')
def deletefriend(request):
    session = request.session
    username = session['username_name']
    cradentials = request.dbsession.query(User).filter_by(username = username).first()
    if username != '':
          deletefriend = request.params['friendname']
          getdeletefriendid = request.dbsession.query(User).filter_by(username = deletefriend)
          friendid = ''
            # getdeletefriendid = request.dbsession.query(FriendList,User.id).join(User, User.id==FriendList.friend_id).all()
          for userid in getdeletefriendid:
            friendid = userid.id
            
             # import ipdb;ipdb.set_trace()
          deletefriendbyname = request.dbsession.query(FriendList).filter_by(friend_id = int(friendid)).first()
          request.dbsession.delete(deletefriendbyname)
  
          return HTTPFound(location = request.route_url('home'))
    else:
        return HTTPFound(location = request.route_url('login'))



@view_config(route_name = 'storeuser',request_method = 'POST')
def storeuser(request):
    username = request.params['form-username']
    password = request.params['form-password']
    email = request.params['form-email']
    age = request.params['form-age']
    alluser = request.dbsession.query(User).all()
    for user in alluser:
        if username == user.username :
                return render_to_response('../templates/addnewuser.jinja2',{'error' :'please choose Unqiue UserName'},request =request)
        if email == user.email:
                return render_to_response("../templates/addnewuser.jinja2",{ 'error' :'please choose Unqiue email'},   request = request)
        
    else:
        request.dbsession.add(User(username = username,password= password,email = email,age = age))
        return HTTPFound(location = request.route_url('login'))
   
       
   
@view_config(route_name='logout')
def logout(request):
    # DBSession.query(User).filter(User.id==request.user.id).update({"verified":'N'}) #making the verified 'N' again

    session=request.session
    headers=forget(request)
    session['username_name'] = ''

    return HTTPFound(location=request.route_url('login'),headers=headers)

@view_config(route_name = 'viewprofile',renderer = '../templates/viewprofile.jinja2')
def viewprofile(request):
    session = request.session
    username = session['username_name']
    cradentials = request.dbsession.query(User).filter_by(username = username).first()
    if username != '':
        select = []
        myid = request.params['myid']
        friendid = request.params['friendid']
        selectfriend  = request.dbsession.query(FriendList).all()
        allblog = request.dbsession.query(FriendBlogs).filter_by(friend_id = friendid).all()
        friendid = request.params['friendid'].encode("utf-8")
        friendname = request.dbsession.query(User).filter_by(id = int(friendid)).first()
        for value in selectfriend:
            if int(myid.encode("utf-8")) == value.my_id:
                 selectname = request.dbsession.query(User).filter_by(id= value.friend_id).first()
                 select.append(selectname.username) 
        return dict(myid = myid,friendid = friendid,username=friendname,allblog  = allblog,friendname = friendname )
    else:
        return HTTPFound(location = request.route_url('login'))

@view_config(route_name = 'myviewprofile',renderer = '../templates/viewprofile.jinja2')
def myviewprofile(request):
    session = request.session
    username = session['username_name']
    cradentials = request.dbsession.query(User).filter_by(username = username).first()
    if username != '':
        select = []
        myid = request.params['myid']
        friendid = request.params['friendid'].encode("utf-8")
        friendname = request.dbsession.query(User).filter_by(id = int(friendid)).first()
        selectfriend  = request.dbsession.query(FriendList).all()
        allblog = request.dbsession.query(FriendBlogs).all()        
        # allblog = request.dbsession.query(FriendBlogs).all() 
        allblog = request.dbsession.query(FriendBlogs).filter_by(friend_id = friendid).all()
        # import ipdb;ipdb.set_trace()
        for value in selectfriend:
            if int(myid.encode("utf-8")) == value.my_id:
                 selectname = request.dbsession.query(User).filter_by(id= value.friend_id).first()
                 select.append(selectname) 
        return dict(myid = myid,friendid = friendid,username= friendname,selectname= selectname,allblog = allblog)
    else:
        return HTTPFound(location = request.route_url('login'))
@view_config(route_name = 'storeblog')
def storeblog(request):
    myid = request.params['myid']
    friendid = request.params['friendid']
    textarea=request.params['textarea']
    friendid_name = int(myid.encode("utf-8"))
    friendname = request.dbsession.query(User).filter_by(id = int(friendid)).first()
    myname =  request.dbsession.query(User).filter_by(id = int(myid.encode("utf-8"))).first()
    # import ipdb;ipdb.set_trace()
    request.dbsession.add(FriendBlogs(friend_id= friendid,my_id= myid,blog = textarea,friend_name = myname.username))
    return HTTPFound(location = request.route_url('home'))


    



 

    



    


       



   

         

   
 
         



