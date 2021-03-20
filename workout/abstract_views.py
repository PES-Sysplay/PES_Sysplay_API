from abc import ABC

from django.shortcuts import render
from django.views.generic import TemplateView


class FormView(ABC, TemplateView):
    form_class = None
    initial = {}

    def set_form(self, form):
        pass

    def get_model_object(self):
        return None

    def get_context_data(self, model_object=None, **kwargs):
        context = super().get_context_data(**kwargs)
        if not model_object:
            model_object = self.get_model_object()
        if model_object:
            form = self.form_class(instance=model_object)
        else:
            form = self.form_class(initial=self.initial)
        self.set_form(form)
        context.update({'form': form})
        return context

    def post(self, request, *args, **kwargs):
        model_object = self.get_model_object()
        form = self.form_class(request.POST, request.FILES, instance=model_object)
        if form.is_valid():
            model_object = form.save()
            return self.get_success_redirect(model_object=model_object)
        context = self.get_context_data(model_object=model_object)
        context.update({'form': form})
        return render(request=request, template_name=self.template_name, context=context)

    def get_success_redirect(self, model_object):
        return None
