from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.generic import TemplateView, View
from .forms import CreateUserForm
from django.template.context_processors import csrf
from crispy_forms.utils import render_crispy_form
from django.contrib.auth import login


class HomePage(TemplateView):

    template_name = 'record/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.__setitem__('form', CreateUserForm)
        context.__setitem__('request', self.request)
        return context


class CreateUserView(View):

    user_form = CreateUserForm

    def get(self, request, *args, **kwargs):
        form = self.user_form()
        return render(request, 'record/index.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form_user = self.user_form(request.POST)
        if form_user.is_valid():
            user = form_user.save()
            login(request, user)
            # template = render(request, 'record/profile.html')
            # return template
            return HttpResponse('Вы успешно зарегистрировались')

        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form_user, context=ctx)
        return HttpResponse(form_html)

