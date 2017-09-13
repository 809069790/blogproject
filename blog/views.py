from django.shortcuts import render,get_object_or_404
from .models import Post,Category
from markdown import markdown
from django.views.generic import ListView,DetailView

from comment.forms import CommentForm
from django.http import HttpResponse

# def index(request):
#     post_list = Post.objects.all()
#     return render(request,'blog/index.html',context={'post_list':post_list})
    # return HttpResponse('<h1>hello world</h1>')
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'

# def detail(request,pk):
#     post = get_object_or_404(Post,pk=pk)
#     post.increase_views()
#     post.body = markdown(post.body,extensions=[
#                          'markdown.extensions.extra',
#                          'markdown.extensions.codehilite',
#                          'markdown.extensions.toc',])
#     form = CommentForm()
#     comment_list = post.comment_set.all()
#     context = {
#         'post':post,
#         'form':form,
#         'comment_list':comment_list,
#     }
#     return render(request,'blog/detail.html',context=context)

# def archives(request,year,month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month)
#     return render(request,'blog/index.html',context={'post_list':post_list})

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self,request,*args,**kwargs):
        response = super().get(request,*args,**kwargs)
        self.object.increase_views()

        return response

    def get_object(self, queryset=None):
        post = super().get_object(queryset)
        post.body = markdown(post.body,extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form':form,
            'comment_list':comment_list,
        })
        return context

class ArchivesView(IndexView):
    def get_queryset(self):
        return super().get_queryset().filter(
            created_time__year = self.kwargs.get('year'),
            created_time__month = self.kwargs.get('month')
        )

# def category(request,pk):
#     cate = get_object_or_404(Category,pk=pk)
#     post_list = Post.objects.filter(category=cate)
#     return render(request,'blog/index.html',context={'post_list':post_list})
class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)