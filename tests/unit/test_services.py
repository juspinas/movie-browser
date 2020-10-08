from datetime import date

import pytest

# from mbrowser.authentication.services import AuthenticationException
from mbrowser.movies import services as movies_services
# from mbrowser.authentication import services as auth_services
from mbrowser.movies.services import NonExistentMovieException


# def test_can_add_user(in_memory_repo):
#     new_username = 'jz'
#     new_password = 'abcd1A23'

#     auth_services.add_user(new_username, new_password, in_memory_repo)

#     user_as_dict = auth_services.get_user(new_username, in_memory_repo)
#     assert user_as_dict['username'] == new_username

#     # Check that password has been encrypted.
#     assert user_as_dict['password'].startswith('pbkdf2:sha256:')


# def test_cannot_add_user_with_existing_name(in_memory_repo):
#     username = 'thorke'
#     password = 'abcd1A23'

#     with pytest.raises(auth_services.NameNotUniqueException):
#         auth_services.add_user(username, password, in_memory_repo)


# def test_authentication_with_valid_credentials(in_memory_repo):
#     new_username = 'pmccartney'
#     new_password = 'abcd1A23'

#     auth_services.add_user(new_username, new_password, in_memory_repo)

#     try:
#         auth_services.authenticate_user(new_username, new_password, in_memory_repo)
#     except AuthenticationException:
#         assert False


# def test_authentication_with_invalid_credentials(in_memory_repo):
#     new_username = 'pmccartney'
#     new_password = 'abcd1A23'

#     auth_services.add_user(new_username, new_password, in_memory_repo)

#     with pytest.raises(auth_services.AuthenticationException):
#         auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


# def test_can_add_comment(in_memory_repo):
#     article_id = 3
#     comment_text = 'The loonies are stripping the supermarkets bare!'
#     username = 'fmercury'

#     # Call the service layer to add the comment.
#     news_services.add_comment(article_id, comment_text, username, in_memory_repo)

#     # Retrieve the comments for the article from the repository.
#     comments_as_dict = news_services.get_comments_for_article(article_id, in_memory_repo)

#     # Check that the comments include a comment with the new comment text.
#     assert next(
#         (dictionary['comment_text'] for dictionary in comments_as_dict if dictionary['comment_text'] == comment_text),
#         None) is not None


# def test_cannot_add_comment_for_non_existent_article(in_memory_repo):
#     article_id = 7
#     comment_text = "COVID-19 - what's that?"
#     username = 'fmercury'

#     # Call the service layer to attempt to add the comment.
#     with pytest.raises(news_services.NonExistentArticleException):
#         news_services.add_comment(article_id, comment_text, username, in_memory_repo)


# def test_cannot_add_comment_by_unknown_user(in_memory_repo):
#     article_id = 3
#     comment_text = 'The loonies are stripping the supermarkets bare!'
#     username = 'gmichael'

#     # Call the service layer to attempt to add the comment.
#     with pytest.raises(news_services.UnknownUserException):
#         news_services.add_comment(article_id, comment_text, username, in_memory_repo)


def test_can_get_article(in_memory_repo):
    movie_id = 2

    movie_as_dict = movies_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['id'] == movie_id
    assert movie_as_dict['title'] == "Prometheus"
    assert movie_as_dict['release_year'] == 2012
    #assert article_as_dict['first_para'] == 'US President Trump tweeted on Saturday night (US time) that he has asked the Centres for Disease Control and Prevention to issue a ""strong Travel Advisory"" but that a quarantine on the New York region"" will not be necessary.'
    # assert article_as_dict['hyperlink'] == 'https://www.nzherald.co.nz/world/news/article.cfm?c_id=2&objectid=12320699'
    # assert article_as_dict['image_hyperlink'] == 'https://www.nzherald.co.nz/resizer/159Vi4ELuH2fpLrv1SCwYLulzoM=/620x349/smart/filters:quality(70)/arc-anglerfish-syd-prod-nzme.s3.amazonaws.com/public/XQOAY2IY6ZEIZNSW2E3UMG2M4U.jpg'
    # assert len(article_as_dict['comments']) == 0

    # tag_names = [dictionary['name'] for dictionary in article_as_dict['tags']]
    # assert 'World' in tag_names
    # assert 'Health' in tag_names
    # assert 'Politics' in tag_names


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 1001

    # Call the service layer to attempt to retrieve the Movie.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movies_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movies_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['id'] == 1000


# def test_get_articles_by_date_with_one_date(in_memory_repo):
#     target_date = date.fromisoformat('2020-02-28')

#     articles_as_dict, prev_date, next_date = news_services.get_articles_by_date(target_date, in_memory_repo)

#     assert len(articles_as_dict) == 1
#     assert articles_as_dict[0]['id'] == 1

#     assert prev_date is None
#     assert next_date == date.fromisoformat('2020-02-29')


def test_get_movies_by_release_year(in_memory_repo):
    target_year = 2006

    movies_as_dict = movies_services.get_movies_by_release_year(target_year, in_memory_repo)

    # Check that there are 44 movies release in 2006.
    assert len(movies_as_dict) == 44

    # Check that the article ids for the the articles returned are 3, 4 and 5.
    # article_ids = [article['id'] for article in articles_as_dict]
    # assert set([3, 4, 5]).issubset(article_ids)

    # Check that the dates of articles surrounding the target_date are 2020-02-29 and 2020-03-05.
    # assert prev_date == date.fromisoformat('2020-02-29')
    # assert next_date == date.fromisoformat('2020-03-05')


def test_get_moviess_by_release_year_with_non_existent_release_year(in_memory_repo):
    target_year = 2005

    movies_as_dict = movies_services.get_movies_by_release_year(target_year, in_memory_repo)

    # Check that there are no movies released in 2005.
    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [22, 596, 0, 1001]
    movies_as_dict = movies_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the article ids returned were 5 and 6.
    movie_ids = [movie['id'] for movie in movies_as_dict]
    assert set([22, 596]).issubset(movie_ids)


# def test_get_comments_for_article(in_memory_repo):
#     comments_as_dict = news_services.get_comments_for_article(1, in_memory_repo)

#     # Check that 2 comments were returned for article with id 1.
#     assert len(comments_as_dict) == 2

#     # Check that the comments relate to the article whose id is 1.
#     article_ids = [comment['article_id'] for comment in comments_as_dict]
#     article_ids = set(article_ids)
#     assert 1 in article_ids and len(article_ids) == 1


# def test_get_comments_for_non_existent_article(in_memory_repo):
#     with pytest.raises(NonExistentArticleException):
#         comments_as_dict = news_services.get_comments_for_article(7, in_memory_repo)


# def test_get_comments_for_article_without_comments(in_memory_repo):
#     comments_as_dict = news_services.get_comments_for_article(2, in_memory_repo)
#     assert len(comments_as_dict) == 0