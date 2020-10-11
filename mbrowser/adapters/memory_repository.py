import csv
import os
from datetime import date, datetime
from typing import List

from bisect import bisect, bisect_left, insort_left

# from werkzeug.security import generate_password_hash

from mbrowser.adapters.abstract_repository import AbstractRepository, RepositoryException
from mbrowser.domain.model import Director, Genre, Actor, Movie, User, make_genre_association


class MemoryRepository(AbstractRepository):
    # Articles ordered by date, not id. id is assumed unique.

    def __init__(self):
        self._movies = list()
        self._movies_index = dict()
        self._genres = list()
        self._users = list()
        self._comments = list()

    # def add_user(self, user: User):
    #     self._users.append(user)

    # def get_user(self, username) -> User:
    #     return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        insort_left(self._movies, movie)
        self._movies_index[movie.movie_id] = movie

    def get_movie(self, id: int) -> Movie:
        movie = None

        try:
            movie = self._movies_index[id]
        except KeyError:
            pass  # Ignore exception and return None.

        return movie

    # def get_all_movies(self):
    #     return self._movies

    def get_movies_by_release_year(self, target_year: int) -> List[Movie]:
        target_movie = Movie(
            title=None,
            release_year=target_year,
            movie_id=None,
            director = Director(""),
        )
        matching_movies = list()

        try:
            for movie in self._movies:
                if movie.release_year == target_year:
                    matching_movies.append(movie)
        except ValueError:
            # No movies for specified release year. Simply return an empty list.
            pass

        return matching_movies

    def get_number_of_movies(self):
        return len(self._movies)

    def get_first_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[0]
        return movie

    def get_last_movie(self):
        movie = None

        if len(self._movies) > 0:
            movie = self._movies[-1]
        return movie

    def get_movies_by_id(self, id_list):
        # Strip out any ids in id_list that don't represent Article ids in the repository.
        existing_ids = [id for id in id_list if id in self._movies_index]

        # Fetch the Articles.
        movies = [self._movies_index[id] for id in existing_ids]
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        # Linear search, to find the first occurrence of a Tag with the name tag_name.
        genre = next((genre for genre in self._genres if genre.genre_name == genre_name), None)

        # Retrieve the ids of articles associated with the Tag.
        if genre is not None:
            movie_ids = [movie.movie_id for movie in genre.genre_movies]
        else:
            # No Tag with name tag_name, so return an empty list.
            movie_ids = list()

        return movie_ids

    # def get_release_year_of_previous_movie(self, movie: Movie):
    #     previous_release_year = None

    #     try:
    #         index = self.movie_index(movie)
    #         for stored_movie in reversed(self._movies[0:index]):
    #             if stored_movie.release_year < movie.release_year:
    #                 previous_release_year = stored_movie.release_year
    #                 break
    #     except ValueError:
    #         # No earlier movies, so return None.
    #         pass

    #     return previous_release_year

    # def get_release_year_of_next_movie(self, movie: Movie):
    #     next_release_year = None

    #     try:
    #         index = self.movie_index(movie)
    #         for stored_movie in self._movies[index + 1:len(self._movies)]:
    #             if stored_movie.release_year > movie.release_year:
    #                 next_release_year = stored_movie.release_year
    #                 break
    #     except ValueError:
    #         # No subsequent articles, so return None.
    #         pass

    #     return next_release_year

    def add_genre(self, genre: Genre):
        self._genres.append(genre)

    def get_genres(self) -> List[Genre]:
        print('In memory repo, getting Genres!')
        return self._genres

    # def add_comment(self, comment: Comment):
    #     super().add_comment(comment)
    #     self._comments.append(comment)

    # def get_comments(self):
    #     return self._comments

    # Helper method to return article index.
    def movie_index(self, movie: Movie):
        index = bisect_left(self._movies, movie)
        if index != len(self._movies) and self._movies[index].title == movie.title:
            return index
        raise ValueError


def read_csv_file(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies_and_tags(data_path: str, repo: MemoryRepository):
    genres = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'Data1000Movies.csv')):

        movie_key = int(data_row[0])
        genre_tags = data_row[2].split(",")
        number_of_genres = len(genre_tags)

        # Add any new tags; associate the current movie with tags.
        for genre in genre_tags:
            if genre not in genres.keys():
                genres[genre] = list()
            genres[genre].append(movie_key)

        # del data_row[-number_of_tags:]

        # Create Article object.
        movie = Movie(
            title=data_row[1],
            release_year=data_row[6],
            movie_id=movie_key,
            director=data_row[4],
            # actors
            # date=date.fromisoformat(data_row[1]),
            # title=data_row[2],
            # first_para=data_row[3],
            # hyperlink=data_row[4],
            # image_hyperlink=data_row[5],
            # id=article_key
        )

        # Add the Article to the repository.
        repo.add_movie(movie)

    # Create Tag objects, associate them with Articles and add them to the repository.
    for genre_name in genres.keys():
        genre = Genre(genre_name)
        for movie_id in genres[genre_name]:
            movie = repo.get_movie(movie_id)
            make_genre_association(movie, genre)
        repo.add_genre(genre)


# def load_users(data_path: str, repo: MemoryRepository):
#     users = dict()

#     for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
#         user = User(
#             username=data_row[1],
#             password=generate_password_hash(data_row[2])
#         )
#         repo.add_user(user)
#         users[data_row[0]] = user
#     return users


# def load_comments(data_path: str, repo: MemoryRepository, users):
#     for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
#         comment = make_comment(
#             comment_text=data_row[3],
#             user=users[data_row[1]],
#             article=repo.get_article(int(data_row[2])),
#             timestamp=datetime.fromisoformat(data_row[4])
#         )
#         repo.add_comment(comment)


def populate(data_path: str, repo: MemoryRepository):
    # Load articles and tags into the repository.
    load_movies_and_tags(data_path, repo)

    # Load users into the repository.
    # users = load_users(data_path, repo)

    # # Load comments into the repository.
    # load_comments(data_path, repo, users)