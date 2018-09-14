from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from blog.models import Post
from tagging.models import Tag, TaggedItem
from tagging.views import TaggedObjectList

from django.views.generic.edit import FormView
from blog.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from mysite.views import LoginRequiredMixin
# Create your views here.

#--- ListView
class PostLV(LoginRequiredMixin, ListView) :
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts' #default name = object_list
    paginate_by = 2 # the number of objects in one page

class PostTOL(LoginRequiredMixin, TaggedObjectList):
    model = Post
    template_name = 'tagging/tagging_post_list.html'

#--- DetailView
class PostDV(LoginRequiredMixin, DetailView):
    model = Post
    #unless defined, the defaults values are used.

#-- ArchiveView added
class PostAV(LoginRequiredMixin, ArchiveIndexView):
    model = Post
    date_field = 'modify_date'

class PostYAV(YearArchiveView):
    model = Post
    date_field = 'modify_date'
    make_object_list = True
    #if make_object_list is true, the objects list of that year will be transmitted to the corresponding template

class PostMAV(LoginRequiredMixin, MonthArchiveView):
    model = Post
    date_field = 'modify_date'

class PostDAV(LoginRequiredMixin, DayArchiveView):
    model = Post
    date_field = 'modify_date'

class PostTAV(LoginRequiredMixin, TodayArchiveView):
    model = Post
    date_field = 'modify_date'

#-- TemplateView
class TagTV(TemplateView):
    template_name = 'tagging/tagging_cloud.html'

#-- FormView
class SearchFormView(LoginRequiredMixin, FormView):
    form_class = PostSearchForm
    template_name = 'blog/post_search.html'

    def form_valid(self, form):
        schWord = '%s' % self.request.POST['search_word']
        post_list = Post.objects.filter(Q(title__icontains=schWord) | Q(description__icontains=schWord) | Q(content__icontains=schWord)).distinct()
        context = {}
        context['form'] = form
        context['search_term'] = schWord
        context['object_list'] = post_list
        return render(self.request, self.template_name, context)

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    initial = {'slug': 'auto-filling-do-not-input'}
    success_url = reverse_lazy('blog:index')


    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PostCreateView, self).form_valid(form)

class PostChangeLV(LoginRequiredMixin, ListView):
    template_name = 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'slug', 'description', 'content', 'tag']
    success_url = reverse_lazy('blog:index')

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog:index')
