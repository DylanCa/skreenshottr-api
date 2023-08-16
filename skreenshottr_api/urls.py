"""
URL configuration for skreenshottr_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from allauth.socialaccount.views import signup
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from dj_rest_auth.registration.views import (
    SocialAccountListView,
    SocialAccountDisconnectView,
)
from dj_rest_auth.views import PasswordResetConfirmView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from rest_framework_nested import routers

from screenshots.authentication.social_adapters import GoogleLogin, GoogleConnect
from screenshots.viewsets.screenshot_viewset import ScreenshotViewSet
from screenshots.viewsets.tag_viewset import TagViewSet

router = routers.DefaultRouter()
router.register(r"tags", TagViewSet)
router.register(r"screenshots", ScreenshotViewSet)

screenshots_router = routers.NestedSimpleRouter(
    router, r"screenshots", lookup="screenshot"
)
screenshots_router.register(r"tags", TagViewSet, basename="screenshot-tags")

shown_urls = [
    # Administration #
    path("admin/", admin.site.urls),
    path("debug/", include("debug_toolbar.urls")),
    # Routers #
    path("", include(router.urls)),
    path("", include(screenshots_router.urls)),
    # Authentication & Social Endpoints #
    # Registration #
    path("register/", include("dj_rest_auth.registration.urls")),
    path("signup/", signup, name="socialaccount_signup"),
    path("login/google/", GoogleLogin.as_view(), name="google_login"),
    # User Endpoints #
    path("", include("dj_rest_auth.urls")),
    path(
        "user/social-accounts/connect/google/",
        GoogleConnect.as_view(),
        name="google_connect",
    ),
    path(
        "user/social-accounts/",
        SocialAccountListView.as_view(),
        name="socialaccount_connections",
    ),
    path(
        "user/social-accounts/<int:pk>/disconnect/",
        SocialAccountDisconnectView.as_view(),
        name="social_account_disconnect",
    ),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Skreenshottr API",
        default_version="v1",
        description="Schema for Skreenshottr API",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=shown_urls,
)

urlpatterns = shown_urls + [
    path(
        "password/reset/confirm/<str:uidb64>/<str:token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    # Swagger #
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
