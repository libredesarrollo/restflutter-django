from django.contrib import admin
from django.http import HttpResponseRedirect
from .models import Group, Button, Image, Chip, Text, Mix, Behavior, Note


# Register your models here.

class BehaviorCustomForm(admin.ModelAdmin):
    change_form_template = 'admin/behavior_change_form.html'
    tag_content_type = "button__id"

    def change_view(self, request, object_id, form_url='', extra_content=None):
        extra_content = extra_content or {}
        
        extra_content["content_1"] = extra_content["content_2"] = extra_content["behavioral_model"] = ""
        extra_content["object_id"] = object_id

        behavior = Behavior.objects.filter(**{self.tag_content_type: object_id}).first()

        if behavior:
            extra_content["content_1"] = behavior.content_1
            extra_content["content_2"] = behavior.content_2
            extra_content["behavioral_model"] = behavior.behavioral_model
        
        return super().change_view(request, object_id, form_url, extra_content)

  
    def response_change(self, request, obj=None):

        #print(obj)

        if "content_1" in request.POST:

            behavior = Behavior.objects.filter(**{self.tag_content_type: obj.id}).first()

            if request.POST.get('content_1') == "" and behavior:
                #self.message_user(request,"Contenido 1 tiene que set distinto de vacio")
                behavior.delete()
                self.message_user(request,"Comportamiento eliminado con éxito")
                return HttpResponseRedirect(".")

            
            if not behavior:
                behavior = Behavior()

            behavior.content_1 = request.POST.get('content_1')
            behavior.content_2 = request.POST.get('content_2')
            behavior.behavioral_model = request.POST.get('behavioral_model')
            behavior.content_object = obj

            behavior.save()

        return super().response_change(request, obj)

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    change_form_template = 'admin/mix_change_form.html'

    def change_view(self, request, object_id, form_url='', extra_content=None):
        extra_content = extra_content or {}
        
        extra_content["object_id"] = object_id
        extra_content["buttons"] = Button.objects.all()
        extra_content["images"] = Image.objects.all()
        extra_content["chips"] = Chip.objects.all()
        extra_content["texts"] = Text.objects.all()
        return super().change_view(request, object_id, form_url, extra_content)
    
    def response_change(self, request, obj=None):

        #print(obj)

        if "orden" in request.POST:
            mix = Mix()
            mix.widget = request.POST.get('widget').split("_")[0]
            mix.widget_id = request.POST.get('widget').split("_")[1]
            mix.orden = request.POST.get('orden')
            mix.group = obj
            mix.save()

            #self.message_user(request,"Hubo un error")
            #return HttpResponseRedirect(".")

        return super().response_change(request, obj)





@admin.register(Button)
class ButtonAdmin(BehaviorCustomForm):
    pass

@admin.register(Image)
class ImageAdmin(BehaviorCustomForm):
    tag_content_type="image__id"

@admin.register(Chip)
class ChipAdmin(BehaviorCustomForm):
    tag_content_type="chip__id"

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    pass
@admin.register(Mix)
class MixAdmin(admin.ModelAdmin):
    pass
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass