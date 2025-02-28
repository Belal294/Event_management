import os
import django
import random
from faker import Faker
from django.contrib.auth import get_user_model
from events.models import Event, Participant, Category

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_management.settings')
django.setup()

def populate_db():
    fake = Faker()

    # Create categories
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.sentence()
    ) for _ in range(3)]
    print(f"Created {len(categories)} categories.")

    # Create events
    events = [Event.objects.create(
        name=fake.sentence(nb_words=4),
        description=fake.paragraph(),
        date=fake.date_this_year(),
        time=fake.time(),
        location=fake.city(),
        category=random.choice(categories)
    ) for _ in range(5)]
    print(f"Created {len(events)} events.")

    # Create participants
    User = get_user_model()  # Use custom user model
    participants = []
    for _ in range(10):
        username = fake.user_name()  # Generate a random username
        email = fake.email()
        password = "password123"

        user = User.objects.create_user(username=username, email=email, password=password)
        participant = Participant.objects.create(user=user, name=fake.name(), email=email)
        participants.append(user)

    print(f"Created {len(participants)} participants.")

    # Assign participants to events
    for event in events:
        selected_users = random.sample(participants, random.randint(1, 5))
        event.participants.set(selected_users)  # Associate users to the event

    print("Database populated successfully!")

if __name__ == "__main__":
    populate_db()
