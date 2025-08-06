from django import forms


from restaurent.models import *

class StoreCategoryForm(forms.ModelForm):

    class Meta:
        model = StoreCategory
        fields = ['name', 'image']



    widgets={
        'name':forms.widgets.TextInput(attrs={"class":"form-control" , "placeholder":"category name"}),
        'image':forms.widgets.FileInput(attrs={"class":"form-control"})
    }


class StoreForm(forms.ModelForm):
    class Meta:
        model = Store
        fields = ['name', 'category', 'image', 'short_descritpion', 'rating', 'time']
        widgets = {
            'name': forms.TextInput(attrs={
                "class": "form-control","placeholder": "Store name"}),

            'category': forms.Select(attrs={"class": "form-control"}),

            'image': forms.FileInput(attrs={"class": "form-control"}),

            'short_descritpion': forms.TextInput(attrs={"class": "form-control","placeholder": "Short description"}),

            'rating': forms.NumberInput(attrs={"class": "form-control","placeholder": "Rating out of 5",}),

            'time': forms.NumberInput(attrs={"class": "form-control","placeholder": "Estimated time in minutes"}),
        }



        
class FoodCategoryForm(forms.ModelForm):

    class Meta:
        model = FoodCategory
        fields = ['store','name']



    widgets={
        'store':forms.widgets.TextInput(attrs={"class":"form-control" , "placeholder":"store"}),
       
    
        'name':forms.widgets.TextInput(attrs={"class":"form-control" , "placeholder":" foodcategory name"}),
       
    }



    
class FoodItemForm(forms.ModelForm):
    class Meta:
        model = FoodItem
        fields = ['store', 'category', 'name', 'image', 'price', 'is_veg']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'store': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'is_veg': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }