from django.urls import NoReverseMatch

from rest_framework.routers import APIRootView, DefaultRouter
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.request import Request


class ApiRootViewWithProfile(APIRootView):
    def get(self, request: Request, *args, **kwargs):
        ret = {}
        if request.user.is_authenticated:
            ret['profile'] = reverse('user-detail', request=request, args=[request.user.id])
        else:
            ret['register'] = reverse('register', request=request)
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ':' + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get('format')
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue

        return Response(ret)
    
    def get_view_name(self):
        return "Api Root View"


class Router(DefaultRouter):
    APIRootView = ApiRootViewWithProfile