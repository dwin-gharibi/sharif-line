from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
import uuid

class Survey(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='surveys')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    is_active = models.BooleanField(default=True)
    custom_thank_you_message = models.TextField(
        blank=True, 
        null=True,
        verbose_name="پیام تشکر شخصی‌سازی شده",
        help_text="متن شخصی‌سازی شده‌ای که می‌خواهید بعد از پاسخ به نظرسنجی نمایش داده شود."
    )
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or 'survey'
            self.slug = base_slug
            counter = 1
            while Survey.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}" if counter < 5 else f"{base_slug}-{uuid.uuid4().hex[:8]}"
                counter += 1
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('surveys:survey_detail', kwargs={'slug': self.slug})
    
    def get_share_url(self):
        return reverse('surveys:take_survey', kwargs={'slug': self.slug})
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Question(models.Model):
    TEXT = 'text'
    SINGLE_CHOICE = 'single'
    MULTIPLE_CHOICE = 'multiple'
    RATING = 'rating'
    
    QUESTION_TYPES = [
        (TEXT, 'پاسخ متنی'),
        (SINGLE_CHOICE, 'تک انتخابی'),
        (MULTIPLE_CHOICE, 'چند انتخابی'),
        (RATING, 'امتیازدهی'),
    ]
    
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    text = models.CharField(max_length=500)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES, default=TEXT)
    required = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.text} ({self.get_question_type_display()})"

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    text = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.text

class Response(models.Model):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    created_at = models.DateTimeField(auto_now_add=True)
    respondent_ip = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return f"پاسخ به {self.survey.title} در {self.created_at}"

class Answer(models.Model):
    response = models.ForeignKey(Response, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text_answer = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"پاسخ به {self.question.text}"

class SelectedChoice(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='selected_choices')
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, related_name='selections')
    
    def __str__(self):
        return f"{self.choice.text}"
