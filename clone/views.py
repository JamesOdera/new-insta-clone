from django.shortcuts import render
from django.http  import HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
import datetime as dt
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.forms import * 


def index(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'index.html', context)

def about(request):
    return render(request, 'clone/about.html')

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    ordering = ['-pub_date']
    template_name = 'index.html'


    #  def get_queryset(self):
    #   return Post.objects.all()

    # def get_queryset(self):
    #   return Comment.objects.order_by('id')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = [ 'title', 'content', 'cover']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)



class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = [ 'title', 'content', 'cover']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False