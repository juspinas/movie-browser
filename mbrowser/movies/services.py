from typing import List, Iterable

from mbrowser.adapters.abstract_repository import AbstractRepository
from mbrowser.domain.model import Director, Genre, Actor, Movie, User


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


# def add_comment(article_id: int, comment_text: str, username: str, repo: AbstractRepository):
#     # Check that the article exists.
#     article = repo.get_article(article_id)
#     if article is None:
#         raise NonExistentArticleException

#     user = repo.get_user(username)
#     if user is None:
#         raise UnknownUserException

#     # Create comment.
#     comment = make_comment(comment_text, user, article)

#     # Update the repository.
#     repo.add_comment(comment)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)

# def get_all_movies(repo: AbstractRepository):
#     return repo.get_all_movies()


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_release_year(year, repo: AbstractRepository):
    # Returns articles for the target date (empty if no matches), the date of the previous article (might be null), the date of the next article (might be null)

    movies = repo.get_movies_by_release_year(target_year=year)

    movies_dto = list()
    # prev_date = next_date = None

    if len(movies) > 0:
        # prev_date = repo.get_date_of_previous_article(articles[0])
        # next_date = repo.get_date_of_next_article(articles[0])

        # Convert Articles to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto #, prev_date, next_date


def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


# def get_comments_for_article(article_id, repo: AbstractRepository):
#     article = repo.get_article(article_id)

#     if article is None:
#         raise NonExistentArticleException

#     return comments_to_dict(article.comments)


# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'movie_id': movie.movie_id,
        'title': movie.title,
        'release_year': movie.release_year,
        'director' : movie.director,
        'actors' : [],
        'genres' : genres_to_dict(movie.genres)
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


# def comment_to_dict(comment: Comment):
#     comment_dict = {
#         'username': comment.user.username,
#         'article_id': comment.article.id,
#         'comment_text': comment.comment,
#         'timestamp': comment.timestamp
#     }
#     return comment_dict


# def comments_to_dict(comments: Iterable[Comment]):
#     return [comment_to_dict(comment) for comment in comments]


def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'genre_movies': [movie.movie_id for movie in genre.genre_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.release_year, dict.id, dict.director, dict.actors, dict.genres)
    # Note there's no comments or tags.
    return article