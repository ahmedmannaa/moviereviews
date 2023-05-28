from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import Movie, Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required

def home(request):
    searchTerm = request.GET.get('searchMovie')
    if searchTerm:
        movies = Movie.objects.filter(title__icontains=searchTerm)
    else:
        movies = Movie.objects.all()

    return render(request, 'home.html', {
        'searchTerm': searchTerm,
        'movies': movies
    })


def about(request):
    return HttpResponse('<h1>Welcome to About Page</h1>')


def signup(request):
    email = request.GET.get('email')
    return render(request, 'signup.html', {'email': email})


def details(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    reviews = Review.objects.filter(movie=movie)
    return render(request, 'detail.html', {'movie': movie, 'reviews': reviews})

@login_required
def createreview(req, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)

    if req.method == 'GET':
        return render(req, 'createreview.html', {
            'form': ReviewForm(),
            'movie': movie
        })
    else:
        try:
            form = ReviewForm(req.POST)
            newReview = form.save(commit=False)
            newReview.user = req.user
            newReview.movie = movie
            newReview.save()
            return redirect('detail', newReview.movie.id)
        except ValueError:
            return render(req, 'createreview.html', {
                'form': ReviewForm(),
                'error': 'bad data passed in'
            })

@login_required
def updatereview(req, review_id):
    review = get_object_or_404(Review, pk=review_id, user=req.user)
    if req.method == 'GET':
        form = ReviewForm(instance=review)
        return render(req, 'updatereview.html', {
            'review': review, 'form': form
        })
    else:
        try:
            form = ReviewForm(req.POST, instance=review)
            form.save()
            return redirect('detail', review.movie_id)
        except ValueError:
            return render(req, 'updatereview.html', {
                'review': review,
                'form': form,
                'error': 'Bad data in form'
            })

@login_required
def deletereview(req, review_id):
    review = get_object_or_404(Review, pk=review_id, user=req.user)
    review.delete()
    return redirect('detail', review.movie.id)
