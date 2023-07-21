from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404

from .forms import *
from .models import *
menu = [{'title':"Добавить отзыв",'url_name':'add_comment'},
        # {'title':"О сайте",'url_name':'about'}
            # {'title':"Войти",'url_name':"login"}
]


def index(request):
    posts = Comment.objects.all()

    context ={'posts':posts,
               'menu': menu,
               'title':'Главная страница',
              'cat_selected':3,
              }

    return render(request,'commnets/index.html',context = context)




def about(request):
    return render(request,'commnets/about.html', {'menu': menu ,'title':'О сайте'})


def cat(request,catid):
    if catid>100:
        raise Http404()

    if catid > 50:
        return redirect("home",permanent=True)

    if (request.GET):
        print(request.GET)

    return HttpResponse(f'<h1>Категории</h1><p>{catid}</p>')





def add_comment(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST)

        if form.is_valid():
            # print(form.cleaned_data)
            form.save()
            # Comment.objects.create(**form.cleaned_data)
            # return redirect('home')

            try:
                # Comment.objects.create(**form.cleaned_data)
                # form.save()
                return redirect('home')


            except:
                form.add_error(None,'Ошибка добавления')
    else:
        form = AddPostForm()

    return render(request, 'commnets/add_com.html', {'form':form,'menu': menu, 'title': 'Добавление отзыва'})







def login(request):
    return HttpResponse('Авторизация')





def show_comment(request,post_slug):
    post = get_object_or_404(Comment,slug=post_slug)

    context = {'post': post,
               'menu': menu,
               'title': post.title,
               'cat_selected': post.cat_id,
               }

    return render(request,'commnets/post.html',context=context)




def show_category(request,cat_id):
    posts = Comment.objects.filter(cat_id=cat_id)


    if len(posts)==0:
        raise Http404
    context = {'posts': posts,
               'menu': menu,
               'title': 'Главная страница',
               'cat_selected': cat_id,
               }

    return render(request,'commnets/index.html',context=context)


def pageNotFound(request,exception):
    return HttpResponseNotFound('<h1>Страница не найдена </h1>')