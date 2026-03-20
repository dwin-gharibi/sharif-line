from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from django.views import View
from django.forms import formset_factory
from django.db import transaction
from django.contrib import messages
import json

from .models import Survey, Question, Choice, Response, Answer, SelectedChoice
from .forms import SurveyForm, QuestionForm, ChoiceForm, BaseAnswerForm, ThankYouMessageForm

class SurveyListView(LoginRequiredMixin, ListView):
    model = Survey
    template_name = 'surveys/survey_list.html'
    context_object_name = 'surveys'
    
    def get_queryset(self):
        return Survey.objects.filter(creator=self.request.user)

class SurveyDetailView(LoginRequiredMixin, DetailView):
    model = Survey
    template_name = 'surveys/survey_detail.html'
    context_object_name = 'survey'
    
    def get_queryset(self):
        return Survey.objects.filter(creator=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['questions'] = self.object.questions.all().prefetch_related('choices')
        context['response_count'] = self.object.responses.count()
        return context

class SurveyCreateView(LoginRequiredMixin, CreateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    
    def form_valid(self, form):
        form.instance.creator = self.request.user
        self.object = form.save()
        if not self.object.slug:
            self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse('surveys:survey_edit', kwargs={'slug': self.object.slug})

class SurveyUpdateView(LoginRequiredMixin, UpdateView):
    model = Survey
    form_class = SurveyForm
    template_name = 'surveys/survey_form.html'
    
    def get_queryset(self):
        return Survey.objects.filter(creator=self.request.user)
    
    def get_success_url(self):
        return reverse('surveys:survey_detail', kwargs={'slug': self.object.slug})

class SurveyDeleteView(LoginRequiredMixin, DeleteView):
    model = Survey
    template_name = 'surveys/survey_confirm_delete.html'
    success_url = reverse_lazy('surveys:survey_list')
    
    def get_queryset(self):
        return Survey.objects.filter(creator=self.request.user)

class SurveyEditView(LoginRequiredMixin, DetailView):
    model = Survey
    template_name = 'surveys/survey_edit.html'
    context_object_name = 'survey'
    
    def get_queryset(self):
        return Survey.objects.filter(creator=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['question_form'] = QuestionForm()
        context['choice_form'] = ChoiceForm()
        context['questions'] = self.object.questions.all().prefetch_related('choices')
        return context

class QuestionCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        survey = get_object_or_404(Survey, slug=slug, creator=request.user)
        form = QuestionForm(request.POST)
        
        if form.is_valid():
            question = form.save(commit=False)
            question.survey = survey
            question.order = survey.questions.count() + 1
            question.save()
            
            if question.question_type in [Question.SINGLE_CHOICE, Question.MULTIPLE_CHOICE]:
                Choice.objects.create(question=question, text='گزینه 1', order=1)
                Choice.objects.create(question=question, text='گزینه 2', order=2)
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': question.id,
                    'text': question.text,
                    'type': question.get_question_type_display(),
                    'required': question.required,
                })
            
            return redirect('surveys:survey_edit', slug=survey.slug)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        
        messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
        return redirect('surveys:survey_edit', slug=survey.slug)

class QuestionUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk, survey__creator=request.user)
        form = QuestionForm(request.POST, instance=question)
        
        if form.is_valid():
            form.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': question.id,
                    'text': question.text,
                    'type': question.get_question_type_display(),
                    'required': question.required,
                })
            
            return redirect('surveys:survey_edit', slug=question.survey.slug)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        
        messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
        return redirect('surveys:survey_edit', slug=question.survey.slug)

class QuestionDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        question = get_object_or_404(Question, pk=pk, survey__creator=request.user)
        survey_slug = question.survey.slug
        question.delete()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        return redirect('surveys:survey_edit', slug=survey_slug)

class ChoiceCreateView(LoginRequiredMixin, View):
    def post(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk, survey__creator=request.user)
        form = ChoiceForm(request.POST)
        
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.order = question.choices.count() + 1
            choice.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': choice.id,
                    'text': choice.text,
                })
            
            return redirect('surveys:survey_edit', slug=question.survey.slug)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        
        messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
        return redirect('surveys:survey_edit', slug=question.survey.slug)

class ChoiceUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk):
        choice = get_object_or_404(Choice, pk=pk, question__survey__creator=request.user)
        form = ChoiceForm(request.POST, instance=choice)
        
        if form.is_valid():
            form.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'id': choice.id,
                    'text': choice.text,
                })
            
            return redirect('surveys:survey_edit', slug=choice.question.survey.slug)
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        
        messages.error(request, 'لطفاً خطاهای فرم را برطرف کنید.')
        return redirect('surveys:survey_edit', slug=choice.question.survey.slug)

class ChoiceDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        choice = get_object_or_404(Choice, pk=pk, question__survey__creator=request.user)
        survey_slug = choice.question.survey.slug
        choice.delete()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        return redirect('surveys:survey_edit', slug=survey_slug)

class TakeSurveyView(View):
    template_name = 'surveys/take_survey.html'
    
    def get(self, request, slug):
        survey = get_object_or_404(Survey, slug=slug, is_active=True)
        questions = survey.questions.all().prefetch_related('choices')
        
        forms = []
        forms_data = []
        
        for question in questions:
            form = BaseAnswerForm(question=question)
            forms.append(form)
            
            form_data = {
                'question_id': question.id,
                'label': question.text,
                'type': question.question_type,
                'required': question.required
            }
            forms_data.append(form_data)
        
        questions_data = []
        for question in questions:
            choices_data = []
            for choice in question.choices.all():
                choices_data.append({
                    'id': choice.id,
                    'text': choice.text
                })
            
            questions_data.append({
                'id': question.id,
                'text': question.text,
                'type': question.question_type,
                'required': question.required,
                'choices': choices_data
            })
        
        return render(request, self.template_name, {
            'survey': survey,
            'questions': questions,
            'questions_data': questions_data,
            'forms': forms,
            'forms_data': forms_data,
        })
    
    def post(self, request, slug):
        survey = get_object_or_404(Survey, slug=slug, is_active=True)
        questions = survey.questions.all().prefetch_related('choices')
        
        valid_forms = []
        all_valid = True
        
        for question in questions:
            form = BaseAnswerForm(request.POST, question=question)
            if not form.is_valid():
                all_valid = False
            valid_forms.append((question, form))
        
        if all_valid:
            with transaction.atomic():
                response = Response.objects.create(
                    survey=survey,
                    respondent_ip=request.META.get('REMOTE_ADDR')
                )
                
                for question, form in valid_forms:
                    answer = Answer.objects.create(
                        response=response,
                        question=question
                    )
                    
                    if question.question_type == Question.TEXT:
                        answer.text_answer = form.cleaned_data.get('text_answer', '')
                        answer.save()
                    elif question.question_type == Question.SINGLE_CHOICE:
                        choice_id = form.cleaned_data.get('choice')
                        if choice_id:
                            SelectedChoice.objects.create(
                                answer=answer,
                                choice=Choice.objects.get(id=int(choice_id))
                            )
                    elif question.question_type == Question.MULTIPLE_CHOICE:
                        choice_ids = form.cleaned_data.get('choices', [])
                        for choice_id in choice_ids:
                            SelectedChoice.objects.create(
                                answer=answer,
                                choice=Choice.objects.get(id=int(choice_id))
                            )
                    elif question.question_type == Question.RATING:
                        rating = form.cleaned_data.get('rating')
                        if rating:
                            answer.text_answer = rating
                            answer.save()
            
            return render(request, 'surveys/thank_you.html', {'survey': survey})
        
        forms = [form for _, form in valid_forms]
        
        forms_data = []
        for i, (question, _) in enumerate(valid_forms):
            form_data = {
                'question_id': question.id,
                'label': question.text,
                'type': question.question_type,
                'required': question.required
            }
            forms_data.append(form_data)
        
        questions_data = []
        for question in questions:
            choices_data = []
            for choice in question.choices.all():
                choices_data.append({
                    'id': choice.id,
                    'text': choice.text
                })
            
            questions_data.append({
                'id': question.id,
                'text': question.text,
                'type': question.question_type,
                'required': question.required,
                'choices': choices_data
            })
        
        return render(request, self.template_name, {
            'survey': survey,
            'questions': questions,
            'forms': forms,
            'forms_data': forms_data,
            'questions_data': questions_data
        })

class SurveyResponsesView(LoginRequiredMixin, DetailView):
    model = Survey
    template_name = 'surveys/survey_responses.html'
    context_object_name = 'survey'
    
    def get_queryset(self):
        return Survey.objects.filter(creator=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = self.object.responses.all().prefetch_related(
            'answers__selected_choices__choice', 'answers__question'
        )
        return context

class UpdateQuestionOrderView(LoginRequiredMixin, View):
    def post(self, request, slug):
        survey = get_object_or_404(Survey, slug=slug, creator=request.user)
        
        try:
            data = json.loads(request.body)
            question_ids = data.get('question_ids', [])
            
            with transaction.atomic():
                for order, question_id in enumerate(question_ids, start=1):
                    Question.objects.filter(
                        id=question_id, 
                        survey=survey
                    ).update(order=order)
            
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class DeleteIncompleteSurveyView(View):    
    def post(self, request, survey_id):
        try:
            if request.body:
                try:
                    json.loads(request.body)
                except json.JSONDecodeError:
                    pass
                    
            survey = Survey.objects.get(id=survey_id, creator=request.user)
            if not survey.slug:
                survey_title = survey.title
                survey.delete()
                messages.success(request, f'نظرسنجی ناقص "{survey_title}" با موفقیت حذف شد.')
                return JsonResponse({'status': 'success'})
            return JsonResponse({'status': 'error', 'message': 'این نظرسنجی ناقص نیست'}, status=400)
        except Survey.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'نظرسنجی پیدا نشد'}, status=404)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

class UpdateThankYouMessageView(LoginRequiredMixin, View):    
    def get(self, request, slug):
        survey = get_object_or_404(Survey, slug=slug, creator=request.user)
        form = ThankYouMessageForm(instance=survey)
        return render(request, 'surveys/thank_you_message_form.html', {
            'form': form,
            'survey': survey
        })
    
    def post(self, request, slug):
        survey = get_object_or_404(Survey, slug=slug, creator=request.user)
        form = ThankYouMessageForm(request.POST, instance=survey)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'پیام تشکر با موفقیت به‌روزرسانی شد.')
            return redirect('surveys:survey_edit', slug=survey.slug)
        
        return render(request, 'surveys/thank_you_message_form.html', {
            'form': form,
            'survey': survey
        })
