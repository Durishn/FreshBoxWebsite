from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from dummy_data import getUsers
from dummy_data import userType
#from dummy_data import PROJECTS

from layouts import Layouts

class ProjectorViews(Layouts):

    def __init__(self, request):
        self.request = request
        
    @view_config(renderer="templates/index.pt")
    def index_view(self):
        return {"page_title": "Home"}

    @view_config(renderer="templates/company.pt",
                 name="contact")
    def company_view(self):
        return {"page_title": "Contact Us"}
                
    @view_config(renderer="templates/login.pt",
                name="login")
    def login_view(self):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')
        self.request.session['userType'] = userType(username,password)
        if(userType(username,password) == 'admin'):
            return HTTPFound(location='/')
        return {"page_title": "Login"}
    
    @view_config(renderer="templates/index.pt",
                name="logout")
    def logout_view(self):
        self.request.session['userType'] = 'none'
        return HTTPFound(location='/')