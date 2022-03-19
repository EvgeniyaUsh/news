from django import forms


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)
    email = forms.EmailField()
    name = forms.CharField()
    website = forms.URLField(required=False)
