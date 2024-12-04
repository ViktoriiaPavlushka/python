from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from .forms import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.views.generic import FormView
from django.shortcuts import render, redirect
from .forms import TicketForm

MODEL_MAP = {
    "film": Film,
    "director": Director,
    "genre": Genre,
    "hall": Hall,
    "seat": Seat,
    "price" : Price,
    "session": Session,
}

FORM_MAP = {
    "film": FilmForm,
    "director": DirectorForm,
    "genre": GenreForm,
    "hall": HallForm,
    "seat": SeatForm,
    "price" : PriceForm,
    "session": SessionForm,
}

def home(request):
    return render(request, 'home.html')

class DynamicListView(ListView):
    template_name = "list.html"

    def get_queryset(self):
        model_name = self.kwargs.get("model_name")
        model = MODEL_MAP.get(model_name.lower())
        if not model:
            raise ValueError(f"Model '{model_name}' not found.")
        return model.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get("model_name")
        model = MODEL_MAP[model_name.lower()]
        context["model_name"] = model_name.capitalize()
        context["field_names"] = [field.name for field in model._meta.fields]
        context["items"] = self.object_list
        return context


class DynamicDetailView(DetailView):
    template_name = "detail.html"

    def get_object(self):
        model_name = self.kwargs.get("model_name")
        model = MODEL_MAP.get(model_name.lower())
        if not model:
            raise ValueError(f"Model '{model_name}' not found.")
        return get_object_or_404(model, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get("model_name")
        model = MODEL_MAP[model_name.lower()]
        context["model_name"] = model_name.capitalize()
        context["field_names"] = [field.name for field in model._meta.fields]
        context["item"] = self.object
        return context


class DynamicCreateView(CreateView):
    template_name = "form.html"

    def get_form_class(self):
        model_name = self.kwargs.get("model_name")
        form_class = FORM_MAP.get(model_name.lower())
        if not form_class:
            raise ValueError(f"Form for model '{model_name}' not found.")
        return form_class

    def form_valid(self, form):
        # Save the object and get the instance
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get("model_name")
        context["model_name"] = model_name.capitalize()
        context["form_title"] = f"Add New {model_name.capitalize()}"
        return context

    def get_success_url(self):
        model_name = self.kwargs.get("model_name")
        # Redirect to the detail page of the newly created object
        return reverse_lazy("detail", kwargs={"model_name": model_name.lower(), "pk": self.object.pk})



class DynamicUpdateView(UpdateView):
    template_name = "form.html"

    def get_form_class(self):
        model_name = self.kwargs.get("model_name")
        form_class = FORM_MAP.get(model_name.lower())
        if not form_class:
            raise ValueError(f"Form for model '{model_name}' not found.")
        return form_class

    def get_object(self):
        model_name = self.kwargs.get("model_name")
        model = MODEL_MAP.get(model_name.lower())
        if not model:
            raise ValueError(f"Model '{model_name}' not found.")
        return get_object_or_404(model, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get("model_name")
        context["model_name"] = model_name.capitalize()
        context["form_title"] = f"Edit {model_name.capitalize()}"
        return context

    def get_success_url(self):
        model_name = self.kwargs.get("model_name")
        return reverse_lazy("list", kwargs={"model_name": model_name.lower()})


class DynamicDeleteView(DeleteView):
    template_name = "delete.html"

    def get_object(self):
        model_name = self.kwargs.get("model_name")
        model = MODEL_MAP.get(model_name.lower())
        if not model:
            raise ValueError(f"Model '{model_name}' not found.")
        return get_object_or_404(model, pk=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        model_name = self.kwargs.get("model_name")
        context["model_name"] = model_name.capitalize()
        return context

    def get_success_url(self):
        model_name = self.kwargs.get("model_name")
        return reverse_lazy("list", kwargs={"model_name": model_name.lower()})


def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TicketForm()
    return render(request, 'create_ticket.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = Login(request.POST)
        if form.is_valid():
            phoneNumber = form.cleaned_data['phoneNumber']
            password = form.cleaned_data['password']
            user = authenticate(phoneNumber=phoneNumber, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'login.html', {'form': Login()})

def registration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            first = form.cleaned_data['name']
            last = form.cleaned_data['lastName']
            year = form.cleaned_data['yearOfBirth']
            phone = form.cleaned_data['phoneNumber']
            password = form.cleaned_data['password']
            hash_pass = make_password(password)
            User.objects.create(name=first, lastName=last, yearOfBirth= year , phoneNumber=phone, password=hash_pass)
            return redirect('home')
    else:
        form = Registration()
    return render(request, 'registration.html', {'form': form})




