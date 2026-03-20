from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.SurveyListView.as_view(), name='survey_list'),
    path('create/', views.SurveyCreateView.as_view(), name='survey_create'),
    path('<slug:slug>/', views.SurveyDetailView.as_view(), name='survey_detail'),
    path('<slug:slug>/edit/', views.SurveyEditView.as_view(), name='survey_edit'),
    path('<slug:slug>/update/', views.SurveyUpdateView.as_view(), name='survey_update'),
    path('<slug:slug>/delete/', views.SurveyDeleteView.as_view(), name='survey_delete'),
    path('<slug:slug>/responses/', views.SurveyResponsesView.as_view(), name='survey_responses'),
    path('<slug:slug>/take/', views.TakeSurveyView.as_view(), name='take_survey'),
    path('<slug:slug>/thank-you-message/', views.UpdateThankYouMessageView.as_view(), name='update_thank_you_message'),
    path('<slug:slug>/questions/add/', views.QuestionCreateView.as_view(), name='question_create'),
    path('<slug:slug>/questions/update-order/', views.UpdateQuestionOrderView.as_view(), name='update_question_order'),
    path('questions/<int:pk>/update/', views.QuestionUpdateView.as_view(), name='question_update'),
    path('questions/<int:pk>/delete/', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('questions/<int:question_pk>/choices/add/', views.ChoiceCreateView.as_view(), name='choice_create'),
    path('choices/<int:pk>/update/', views.ChoiceUpdateView.as_view(), name='choice_update'),
    path('choices/<int:pk>/delete/', views.ChoiceDeleteView.as_view(), name='choice_delete'),
    path('<int:survey_id>/delete-incomplete/', views.DeleteIncompleteSurveyView.as_view(), name='delete_incomplete_survey'),
] 