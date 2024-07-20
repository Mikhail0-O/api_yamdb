import os
import csv

from django.core.management.base import BaseCommand
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

from reviews.models import Titles, Genres, Categories, Reviews, Comments
from users.models import CustomUser, Role


class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            'folder_path',
            type=str,
            help='The folder containing the CSV files'
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        folder_path = kwargs['folder_path']

        file_map = {
            'category': self.load_categories,
            'genre': self.load_genres,
            'titles': self.load_titles,
            'genre_title': self.load_genre_titles,
            'users': self.load_users,
            'review': self.load_reviews,
            'comments': self.load_comments,
        }

        try:
            for file_name, load_function in file_map.items():
                file_path = os.path.join(folder_path, f'{file_name}.csv')
                if os.path.exists(file_path):
                    load_function(file_path)
                else:
                    self.stdout.write(self.style.WARNING(
                        f'{file_name}.csv not found in the folder')
                    )

            self.stdout.write(self.style.SUCCESS('Data imported successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error importing data: {e}'))
            transaction.set_rollback(True)

    def load_categories(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Categories.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

    def load_genres(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Genres.objects.get_or_create(
                    id=int(row['id']),
                    name=row['name'],
                    slug=row['slug']
                )

    def load_titles(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                category = Categories.objects.get(id=int(row['category']))
                title = Titles.objects.create(
                    id=int(row['id']),
                    name=row['name'],
                    year=int(row['year']),
                    description=row.get('description', ''),
                    category=category
                )
                genres = row['genre'].split('|') if 'genre' in row else []
                for genre_name in genres:
                    genre = Genres.objects.get(slug=genre_name)
                    title.genre.add(genre)

    def load_genre_titles(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Titles.objects.get(id=int(row['title_id']))
                genre = Genres.objects.get(id=int(row['genre_id']))
                title.genre.add(genre)

    def load_users(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    role = Role.objects.get(title=row['role'])
                except ObjectDoesNotExist:
                    # Если роль не существует, создаем её
                    role = Role.objects.create(title=row['role'])
                CustomUser.objects.create_user(
                    id=int(row['id']),
                    username=row['username'],
                    email=row['email'],
                    role=role,
                    bio=row.get('bio', ''),
                    first_name=row.get('first_name', ''),
                    last_name=row.get('last_name', '')
                )

    def load_reviews(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                title = Titles.objects.get(id=int(row['title_id']))
                user = CustomUser.objects.get(id=int(row['author']))
                Reviews.objects.create(
                    id=int(row['id']),
                    title=title,
                    text=row['text'],
                    author=user,
                    rating=int(row['score']),
                    pub_date=row['pub_date']
                )

    def load_comments(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                review = Reviews.objects.get(id=int(row['review_id']))
                user = CustomUser.objects.get(id=int(row['author']))
                Comments.objects.create(
                    id=int(row['id']),
                    review=review,
                    text=row['text'],
                    author=user,
                    pub_date=row['pub_date']
                )
