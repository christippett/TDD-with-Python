from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
import sys

class FunctionalTest(StaticLiveServerTestCase):
	
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass() # run the normal superclass setup
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self): # This method runs before each test
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3) # Force selenium to wait 3 seconds before continuing with the test
		# NB: implicitly_wait won't work for every use case. More sophisticated
		# 'explicit' wait algorithms may be needed as apps grow in complexity
		
	def tearDown(self): # This method runs after each test. This method will run even if the test fails and causes an error (unless an error occurs in the setUp method)
		self.browser.quit()
		
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])
