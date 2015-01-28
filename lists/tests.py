from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List

# Import view function
from lists.views import home_page, view_list # home_page is the view function stored in lists/views.py

# TestCase is an augmented version of the standard unittest.TestCase,
# with some Django-specific features thrown in

# class SmokeTest(TestCase):
# 	
# 	def test_bad_maths(self):
# 		self.assertEqual(1 + 1, 3)

class HomePageTest(TestCase):
	
	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/') # function Django uses internally to resolve URLs and find what view function they should be mapped to
		self.assertEqual(found.func, home_page) # Check that resolve, when called with '/', finds a function called home_page
		
	def test_home_page_returns_correct_html(self):
		request = HttpRequest() # An HttpRequest object, this is what Django sees when a user's browser asks for a page
		response = home_page(request) # We pass this request to our home_page view, which gives a reponse in form of an HttpResponse object
		expected_html = render_to_string('home.html')
		self.assertEqual(response.content.decode(), expected_html)
		
		self.assertTrue(response.content.startswith(b'<html>'))
		self.assertIn(b'<title>To-Do lists</title>', response.content)
		self.assertTrue(response.content.endswith(b'</html>'))
		
		# NB: response.content is the HTML contents of the HttpResponse object
		
		# NB: response.content is in raw bytes, not a Python string, so
		# we have to use the b'' syntax to compare them (converts string to bytes)
		
	# def test_home_page_only_saves_items_when_necessary(self):
	# 	request = HttpRequest()
	# 	home_page(request)
	# 	self.assertEqual(Item.objects.count(), 0)
		
	# def test_home_page_displays_all_list_items(self):
	# 	Item.objects.create(text='itemey 1')
	# 	Item.objects.create(text='itemey 2')
	# 	request = HttpRequest()
	# 	response = home_page(request)
	# 	self.assertIn('itemey 1', response.content.decode())
	# 	self.assertIn('itemey 2', response.content.decode())
		
class ListAndItemModelTest(TestCase):
	
	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()

		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)

class ListsViewTest(TestCase):

	def test_uses_list_template(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id))
		self.assertTemplateUsed(response, 'list.html')

	def test_displays_only_items_for_that_list(self):
		correct_list = List.objects.create()
		Item.objects.create(text='itemey 1', list=correct_list)
		Item.objects.create(text='itemey 2', list=correct_list)

		other_list = List.objects.create()
		Item.objects.create(text='other list item 1', list=other_list)
		Item.objects.create(text='other list item 2', list=other_list)

		# Instead of calling the view function directly, we use
		# the Django test client, which is an attribute of the
		# Django TestCase called self.client
		response = self.client.get('/lists/%d/' % (correct_list.id))

		# Django's assertContains method knows how to deal with
		# responses and the bytes of their content (no need for .decode())
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

		# # Old way of testing:
		# request = HttpRequest()
		# response = view_list(request)
		
		# self.assertIn('itemey 1', response.content.decode())
		# self.assertIn('itemey 2', response.content.decode())

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list) # response.context represents the context passed to the render function


class NewListTest(TestCase):

	def test_saving_a_POST_request(self):
		# request = HttpRequest()
		# request.method = 'POST'
		# request.POST['item_text'] = 'A new list item'
		
		# response = home_page(request)

		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
		
	def test_redirects_after_POST(self):
		# request = HttpRequest()
		# request.method = 'POST'
		# request.POST['item_text'] = 'A new list item'
		
		# response = home_page(request)

		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		
		new_list = List.objects.first()
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

		# a - code sample
		# self.assertEqual(response.status_code, 302)
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
		
		# b - code sample
		# expected_html = render_to_string(
		# 	'home.html',
		# 	{'new_item_text': 'A new list item'}
		# )
		# self.assertEqual(response.content.decode(), expected_html)

class NewItemTest(TestCase):

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/add_item' % (correct_list.id,),
			data={'item_text': 'A new item for an existing list'}
		)

		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

		
		