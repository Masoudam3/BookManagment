from django.db import models
from django.contrib.auth.models import User

from datetime import date

from uuid import uuid4


class Genre(models.Model):
    """
    Model representing a genre (e.g. Science fiction, French poetery etc).
    """
    name = models.CharField(max_length = 200, help_text = "Enter a book genre(e.g. Science fiction, French poetery etc.)")

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Model representing a book (but not a specific copy a book).
    """
    title = models.CharField(max_length = 200)
    summery = models.TextField(max_length = 1000, help_text = "Enter a brief description of the book")
    isbn = models.CharField(max_length = 13, help_text = "13 character <a href = 'https://www.isbn-international.org/content/what-isbn'>ISBN nuber</a>")
    
    # ManyToManyField used because genre can contain many book. Book can coverd many genre 
    genre = models.ManyToManyField(Genre, help_text = "Select a genre for this book")
    
    # ForeignKey used because books can only have one author , but authro can have multiple books
    author = models.ForeignKey("Author", on_delete = models.SET_NULL, null = True)
    
    def __str__(self):
        return self.title




class Author(models.Model):
    """
    Model representing an aurthor.
    """
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100) 
    date_of_birth = models.DateField(null = True, blank = True)
    date_of_death = models.DateField("Died", null = True, blank = True)

    class Meta:
        ordering =["last_name", "first_name"]

    def __str__(self):
        return ("{0}, {1}".format(self.last_name, self.first_name))


class BookInstance(models.Model):
    """
    Model representing a copy of book.
    """
    id = models.UUIDField(primary_key= True, default = uuid4, 
                        help_text = "unique ID for this particular book aroos whole library.")
    book = models.ForeignKey("Book", on_delete = models.SET_NULL , null = True)
    imprint = models.CharField(max_length = 200)
    due_back = models.DateField(null = True, blank = True)
    borrower = models.ForeignKey(User, on_delete = models.SET_NULL, null = True, blank = True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Avialable"),
        ("r", "Reserved"),
    )

    status = models.CharField(max_length = 1, choices = LOAN_STATUS, 
                            blank = True, default = "m", help_text = "Book avilability")

    class Meta:
        ordering = ["due_back"]
        permissions = (
            ("can_read_private_section", "VIP_user"),
            ("user_watcher", "User Watcher")
        )
    
    @property
    def is_overdue (self):
        if self.due_back and date.today() > self.due_back :
            return True
        
        return False      

    def __str__(self):
        return ("{0}: ({1})".format(self.book.title, self.id))                
