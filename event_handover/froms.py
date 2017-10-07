from django.forms import ModelForm


class CommentChangeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentChangeForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and hasattr(instance, "user"):
                # self.fields['user'].widget.attrs['disabled'] = 'disabled'
                # self.fields['content'].widget.attrs['disabled'] = 'disabled'
                pass

    def clean_user(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.user
        else:
            return self.cleaned_data['user']


class CommentAddForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentAddForm, self).__init__(*args, **kwargs)
