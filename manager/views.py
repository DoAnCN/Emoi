from django.shortcuts import render
import sweetify

# Create your views here.
def test_view(request):
	sweetify.success(request, "You did it', text='Good job! You successfully showed a SweetAlert message', persistent='Hell yeah')
	return redirect('/')
