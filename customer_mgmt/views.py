from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from customer_mgmt.models import Customer, Interaction
from django.db import models
from django.db.models import OuterRef, Subquery

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Correo o contraseña incorrectos')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def redirect_to_login(request, exception=None):
    return redirect('login')

@login_required
def dashboard(request):
    name_filter = request.GET.get('nombre', '')
    birthday_filter = request.GET.get('cumpleanos', '')
    sort_by = request.GET.get('orden', '')

    customers = Customer.objects.all().select_related('company', 'assigned_sales_person')
    
    last_interaction = Interaction.objects.filter(
        customer=OuterRef('pk')
    ).order_by('-date')

    # Incluye la fecha y el tipo de interacción
    customers = customers.annotate(
        last_interaction_date=Subquery(last_interaction.values('date')[:1]),
        last_interaction_type=Subquery(last_interaction.values('interaction_type')[:1]),
    )

    if name_filter:
        customers = customers.filter(name__icontains=name_filter)

    if birthday_filter:
        try:
            month, day = map(int, birthday_filter.split('-'))
            customers = customers.filter(birth_date__month=month, birth_date__day=day)
        except ValueError:
            pass

    # Ordenamiento
    if sort_by == 'nombre':
        customers = customers.order_by('name')
    elif sort_by == 'empresa':
        customers = customers.order_by('company__name')
    elif sort_by == 'cumpleanos':
        customers = customers.order_by('birth_date')
    elif sort_by == 'ultima_interaccion':
        customers = customers.order_by('-last_interaction_date')


    return render(request, 'dashboard.html', {
        'user': request.user,
        'customers': customers,
        'name_filter': name_filter,
        'birthday_filter': birthday_filter,
        'sort_by': sort_by,
    })