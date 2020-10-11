from flask import Blueprint, request, render_template, redirect, url_for, session

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_genre', genre=genre_name)

    return genre_urls

def get_letter_urls():
    letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    letter_urls = dict()
    for letter in letters:
        letter_urls[letter] = url_for('movies_bp.movies_by_title', letter=letter)

    return letter_urls


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    # for movie in movies:
    #     movie['hyperlink'] = url_for('movies_bp.movies_by_rank', date=article['date'].isoformat())
    return movies