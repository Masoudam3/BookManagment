from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required

from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Author
from .models import Book
from .models import BookInstance
from .models import Genre

from .forms import RenewBookForm
from .forms import CreteUserForm
from .forms import LoginUserForm
import datetime

from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


def register(request):
    if request.method == "POST" :
        form = CreteUserForm(request.POST) 
        if form.is_valid:       
            username = request.POST["username"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            email = request.POST["email"]
            form.save()
            user = authenticate(username = username, email= email, password = password2)
            if user is not None:
                login (request, user)
                url = reverse("book:index")
                return HttpResponseRedirect(url)

    form = CreteUserForm()

    context = {
        "form":form,
    }
    return render(request, "registration/sign_up.html", context)

def sign_in(request):
    if request.method == "POST":
        form = LoginUserForm(request.POST)
        if form.is_valid:
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username = username, password =password)
            if user is not None:
                login (request, user)
                url = reverse("book:index")
                return HttpResponseRedirect(url)
                
    else:
        form = LoginUserForm(request.POST)
    context = {
        "form":form,
    }
    return render(request, "registration/login.html", context,)
         

# @login_required

def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact = "a").count()
    num_authors = Author.objects.all().count()
    context = {
        "num_books" : num_books ,
        "num_instances" : num_instances ,
        "num_instances_available" : num_instances_available ,
        "num_authors" : num_authors , 
    }
    
    return render(request, "book/index.html", context)
    
    # if request.user.is_authenticated:
    #     return render(request, "book/index.html", context)
    # else :
    #     return render(request, "accounts/login.html", context)


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book
    context_object_name = "book_list"
    template_name = "book/book_list.html"
    paginate_by = 5
    
    # queryset = Book.objects.filter(title__icontains = "django")
    # login_url = "accounts/login"
    # redirect_field_name = "/"

    
class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = "book/book_detail.html"


class LonedBookByUserListView(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = "book/book_instance_list_borrower_user.html"
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(borrower = self.request.user).filter(status__exact = "o").order_by("due_back")


class AutorListView(LoginRequiredMixin, generic.ListView):
    moedel = Author
    context_object_name = "authors_list"
    template_name = "book/author_list_view.html"
    paginate_by = 5
    
    def get_queryset(self):
        return Author.objects.all()
    

class BorrowedBooklist(LoginRequiredMixin, generic.ListView):
    model = BookInstance
    context_object_name = "borrowed_book_list"
    template_name = "book/borrowed_book_list.html"
    paginate_by = 5

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact = "o")

@login_required
def renew_book_librarian(request, pk):
    book_inst = get_object_or_404(BookInstance, pk = pk)

    if request.method == "POST" :
        form = RenewBookForm(request.POST)

        if form.is_valid():
            book_inst.due_back = form.cleaned_data["renewal_date"]
            book_inst.save()


        url = reverse("book:borrowed")
        return HttpResponseRedirect(url)
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks = 3)
        form = RenewBookForm(initial = {"renewal_date" : proposed_renewal_date})
    
    context = {
        "form" : form,
        "bookinst" : book_inst
    }

    return render(request, "book/book_renew_librarian.html", context)

                  