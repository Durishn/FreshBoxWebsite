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

    @view_config(renderer="templates/contact_us.pt",
                 name="contact_us")
    def company_view(self):
        return {"page_title": "Contact Us"}
    
    @view_config(renderer="templates/about_us.pt",
                 name="about_us")
    def company_view(self):
        return {"page_title": "About Us"}
                
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
    
    @view_config(renderer='templates/test_ajax.pt', name='test_ajax')
    def test_ajax(self):
        return {"page_title": "Test AJAX"}
        
    @view_config(renderer='json', name='test.json')
    def test_json(self):
        return {"data":"This is an AJAX call"}
