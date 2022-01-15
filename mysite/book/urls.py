from django.urls import path, re_path

from . import views


app_name = "book"
urlpatterns = [
    path("", views.index, name = "index"),
    path("list/", views.BookListView.as_view() , name = "booklist"),
    path("list/authors/", views.AutorListView.as_view(), name = "authorlist"),
    re_path("^detail/(?P<pk>\d+)/$", views.BookDetailView.as_view(), name = "bookdetail"),
    path("mybooks/", views.LonedBookByUserListView.as_view(), name = "mybooks"),
    path("detail/<uuid:pk>/renew/",views.renew_book_librarian, name = "ranewbooklibrarian"),
    path("borrowed/", views.BorrowedBooklist.as_view(), name = "borrowed"),
    path("sign_up/", views.register, name = "sign_up" ),
    path("sign_in/", views.sign_in, name = "sign_in")
] 