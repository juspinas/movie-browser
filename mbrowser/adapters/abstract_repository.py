import abc
from typing import List
from datetime import date

from mbrowser.domain.model import Director, Genre, Actor, Movie, User

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    # @abc.abstractmethod
    # def add_user(self, user: User):
    #     """" Adds a User to the repository. """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_user(self, username) -> User:
    #     """ Returns the User named username from the repository.
    #     If there is no User with the given username, this method returns None.
    #     """
    #     raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        """ Returns Movie with id from the repository.
        If there is no Movie with the given id, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_release_year(self, target_year: int) -> List[Movie]:
        """ Returns a list of Movies that were released on target_year.
        If there are no Movies released on the given year, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie, ordered by release_year, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie, ordered by release_year, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        """ Returns a list of Movies, whose ids match those in id_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Movies that are tagged by genre_name.
        If there are no movies that are tagged by genre_name, this method returns an empty list.
        """
        raise NotImplementedError

    # @abc.abstractmethod
    # def get_release_year_of_previous_movie(self, movie: Movie):
    #     """ Returns the date of an Article that immediately precedes article.
    #     If article is the first Article in the repository, this method returns None because there are no Articles
    #     on a previous date.
    #     """
    #     raise NotImplementedError

    # @abc.abstractmethod
    # def get_release_year_of_next_movie(self, movie: Movie):
    #     """ Returns the date of an Article that immediately follows article.
    #     If article is the last Article in the repository, this method returns None because there are no Articles
    #     on a later date.
    #     """
    #     raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    # @abc.abstractmethod
    # def add_comment(self, comment: Comment):
    #     """ Adds a Comment to the repository.
    #     If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
    #     RepositoryException and doesn't update the repository.
    #     """
    #     if comment.user is None or comment not in comment.user.comments:
    #         raise RepositoryException('Comment not correctly attached to a User')
    #     if comment.article is None or comment not in comment.article.comments:
    #         raise RepositoryException('Comment not correctly attached to an Article')

    # @abc.abstractmethod
    # def get_comments(self):
    #     """ Returns the Comments stored in the repository. """
    #     raise NotImplementedError