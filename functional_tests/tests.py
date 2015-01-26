from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# import unittest

# NB: unittest provides helper functions such as assertIn, 
# assertEqual, assertTrue, assertFalse, etc - see unittest 
# documentation for more information


class NewVisitorTest(LiveServerTestCase): # Tests are organised into classes, which inherit from unittest.TestCase
	
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
		
	def test_can_start_a_list_and_retrieve_it_later(self): # Any method whose name starts with 'test' is a test method, and will be run by the test runner. You can have more than one test_ method per class
		
		# NB: It is useful to write a story as to how the user will use
		# and interact with your app, hence the introduction of 'Edith'
		
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
# 		self.browser.get('http://localhost:8000')
		self.browser.get(self.live_server_url)
		
		# She notices the page title and head mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)
				
		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		
		# She types "Buy peacock feathers" into a text box
		inputbox.send_keys('Buy peacock feathers')
		
		# When she hits enter,  she is taken to a new URL,
		# and now the page lists "1: Buy peacock feathers" as an item
		# in a to-do list table
		inputbox.send_keys(Keys.ENTER)
		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		
# 		import time
# 		time.sleep(10)
		
# 		table = self.browser.find_element_by_id('id_list_table')
# 		rows = table.find_elements_by_tag_name('tr')
# 		self.assertTrue(
# 			any(row.text == '1: Buy peacock feathers' for row in rows), # any() is a Python built-in function
# 			"New to-do item did not appear in table -- its text was:\n%s" % (table.text,)
# 		)

# 		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
# 		self.assertIn(
# 			'2: Use peacock feathers to make a fly' ,
# 			[row.text for row in rows]
# 		)

		# There is still a text box inviting her to add another item
		# She enters "Use peacock feathers to make a fly"
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Use peacock feathers to make a fly')
		inputbox.send_keys(Keys.ENTER)
		
		# The page updates again and shows both items in the list
		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
		
		# Now a new user, Francis, comes along to the site
		
		## We use a new browser session to make sure that no information
		## of Edith's is coming through from cookies, etc
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Francis visits the home page. There is no sign of Edith's list
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('buy peacock feathers', page_text)
		self.assertNotIn('make a fly', page_text)
		
		# Francis starts a new list by entering a new item. He
		# is less interesting than Edith...
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		
		# Francies gets his own unique URL
		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)
		
		# Again, there is no trace of Edith's list
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Buy peacock feathers', page_text)
		self.assertIn('Buy milk', page_text)
		
		# Satisfied, they both go back to sleep


# No longer needed since we're using Django's LiveServerTestCase
# if __name__ == '__main__': # Is this script being run from the command-line?
# 	unittest.main(warnings='ignore') # Launch the test runner. It will automatically find test classes and methods in the file and run them