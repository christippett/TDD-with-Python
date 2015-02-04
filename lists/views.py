from django.shortcuts import render, redirect
from lists.models import Item, List
from django.core.exceptions import ValidationError
# from django.http import HttpResponse # no longer needed since we're rendering page using template engine

# Create your views here.
# home_page = None

# ======================
# ITERATION 1
# ======================
# def home_page(request):
# # 	return HttpResponse('<html><title>To-Do lists</title></html>')
# # 	if request.method == 'POST':
# # 		return HttpResponse(request.POST['item_text'])
# 
# 	item = Item()
# 	item.text = request.POST.get('item_text', '')
# 	item.save()
# 	
# 	return render(
# 		request, 
# 		'home.html',
# 		{'new_item_text': request.POST.get('item_text', ''),}
# 	)

# ======================
# ITERATION 2
# ======================
# def home_page(request):
# 	if request.method == 'POST':
# 		new_item_text = request.POST['item_text']
# 		Item.objects.create(text=new_item_text) # shorthand for creating a new Item, without needing to call .save()
# 	else:
# 		new_item_text = ''
# 	
# 	return render(
# 		request, 
# 		'home.html',
# 		{'new_item_text': request.POST.get('item_text', ''),}
# 	)

# ======================
# ITERATION 3
# ======================
def home_page(request):
	return render(request, 'home.html')

	# # The home_page view no longer handles new list creation
	# if request.method == 'POST':
	# 	Item.objects.create(text=request.POST['item_text']) 
	# 	# return redirect('/')
	# 	return redirect('/lists/the-only-list-in-the-world/')

	# # Return the contents of the POST variable directly to template
	# # (does not save to DB)
	# return render(
	# 	request, 
	# 	'home.html',
	# 	{'new_item_text': request.POST.get('item_text', ''),}
	# )
	
	# # Get all Items from database and load into template
	# items = Item.objects.all()
	# return render(
	# 	request, 
	# 	'home.html',
	# 	{'items': items,}
	# )

def view_list(request, list_id):
	# items = Item.objects.all()
	list_ = List.objects.get(id=list_id)
	items = Item.objects.filter(list=list_)
	return render(
		request, 
		'list.html',
		# {'items': items,}
		{'list': list_}
	)

def new_list(request):
	list_ = List.objects.create()
	#item = Item.objects.create(text=request.POST['item_text'], list=list_)
	item = Item(text=request.POST['item_text'], list=list_)
	try:
		item.full_clean()
		item.save()
	except ValidationError:
		list_.delete()
		error = "You can't have an empty list item"
		return render(request, 'home.html', {"error": error})
	return redirect('/lists/%d/' % (list_.id,))

def add_item(request, list_id):
	list_ = List.objects.get(id=list_id)
	Item.objects.create(text=request.POST['item_text'], list=list_)

	return redirect('/lists/%d/' % (list_.id,))


