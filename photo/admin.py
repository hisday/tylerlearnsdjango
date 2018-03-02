from django.contrib import admin
from photo.models import Album, Photo

class PhotoInLine(admin.StackedInline):
    model = Photo
    extra = 2

class AlbumAdmin(admin.ModelAdmin):
    inlines = [PhotoInLine]
    list_display = ('name', 'description')

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'upload_date')

admin.site.register(Album, AlbumAdmin)
admin.site.register(Photo, PhotoAdmin)
