from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'mt-2 p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-white',
                'placeholder': 'Post Title',
                'required': True,
            }),
            'content': forms.Textarea(attrs={
                'class': 'mt-2 p-3 border border-gray-300 dark:border-gray-600 rounded-lg bg-gray-50 dark:bg-gray-700 text-gray-800 dark:text-white',
                'placeholder': 'Write your post content here...',
                'rows': 6,
                'required': True,
            }),
        }
