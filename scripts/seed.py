import os
import sys
import django
import random
from dotenv import load_dotenv
from faker import Faker

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

# Importar modelos
from customer_mgmt.models import SalesPerson, Company, Customer, Interaction
fake = Faker()

# Importar Variables de entorno
load_dotenv()
PASSWORD = os.getenv("PASSWORD_USERS")

def run():
    print("Eliminando datos anteriores...")
    Interaction.objects.all().delete()
    Customer.objects.all().delete()
    Company.objects.all().delete()
    SalesPerson.objects.all().delete()
    print(PASSWORD)
    print("Creando 3 representantes de ventas...")
    reps = []
    for i in range(3):
        email = fake.email(domain='crm.com')
        display_name = fake.name() +' '+ fake.last_name()        
        rep = SalesPerson.objects.create_user(
            email=f'{email}',
            password=PASSWORD,
            name=f'{display_name}'
        )
        reps.append(rep)

    print("Creando 20 compañías...")
    companies = []
    for _ in range(20):
        companie = Company.objects.create(name=fake.company())
        companies.append(companie)

    print("Creando 1000 clientes...")
    customers = []
    for _ in range(1000):
        display_name = fake.name() + fake.last_name() 
        customer = Customer.objects.create(
            name=display_name,
            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
            company=random.choice(companies),
            assigned_sales_person=random.choice(reps)
        )
        customers.append(customer)

    print("Creando 500 interacciones por cliente...")
    interaction_types = ['Call', 'Email', 'SMS', 'Facebook', 'WhatsApp']
    bulk = []
    for i, customer in enumerate(customers):
        for _ in range(500):
            bulk.append(Interaction(
                customer=customer,
                interaction_type=random.choice(interaction_types),
                date=fake.date_time_between(start_date='-2y', end_date='now')
            ))
        if (i + 1) % 10 == 0:
            print(f"    {i+1}/1000 clientes procesados")

    print("🚀 Guardando interacciones (puede tardar)...")
    Interaction.objects.bulk_create(bulk)
    print("✅ Seed completo.")

if __name__ == '__main__':
    run()