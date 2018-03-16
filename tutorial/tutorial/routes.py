def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('login', '/')
    config.add_route('addnewuser','/addnewuser')
    config.add_route('storeuser','/storeuser')
    config.add_route('checkuser','/checkuser')
    config.add_route('home','/home')
    config.add_route('addfriend','/addfriend')
    config.add_route('logout','/logout')
    config.add_route('myprofile','/myprofile')
    config.add_route('deletefriend','/deletefriend')
    config.add_route('viewprofile','/viewprofile')
    config.add_route('myviewprofile','/myviewprofile')
    config.add_route('storeblog','/storeblog')
    