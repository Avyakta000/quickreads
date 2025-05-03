from django.core.management.base import BaseCommand
from blog.models import Category, Topic

class Command(BaseCommand):
    help = "Populate the database with sample categories and topics"

    def handle(self, *args, **kwargs):
        # Sample categories
        categories = [
            {"name": "Technology"},
            {"name": "Health"},
            {"name": "Education"},
            {"name": "Travel"},
            {"name": "Food"},
            {"name": "Finance"},
            {"name": "Lifestyle"},
            {"name": "Entertainment"},
            {"name": "Sports"},
            {"name": "Science"},
        ]

        # Sample topics
        topics = [
            {"name": "Artificial Intelligence"},
            {"name": "Mental Health"},
            {"name": "Online Learning"},
            {"name": "Adventure Travel"},
            {"name": "Vegan Recipes"},
            {"name": "Cryptocurrency"},
            {"name": "Minimalism"},
            {"name": "Movies and TV Shows"},
            {"name": "Fitness Tips"},
            {"name": "Space Exploration"},
            {"name": "Machine Learning"},
            {"name": "Nutrition"},
            {"name": "E-Learning Platforms"},
            {"name": "Cultural Tourism"},
            {"name": "Dessert Recipes"},
            {"name": "Stock Market"},
            {"name": "Work-Life Balance"},
            {"name": "Music Trends"},
            {"name": "Yoga and Meditation"},
            {"name": "Climate Change"},
        ]

        # Add categories
        for category_data in categories:
            category, created = Category.objects.get_or_create(name=category_data["name"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Category '{category.name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category.name}' already exists"))

        # Add topics
        for topic_data in topics:
            topic, created = Topic.objects.get_or_create(name=topic_data["name"])
            if created:
                self.stdout.write(self.style.SUCCESS(f"Topic '{topic.name}' created"))
            else:
                self.stdout.write(self.style.WARNING(f"Topic '{topic.name}' already exists"))

        self.stdout.write(self.style.SUCCESS("Database population complete!"))
