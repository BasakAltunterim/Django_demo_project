
from django.contrib import admin 
from .models import Amenity, Manager, Property  



class ManagerAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'email')

class PropertyAdmin(admin.ModelAdmin):


    list_display = ('title', 'price', 'address', 'manager','availability') 
    list_editable = ('price',) 
    search_fields = ('title', 'address')
    list_filter = ('price', 'manager')   
    filter_horizontal = ('amenities',)  
    readonly_fields = ('bedrooms', 'bathrooms')  
    autocomplete_fields = ('manager',)  

    actions=('make_available','make_unvailable','raise_rent')



    @admin.action(description="make select properties available")
    def make_available(self,request,queryset):
        queryset.update(availability=True) 

   
    @admin.action(description="Raise rent on selected properties by 10 percent")
    def raise_rent(self, request, queryset):
        for obj in queryset:
            obj.price *= 10
            obj.save()



admin.site.register(Amenity) 
admin.site.register(Manager, ManagerAdmin) 
admin.site.register(Property, PropertyAdmin)
