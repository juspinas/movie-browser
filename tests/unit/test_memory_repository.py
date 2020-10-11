from datetime import date, datetime
from typing import List

import pytest

from mbrowser.domain.model import Director, Genre, Actor, Movie, User, make_genre_association
from mbrowser.adapters.abstract_repository import RepositoryException


# def test_repository_can_add_a_user(in_memory_repo):
#     user = User('Dave', '123456789')
#     in_memory_repo.add_user(user)

#     assert in_memory_repo.get_user('Dave') is user


# def test_repository_can_retrieve_a_user(in_memory_repo):
#     user = in_memory_repo.get_user('fmercury')
#     assert user == User('fmercury', '8734gfe2058v')


# def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
#     user = in_memory_repo.get_user('prince')
#     assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 1000 Movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Sing", "2016", 4)
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(4) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(4)

    # Check that the Movie has the expected title.
    assert movie.title == 'Sing'
    assert movie.release_year == 2016
    assert movie.movie_id == 4
    assert movie.director == 'Christophe Lourdelet'

    # Check that the Movie has expected genres.
    assert movie.has_genre(Genre('Animation'))
    assert movie.has_genre(Genre('Comedy'))
    assert movie.has_genre(Genre('Family'))


def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1001)
    assert movie is None


def test_repository_can_retrieve_movies_by_release_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_release_year(2006)

    # Check that the query returned 44 Movies.
    assert len(movies) == 44


def test_repository_does_not_retrieve_an_article_when_there_are_no_movies_for_a_given_release_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_release_year(2005)
    assert len(movies) == 0


def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()
    assert len(genres) == 20

    genre1 = [genre for genre in genres if genre.genre_name == 'Sci-Fi'][0]
    genre2 = [genre for genre in genres if genre.genre_name == 'Sport'][0]
    # genre3 = [genre for genre in genres if genre.genre_name == 'World'][0]
    # genre4 = [genre for genre in genres if genre.genre_name == 'Politics'][0]

    assert genre1.number_of_genre_movies == 120
    assert genre2.number_of_genre_movies == 18
    # assert genree.number_of_genre_movies == 3
    # assert genre4.number_of_genre_movies == 1



def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Nine Lives'



def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([4, 92, 487])

    assert len(movies) == 3
    assert movies[0].title == 'Sing'
    assert movies[1].title == "Warcraft"
    assert movies[2].title == 'Hairspray'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([4, 1001])

    assert len(movies) == 1
    assert movies[0].title == 'Sing'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 1001])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    genre_ids = in_memory_repo.get_movie_ids_for_genre('Sport')

    assert genre_ids == [195,311,338,368,378,382,494,549,575,585,587,594,597,831,850,897,936,975]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    genre_ids = in_memory_repo.get_movie_ids_for_genre('Anime')

    assert len(genre_ids) == 0


# def test_repository_returns_release_year_of_previous_movie(in_memory_repo):
#     article = in_memory_repo.get_article(6)
#     previous_date = in_memory_repo.get_date_of_previous_article(article)

#     assert previous_date.isoformat() == '2020-03-01'


# def test_repository_returns_none_when_there_are_no_previous_articles(in_memory_repo):
#     article = in_memory_repo.get_article(1)
#     previous_date = in_memory_repo.get_date_of_previous_article(article)

#     assert previous_date is None


# def test_repository_returns_date_of_next_article(in_memory_repo):
#     article = in_memory_repo.get_article(3)
#     next_date = in_memory_repo.get_date_of_next_article(article)

#     assert next_date.isoformat() == '2020-03-05'


# def test_repository_returns_none_when_there_are_no_subsequent_articles(in_memory_repo):
#     article = in_memory_repo.get_article(6)
#     next_date = in_memory_repo.get_date_of_next_article(article)

#     assert next_date is None


def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Anime')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


# def test_repository_can_add_a_comment(in_memory_repo):
#     user = in_memory_repo.get_user('thorke')
#     article = in_memory_repo.get_article(2)
#     comment = make_comment("Trump's onto it!", user, article)

#     in_memory_repo.add_comment(comment)

#     assert comment in in_memory_repo.get_comments()


# def test_repository_does_not_add_a_comment_without_a_user(in_memory_repo):
#     article = in_memory_repo.get_article(2)
#     comment = Comment(None, article, "Trump's onto it!", datetime.today())

#     with pytest.raises(RepositoryException):
#         in_memory_repo.add_comment(comment)


# def test_repository_does_not_add_a_comment_without_an_article_properly_attached(in_memory_repo):
#     user = in_memory_repo.get_user('thorke')
#     article = in_memory_repo.get_article(2)
#     comment = Comment(None, article, "Trump's onto it!", datetime.today())

#     user.add_comment(comment)

#     with pytest.raises(RepositoryException):
#         # Exception expected because the Article doesn't refer to the Comment.
#         in_memory_repo.add_comment(comment)


# def test_repository_can_retrieve_comments(in_memory_repo):
#     assert len(in_memory_repo.get_comments()) == 2