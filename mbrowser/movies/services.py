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


# def get_article_ids_for_tag(tag_name, repo: AbstractRepository):
#     article_ids = repo.get_article_ids_for_tag(tag_name)

#     return article_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert Articles to dictionary form.
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
        'id': movie.movie_id,
        'title': movie.title,
        'release_year': movie.release_year,
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


# def tag_to_dict(tag: Tag):
#     tag_dict = {
#         'name': tag.tag_name,
#         'tagged_articles': [article.id for article in tag.tagged_articles]
#     }
#     return tag_dict


# def tags_to_dict(tags: Iterable[Tag]):
#     return [tag_to_dict(tag) for tag in tags]


# ============================================
# Functions to convert dicts to model entities
# ============================================

def dict_to_movie(dict):
    movie = Movie(dict.title, dict.release_year, dict.id)
    # Note there's no comments or tags.
    return movie