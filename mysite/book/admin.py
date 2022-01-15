from django.contrib import admin
from django.contrib.admin.decorators import register

from .models import Book, BookInstance, Author, Genre

# admin.site.register(Book)
# admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(BookInstance)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "date_of_birth", "date_of_death")
    fields = [
        "first_name",
        "last_name",
        ("date_of_birth", "date_of_death"),
    ]

class BookInstanceinline(admin.TabularInline):
    model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "display_genre")
    inlines = [BookInstanceinline]

    def display_genre(self, obj):
        return ", ".join([genre.name for genre in obj.genre.all()])

    display_genre.short_description = "Genre"    


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ("book", "status", "borrower", "due_back", "id")
    list_filter = ("status", "due_back")
    fieldsets = [(None, {"fields" : ("book", "imprint")}) , 
                ("availablity", {"fields" : ("status", "due_back", "borrower")})]
    
