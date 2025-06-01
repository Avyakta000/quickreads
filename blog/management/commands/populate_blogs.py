from django.core.management.base import BaseCommand
from blog.models import Blog, Category, Topic
from django.contrib.auth import get_user_model
import random

User = get_user_model()

class Command(BaseCommand):
    help = "Populate the database with 20 detailed blog posts"

    def handle(self, *args, **kwargs):
        authors = User.objects.all()
        categories = Category.objects.all()
        topics = Topic.objects.all()

        if not authors.exists():
            self.stdout.write(self.style.ERROR("No users found. Please create a user first."))
            return

        if not categories.exists():
            self.stdout.write(self.style.ERROR("No categories found. Please populate categories first."))
            return

        if not topics.exists():
            self.stdout.write(self.style.ERROR("No topics found. Please populate topics first."))
            return

        blogs = [
            {
                "title": "The Rise of AI in Everyday Life",
                "content": """Artificial Intelligence (AI) is transforming our daily lives in subtle yet significant ways. From virtual assistants like Siri and Alexa to personalized recommendations on Netflix and Amazon, AI algorithms are constantly working in the background. In healthcare, AI helps in early disease detection, while in finance, it’s streamlining fraud detection. As the technology matures, ethical concerns and data privacy remain crucial points of discussion. However, the benefits, from automation to increased productivity, are undeniable."""
            },
            {
                "title": "Healthy Eating Habits for Busy Professionals",
                "content": """In today’s fast-paced work culture, it’s easy to prioritize deadlines over diet. But healthy eating doesn’t have to be time-consuming. Meal prepping on weekends, choosing wholesome snacks like nuts and fruits, and staying hydrated can make a huge difference. Avoiding sugary drinks and processed foods can enhance energy levels and mental clarity. Remember, a healthy body fuels a productive mind."""
            },
            {
                "title": "How Online Learning is Changing Education",
                "content": """The digital shift in education has opened doors for learners globally. Online platforms like Coursera, Udemy, and edX provide access to world-class courses at a fraction of traditional costs. This flexibility allows working professionals to upskill, students to learn at their own pace, and educators to reach a wider audience. Yet, challenges like digital divide and student engagement still need to be addressed to make online learning more effective and inclusive."""
            },
            {
                "title": "Top 10 Travel Destinations for 2025",
                "content": """From the ancient temples of Kyoto to the vibrant streets of Cape Town, 2025 promises unforgettable travel adventures. Iceland’s natural beauty, Morocco’s rich culture, and Colombia’s rebirth as a tourist haven are top contenders. Emerging eco-tourism spots in Costa Rica and Bhutan emphasize sustainability. Whether you're a beach lover or mountain hiker, there’s a place for every type of traveler in 2025."""
            },
            {
                "title": "Mastering Vegan Cooking at Home",
                "content": """Vegan cooking isn’t just a trend — it’s a lifestyle rooted in health and sustainability. Staples like lentils, beans, tofu, and seasonal vegetables can be transformed into flavorful meals with the right spices and sauces. Experimenting with recipes like vegan chili, cashew cheese, or oat milk pancakes can make plant-based eating both satisfying and exciting. Don’t forget to supplement B12 and iron when going fully vegan."""
            },
            {
                "title": "Understanding Cryptocurrency Trends",
                "content": """The cryptocurrency market continues to evolve, with new tokens, regulations, and use cases emerging regularly. While Bitcoin and Ethereum remain dominant, DeFi (Decentralized Finance) and NFTs (Non-Fungible Tokens) are changing how people interact with money and art. Governments are now stepping in with CBDCs (Central Bank Digital Currencies), indicating mainstream acknowledgment. Investors must stay informed and cautious amidst high volatility and security risks."""
            },
            {
                "title": "Decluttering Your Digital Life",
                "content": """Just as physical clutter can affect your productivity, digital clutter can overwhelm your mind. Start by cleaning your inbox, organizing files in cloud storage, and uninstalling unused apps. Set screen time limits and notifications to reduce distractions. Use password managers to simplify login chaos. A well-organized digital life boosts focus, saves time, and improves mental clarity."""
            },
            {
                "title": "The Future of Streaming Platforms",
                "content": """The streaming wars are intensifying with giants like Netflix, Disney+, and Apple TV+ investing heavily in original content. Meanwhile, niche platforms focusing on documentaries, anime, or classic films are gaining traction. Subscription fatigue is real, and bundling services or ad-supported models may shape the next phase of streaming. Tech like AI-powered personalization and 8K streaming are already being tested in beta environments."""
            },
            {
                "title": "Home Workout Routines That Work",
                "content": """Staying fit doesn’t require a gym membership. Bodyweight exercises like squats, planks, and push-ups can be done in small spaces. Apps like FitOn, Nike Training Club, and YouTube channels provide guided routines. Resistance bands and adjustable dumbbells offer variety. The key is consistency and gradually increasing intensity. Make workouts enjoyable to stick with them long term."""
            },
            {
                "title": "What SpaceX Means for Space Travel",
                "content": """Elon Musk’s SpaceX has revolutionized the space industry with reusable rockets and ambitious plans to colonize Mars. With successful missions to the ISS and upcoming lunar contracts with NASA, the company is reducing the cost and increasing the frequency of space travel. While critics question the feasibility of Mars colonization, SpaceX has undoubtedly reignited public interest in space exploration."""
            },
            {
                "title": "Machine Learning vs Traditional Programming",
                "content": """Traditional programming requires explicit instructions, while machine learning enables computers to learn patterns from data. This shift allows more complex decision-making — from spam filters to voice recognition. However, ML models require large datasets and ongoing training, making explainability and bias important considerations. The future lies in combining both paradigms for optimal results."""
            },
            {
                "title": "Nutrition Tips for Better Energy",
                "content": """A well-balanced diet rich in whole grains, lean proteins, and healthy fats can stabilize energy levels. Avoiding excessive caffeine and sugar prevents crashes. Incorporating superfoods like chia seeds, spinach, and almonds boosts stamina. Small, frequent meals rather than heavy ones help maintain consistent energy throughout the day. Hydration is also crucial and often overlooked."""
            },
            {
                "title": "Top E-Learning Platforms Reviewed",
                "content": """With hundreds of platforms available, choosing the right one depends on your goals. Coursera offers university-certified courses, Udemy shines in practical skills, while Skillshare fosters creativity. LinkedIn Learning is great for professional development, and Khan Academy remains a solid free option for students. User interface, pricing, and course variety are key differentiators to consider."""
            },
            {
                "title": "Hidden Gems for Cultural Travel",
                "content": """Beyond Paris and Rome lie destinations like Georgia’s Tbilisi, Japan’s Kanazawa, or Peru’s Arequipa — rich in heritage, food, and local traditions. These spots offer deeper cultural immersion without tourist crowds. Supporting local artisans, attending traditional festivals, and trying regional cuisines offer unforgettable experiences. Respecting local customs enhances the journey even more."""
            },
            {
                "title": "Easy Desserts to Make in 15 Minutes",
                "content": """Quick treats like chocolate mug cakes, banana ice cream, and no-bake energy bites satisfy cravings without fuss. Using pantry staples like oats, cocoa powder, peanut butter, and honey, you can whip up delicious desserts in minutes. These are great for impromptu guests, midnight snacks, or healthy alternatives to store-bought sweets."""
            },
            {
                "title": "How to Start Investing in Stocks",
                "content": """Stock market investing can seem intimidating, but starting with index funds and understanding key metrics like P/E ratio, market cap, and dividend yield makes it manageable. Platforms like Zerodha, Groww, or Robinhood simplify onboarding. Diversification and long-term thinking are your friends. Start small, be consistent, and keep emotions in check."""
            },
            {
                "title": "Work-Life Balance in a Remote World",
                "content": """Remote work has blurred boundaries between office and home. Setting clear working hours, creating a dedicated workspace, and taking regular breaks can help. Disconnecting after work and making time for hobbies, family, or fitness are essential for mental health. Companies must also foster a culture that respects personal time to avoid burnout."""
            },
            {
                "title": "Latest Music Trends You Should Know",
                "content": """From AI-generated music to the resurgence of vinyl, the music industry is undergoing a transformation. Genres are blending, independent artists are thriving via streaming platforms, and fan-powered content like TikTok is dictating what goes viral. Live concerts are adapting with virtual events and augmented reality. It's an exciting time for both listeners and creators."""
            },
            {
                "title": "Benefits of Daily Yoga and Meditation",
                "content": """Incorporating yoga and meditation into your daily routine can significantly reduce stress, improve flexibility, and enhance emotional well-being. Just 20 minutes of morning stretches and mindful breathing can set a positive tone for the day. Long-term benefits include better posture, deeper sleep, and improved focus. The key is consistency over intensity."""
            },
            {
                "title": "Climate Change: What You Can Do Now",
                "content": """Individual actions like reducing meat consumption, cutting down on plastic, using public transport, and supporting eco-conscious brands can collectively make a difference. Voting for green policies, planting trees, and educating others multiplies the impact. Climate change is urgent, but we still have time to act — and it starts with you."""
            },
        ]

        for blog_data in blogs:
            author = random.choice(authors)
            category = random.choice(categories)
            selected_topics = random.sample(list(topics), k=min(2, len(topics)))

            blog = Blog.objects.create(
                title=blog_data["title"],
                content=blog_data["content"],
                author=author,
                categories=category,
            )
            blog.topics.set(selected_topics)

            self.stdout.write(self.style.SUCCESS(f"Created blog: {blog.title}"))

        self.stdout.write(self.style.SUCCESS("Successfully added 20 detailed blog posts."))
