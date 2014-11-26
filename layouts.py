from pyramid.renderers import get_renderer
from pyramid.decorator import reify

from dummy_data import *

class Layouts(object):

	@reify
	def global_template(self):
		renderer = get_renderer("templates/global_layout.pt")
		return renderer.implementation().macros['layout']

	@reify
	def company_name(self):
		return COMPANY

	@reify
	def site_menu(self):
		new_menu = getMenu(self)[:]
		url = self.request.url
		for menu in new_menu:
			if menu['title'] == 'Home':
				menu['current'] = url.endswith('/')
			else:
				menu['current'] = url.endswith(menu['href'])
		return new_menu
		
	@reify
	def get_users(self):
		return getUsers()

	@reify
	def get_host_sites(self):
		retVal = [];
		if("userType" in self.request.session):
			if(self.request.session['userType'] == "Administrator"):
				retVal = getHostSites()
			elif(self.request.session['userType'] == "Coordinator"):
				retVal = getHostSiteList(self.request.session['userID'])
		return retVal
		
	@reify
	def get_orders(self):
		retVal = []
		return getAllOrders()
		
		#hostsite_id = self.request.POST.get('hsid')
		#if (hostsite_id != None):
		#	retVal = getOrders(hostsite_id)
		#return retVal