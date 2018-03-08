#from django.shortcuts import render
from django.views.generic import ListView, DetailView
from photo.models import Album, Photo

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from mysite.views import LoginRequiredMixin


class AlbumLV(ListView):
    model = Album

class AlbumDV(DetailView):
    model = Album

class PhotoDV(DetailView):
    model = Photo

#photo ---
class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['album', 'title', 'image', 'description']
    success_url = reverse_lazy('photo:index')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super(PhotoCreateView, self).form_valid(form)

class PhotoChangeLV(LoginRequiredMixin, ListView):
    template_name = 'photo/photo_change_list.html'

    def get_queryset(self):
        return Photo.objects.filter(owner=self.request.user)

class PhotoUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    fields = ['album', 'title', 'image', 'description']
    success_url = reverse_lazy('photo:index')

class PhotoDeleteView(LoginRequiredMixin, DeleteView):
    model = Photo
    success_url = reverse_lazy('photo:index')

#album --
class AlbumChangeLV(LoginRequiredMixin, ListView):
    template_name = 'photo/album_change_list.html'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user)

class AlbumDeleteView(LoginRequiredMixin, DeleteView):
    model = Album
    success_url = reverse_lazy('photo:index')


#-- inline form set
from django.shortcuts import redirect
from photo.forms import PhotoInlineFormSet

class AlbumPhotoCV(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['name', 'description']
    template_name = 'photo/album_form.html' #can be commented out. _form suffix is default template of CreateView

    def get_context_data(self, **kwargs):
        context = super(AlbumPhotoCV, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES) #request.FILES for file uploading
        else:
            context['formset'] = PhotoInlineFormSet() #Get request
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset']
        for photoform in formset:
            photoform.instance.owner = self.request.user
        if formset.is_valid():
            self.object = form.save() #save album
            formset.instance = self.object #ForeignKey를 방금 save한 앨범으로 세팅하는 듯...
            formset.save() #save photos
            return redirect(self.object.get_absolute_url()) #album 상세 페이지로 이동
        else:
            return self.render_to_response(self.get_context_data(form=form)) #유효하지 않은면 다시 출력

class AlbumPhotoUV(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['name', 'description']
    template_name = 'photo/album_form.html'

    def get_context_data(self, **kwargs):
        context = super(AlbumPhotoUV, self).get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = PhotoInlineFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['formset'] = PhotoInlineFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        form.instance.owner = self.request.user
        context = self.get_context_data()
        formset = context['formset'] #photo
        for photoform in formset:
            photoform.instance.owner = self.request.user
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save() #save record to table
            return redirect(self.object.get_absolute_url())
        else:
            return self.render_to_response(self.get_context_data(form=form))
