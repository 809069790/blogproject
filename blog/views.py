from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Tag
from markdown import markdown
from django.views.generic import ListView,DetailView

from comment.forms import CommentForm
from django.http import HttpResponse

class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 1

    def pagination_data(self,paginator,page,is_paginated):
        if not is_paginated:
            return {}

        #设置默认值
        first = False
        left_has_more = False
        left = []
        page_number = page.number
        right = []
        right_has_more = False
        last = False
        #总页数
        total_pages = paginator.num_pages
        #获取整个分页页码列表，例如[1,2,3,4]
        page_range = paginator.page_range

        #如果当前是第一页
        if page_number == 1:
            right = page_range[page_number:page_number+2]
            if right[-1] <total_pages-1:
                right_has_more = True

            if right[-1]<total_pages:
                last = True

        elif page_number == total_pages:
            left = page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]
            if left[0]>2:
                left_has_more = True
            if left[0]>1:
                first = True
        else:
            left = page_range[(page_number-3) if (page_number-3)>0 else 0:page_number-1]
            right = page_range[page_number:page_number+2]
            if right[-1]<total_pages-1:
                right_has_more =True
            if right[-1]<total_pages:
                last = True
            if left[0]>2:
                left_has_more = True
            if left[0]>1:
                first = True
        data = {
            'first':first,
            'left_has_more':left_has_more,
            'left':left,
            'page_number':page_number,
            'right_has_more':right_has_more,
            'right':right,
            'last':last,
        }
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        pagination_data = self.pagination_data(paginator,page,is_paginated)
        context.update(pagination_data)

        return context

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

class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag,pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)