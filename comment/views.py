from django.shortcuts import render,get_object_or_404,redirect

from blog.models import Post

from .models import Comment
from .forms import CommentForm

def post_comment(request,post_pk):
    # 获得要评论的文章
    post = get_object_or_404(Post,pk=post_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST) # 实例化表单对象
        if form.is_valid():
            comment = form.save(commit=False) # 由表单对象得到模型对象
            comment.post = post
            comment.save()
            # 可以直接重定向到Post模型对象当中
            # 因为，指定了get_absolute_url
            return redirect(post)
        else:
            # 获取文章已有评论
            comment_list = post.comment_set.all()
            context = {
                'post':post,
                'form':form,
                'comment_list':comment_list,
            }
            return render(request,'blog/detail.html',context=context)
    return redirect(post)
