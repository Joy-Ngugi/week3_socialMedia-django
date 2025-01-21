from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Comment, Post

class RegistrationForm(UserCreationForm):
 email = forms.EmailField()
 class Meta:
  model = User
  fields = ['username', 'email', 'password1', 'password2']
  

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
    
    bio = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4',
            'rows': 4,
            'placeholder': 'Tell us about yourself'
        }),
        required=False
    )
    
    profile_picture = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'block w-full text-sm text-gray-500 file:border file:border-gray-300 file:bg-gray-100 file:px-4 file:py-2 file:rounded-lg hover:file:bg-gray-200 mb-4',
            'accept': 'image/*'
        }),
        required=False
    )
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  
        super().__init__(*args, **kwargs)
        if user:
            self.fields['bio'].initial = user.profile.bio  # Pre-fill bio
            self.fields['profile_picture'].initial = user.profile.profile_picture  # Pre-fill profile picture if it exists

    def save(self, commit=True):
        profile = super().save(commit=False)
        if commit:
            profile.save()
        return profile

    

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content', 'image']

    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write something...', 'class': 'w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-1 focus:ring-indigo-500'}))
    image = forms.ImageField(required=False)
    author = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.HiddenInput(), required=False)

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("This field cannot be empty.")
        return content
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].widget.attrs.update({
            'rows': 3,
            'placeholder': 'Add a comment...',
            'class': 'w-full p-3 border border-gray-300 rounded-lg focus:ring-indigo-500',
        })
        self.fields['content'].label = ''

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if not content:
            raise forms.ValidationError("This field cannot be empty.")
        return content