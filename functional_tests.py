from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

# NB: unittest provides helper functions such as assertIn, 
# assertEqual, assertTrue, assertFalse, etc - see unittest 
# documentation for more information


class NewVisitorTest(unittest.TestCase): # Tests are organised into classes, which inherit from unittest.TestCase
	
	def setUp(self): # This method runs before each test
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3) # Force selenium to wait 3 seconds before continuing with the test
		
		# NB: implicitly_wait won't work for every use case. More sophisticated
		# 'explicit' wait algorithms may be needed as apps grow in complexity
		
	def tearDown(self): # This method runs after each test. This method will run even if the test fails and causes an error (unless an error occurs in the setUp method)
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self): # Any method whose name starts with 'test' is a test method, and will be run by the test runner. You can have more than one test_ method per class
		
		# NB: It is useful to write a story as to how the user will use
		# and interact with your app, hence the introduction of 'Edith'
		
		# Edith has heard about a cool new online to-do app. She goes
		# to check out its homepage
		self.browser.get('http://localhost:8000')
		
		# She notices the page title and head mention to-do lists
		self.assertIn('To-Do', self.browser.title)
		
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertEqual('To-Do', header_text)
				
		# She is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)
		
		# She types "Buy peacock feathers" into a text box
		inputbox.send_keys('Buy peacock feathers')
		
		# When she hits enter, the page updates. The page now lists
		# "1: Buy peacock feathers" as an item in the to-do list
		inputbox.send_keys(Keys.ENTER)
		
		# import time
		# time.sleep(10)
		
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
# 		self.assertTrue(
# 			any(row.text == '1: Buy peacock feathers' for row in rows), # any() is a Python built-in function
# 			"New to-do item did not appear in table -- its text was:\n%s" % (table.text,)
# 		)

		self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
		self.assertIn(
			'2: Use peacock feathers to make a fly' ,
			[row.text for row in rows]
		)
		
		# There is still a text box inviting her to add another item
		# She enters "Use peacock feathers to make a fly"
		self.fail('Finish the test!')

		
		# The page updates again and shows both items in the list
		
		# Edit wonders whether the site will remember her list. She
		# sees the site has generated a unique URL for her -- there is
		# some explantory text to that effect
		
		# She visits that URL - her to-do list is still there
		
		# Satisfied, she goes back to sleep


if __name__ == '__main__': # Is this script being run from the command-line?
	unittest.main(warnings='ignore') # Launch the test runner. It will automatically find test classes and methods in the file and run them