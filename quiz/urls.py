from django.urls import path
from graphene_django.views import GraphQLView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from django.contrib.auth import views as auth_views
from quiz.middleware import GraphQLRateLimitMiddleware
from django_ratelimit.decorators import ratelimit
from .views import EmailAPIView, FriendRequestCreateAPIView,  FriendRequestListCreateAPIView, LoginView, RecievedRequestAcceptedListAPIView, RecivedRequestPendingListAPIView, SentRequestAcceptedListAPIView, SentRequestPendingListAPIView, SignUpView, UserSearchAPIView, UserkapDetailAPIView, UserkapListCreateAPIView
from django.views.decorators.csrf import csrf_exempt
from .middleware import static_auth_required
urlpatterns = [
    # Only a single URL to access GraphQL
    # path('graphql/',static_auth_required(csrf_exempt(GraphQLView.as_view(graphiql=True)))),
    
    
    # path('send-message/', SendMessageAPIView.as_view(), name='send_message'),

    # Other URLs...
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    # path('friend-requests/', FriendRequestCreateAPIView.as_view(), name='friend-request-create'),
    path('friend-requests-all/', FriendRequestListCreateAPIView.as_view(), name='friend-request-list'),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path('send-email/', EmailAPIView.as_view(), name='send_email'),
    path('userkap/', UserkapListCreateAPIView.as_view(), name='userkap-list-create'),
    path('userkap/<int:pk>/', UserkapDetailAPIView.as_view(), name='userkap-detail'),
    path('sent-requests/accepted/', SentRequestAcceptedListAPIView.as_view(), name='sent-requests-accepted'),
    path('sent-requests/pending/', SentRequestPendingListAPIView.as_view(), name='sent-requests-pending'),
    path('received-requests/accepted/', RecievedRequestAcceptedListAPIView.as_view(), name='received-requests-accepted'),
    path('received-requests/pending/', RecivedRequestPendingListAPIView.as_view(), name='received-requests-pending'),
    path('search/', UserSearchAPIView.as_view(), name='user-search'),
    
]

    # Add other URLs as needed
    
