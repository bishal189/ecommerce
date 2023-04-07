from django import forms
from .models import Account


class ResitrationForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter password'
    }))
    confrim_password=forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Confrim password'
    }))
    class Meta:
        model=Account
        fields=['first_name','last_name','email','phone_number','password']

    def __init__(self,*args,**kwargs):
        super(ResitrationForm,self).__init__(*args,**kwargs)
        self.fields ['first_name'].widget.attrs['placeholder']='Enter first name'      
        self.fields ['last_name'].widget.attrs['placeholder']='Enter last name'      
        self.fields ['email'].widget.attrs['placeholder']='Enter email Address'      
        self.fields ['phone_number'].widget.attrs['placeholder']='Enter phone number'      
     
        for field in self.fields:
            self.fields [field].widget.attrs['class']='form-control'





    def clean(self):
        cleaned_data=super(ResitrationForm,self).clean()
        password=cleaned_data.get('password')
        confrim_password=cleaned_data.get('confrim_password')


        if password!=confrim_password:
            raise forms.ValidationError(
                'password does not match!.'
            )              