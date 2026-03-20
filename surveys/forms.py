from django import forms
from .models import Survey, Question, Choice, Response, Answer, SelectedChoice
from django_summernote.widgets import SummernoteWidget

class SurveyForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['title', 'description', 'is_active', 'custom_thank_you_message']
        labels = {
            'title': 'عنوان نظرسنجی',
            'description': 'توضیحات',
            'is_active': 'فعال',
            'custom_thank_you_message': 'پیام تشکر',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'عنوان نظرسنجی را وارد کنید'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'توضیحات نظرسنجی را وارد کنید'}),
            'custom_thank_you_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'پیام تشکر پس از تکمیل نظرسنجی را وارد کنید'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
     

class ThankYouMessageForm(forms.ModelForm):
    class Meta:
        model = Survey
        fields = ['custom_thank_you_message']
        labels = {
            'custom_thank_you_message': 'متن پیام تشکر',
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text', 'question_type', 'required']
        labels = {
            'text': 'متن سوال',
            'question_type': 'نوع سوال',
            'required': 'پاسخ اجباری است',
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'متن سوال را وارد کنید'}),
            'question_type': forms.Select(attrs={'class': 'form-control'}),
            'required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text']
        labels = {
            'text': 'متن گزینه',
        }
        widgets = {
            'text': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'متن گزینه را وارد کنید'}),
        }
        help_texts = {
            'text': 'متن گزینه که به کاربر نمایش داده می‌شود',
        }

class BaseAnswerForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        
        if self.question.question_type == Question.TEXT:
            self.fields['text_answer'] = forms.CharField(
                label=self.question.text,
                required=self.question.required,
                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'پاسخ خود را اینجا وارد کنید'})
            )
        elif self.question.question_type == Question.SINGLE_CHOICE:
            choices = [(choice.id, choice.text) for choice in self.question.choices.all()]
            self.fields['choice'] = forms.ChoiceField(
                label=self.question.text,
                required=self.question.required,
                choices=choices,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
            )
        elif self.question.question_type == Question.MULTIPLE_CHOICE:
            choices = [(choice.id, choice.text) for choice in self.question.choices.all()]
            self.fields['choices'] = forms.MultipleChoiceField(
                label=self.question.text,
                required=self.question.required,
                choices=choices,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
            )
        elif self.question.question_type == Question.RATING:
            RATING_CHOICES = [(str(i), str(i)) for i in range(1, 6)]
            self.fields['rating'] = forms.ChoiceField(
                label=self.question.text,
                required=self.question.required,
                choices=RATING_CHOICES,
                widget=forms.RadioSelect(attrs={'class': 'form-check-input rating'})
            ) 