from django.core.paginator import Paginator
from django.shortcuts import render

from books.models import Book


def books_view(request):
    books_object = Book.objects.all()
    template = 'books/books_list.html'
    context = {'books': books_object}
    return render(request, template, context)

def books_details(request, date):
    books_object = Book.objects.all()
    template = 'books/books_details.html'
    books_pub_dates = sorted(list({str(book.pub_date) for book in books_object}))
    paginator = Paginator(books_pub_dates, 1)
    
    if date not in books_pub_dates:
        date = books_pub_dates[0]

    current_page = paginator.get_page(books_pub_dates.index(date)+1)

    books_by_date = [book for book in books_object if str(book.pub_date) == date]
    
    prev_page = None
    next_page = None

    if current_page.has_previous():
        prev_page = paginator.get_page(books_pub_dates.index(date)).object_list[0]
    if current_page.has_next():
        next_page = paginator.get_page(books_pub_dates.index(date)+2).object_list[0]

    context = {
        'books': books_by_date,
        'current_page': current_page,
        'prev_page': prev_page,
        'next_page': next_page
    }

    return render(request, template, context)
