from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase): # Tests are organised into classes, which inherit from unittest.TestCase
	
	def setUp(self): # This method runs before each test
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3) # Force selenium to wait 3 seconds before continuing with the test
		
		# NB: implicitly_wait won't work for every use case. More sophisticated
		# 'explicit' wait algorithms may be needed as apps grow in complexity
		
	def tearDown(self): # This method runs after each test. This method will run even if the test fails and causes an error
		self.browser.quit()
		
	def test_can_start_a_list_and_retrieve_it_later(self): # Any method whose name starts with 'test' is a test method, and will be run by the test runner. You can have more than one test_ method per class
		
		# Edit has heard about a cool new online to-do app. She goes
		# to check out its homepage
		self.browser.get('http://localhost:8000')
		
		# She notices the page title and head mention to-do lists
		self.assertIn('To-Do', self.browser.title) # unittest provides helper functions such as assertIn, assertEqual, assertTrue, assertFalse, etc - see unittest documentation for more information
		self.fail('Finish the test!')
		
		# She is invited to enter a to-do item straight away
		
		# She types "Buy peacock feathers" into a text box
		
		# When she hits enter, the page updates. The page now lists
		# "1: Buy peacock feathers" as an item in the to-do list
		
		# There is still a text box inviting her to add another item
		# She enters "Use peacock feathers to make a fly"
		
		# The page updates again and shows both items in the list
		
		# Edit wonders whether the site will remember her list. She
		# sees the site has generated a unique URL for her -- there is
		# some explantory text to that effect
		
		# She visits that URL - her to-do list is still there
		
		# Satisfied, she goes back to sleep


if __name__ == '__main__': # Is this script being run from the command-line?
	unittest.main(warnings='ignore') # Launch the test runner. It will automatically find test classes and methods in the file and run them