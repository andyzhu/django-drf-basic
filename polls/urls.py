# from polls.apiviews import PollList
from django.urls import path, re_path

from .views import polls_detail, polls_list
from .apiviews import ChoiceList, CreateVote, LoginView, PollViewSet, UserCreate 
# #, PollList, PollDetail
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

router = DefaultRouter()
router.register('polls', PollViewSet, basename='polls')

urlpatterns = [
    # path('polls/', polls_list, name='polls_list'),
    # path('polls/<int:pk>/', polls_detail, name='polls_detail'),
    # path('polls/', PollList.as_view(), name='polls_list'),
    # path('polls/<int:pk>/', PollDetail.as_view(), name='poll_detail'),
    # path('choices/', ChoiceList.as_view(), name='choices_list'),
    path('polls/<int:id>/choices/', ChoiceList.as_view(), name='choice_list'),
    # path('vote', CreateVote.as_view(), name='create_vote'),
    path('polls/<int:poll_pk>/choices/<int:choice_pk>/vote', CreateVote.as_view(), name='create_vote'),
    path('users/', UserCreate.as_view(), name='user_create'),
    path('login/', LoginView.as_view(), name='login'),
    path('docs/', include_docs_urls(title='Polls API')),

]

urlpatterns += router.urls

schema_view = get_schema_view(
    openapi.Info(
        title = 'Polls API',
        default_version= 'v1',
        description= " Polls API ",
        terms_of_service= 'https://www.google.com/policies/terms/',
        contact=openapi.Contact(email="contact@pollsapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny]
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]