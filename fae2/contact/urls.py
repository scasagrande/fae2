"""
Copyright 2014-2016 University of Illinois

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# abouts/urls.py
from django.conf.urls import url
from .views import ContactFormView
from .views import ResponseFormView
from .views import ResponsesView

urlpatterns = [ 
    url(r'^$', ContactFormView.as_view(),                      name='contact_form'),
    url(r'^respond/all/$',         ResponsesView.as_view(),    name='responses'),
    url(r'^respond/(?P<pk>\d+)/$', ResponseFormView.as_view(), name='response_form'),
]
