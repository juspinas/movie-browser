from datetime import date, datetime
from typing import List

import pytest

from mbrowser.domain.model import Director, Genre, Actor, Movie, User
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


# def test_repository_can_retrieve_tags(in_memory_repo):
#     tags: List[Tag] = in_memory_repo.get_tags()

#     assert len(tags) == 4

#     tag_one = [tag for tag in tags if tag.tag_name == 'New Zealand'][0]
#     tag_two = [tag for tag in tags if tag.tag_name == 'Health'][0]
#     tag_three = [tag for tag in tags if tag.tag_name == 'World'][0]
#     tag_four = [tag for tag in tags if tag.tag_name == 'Politics'][0]

#     assert tag_one.number_of_tagged_articles == 3
#     assert tag_two.number_of_tagged_articles == 2
#     assert tag_three.number_of_tagged_articles == 3
#     assert tag_four.number_of_tagged_articles == 1


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


# def test_repository_returns_article_ids_for_existing_tag(in_memory_repo):
#     article_ids = in_memory_repo.get_article_ids_for_tag('New Zealand')

#     assert article_ids == [1, 3, 4]


# def test_repository_returns_an_empty_list_for_non_existent_tag(in_memory_repo):
#     article_ids = in_memory_repo.get_article_ids_for_tag('United States')

#     assert len(article_ids) == 0


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


# def test_repository_can_add_a_tag(in_memory_repo):
#     tag = Tag('Motoring')
#     in_memory_repo.add_tag(tag)

#     assert tag in in_memory_repo.get_tags()


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