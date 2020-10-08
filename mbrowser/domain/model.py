from datetime import date, datetime
from typing import List, Iterable


class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._comments: List[Comment] = list()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self._comments)

    def add_comment(self, comment: 'Comment'):
        self._comments.append(comment)

    def __repr__(self) -> str:
        return f'<User {self._username} {self._password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username

class Comment:
    def __init__(
            self, user: User, article: 'Article', comment: str, timestamp: datetime
    ):
        self._user: User = user
        self._article: Article = article
        self._comment: Comment = comment
        self._timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self._user

    @property
    def article(self) -> 'Article':
        return self._article

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other._user == self._user and other._article == self._article and other._comment == self._comment and other._timestamp == self._timestamp

class ModelException(Exception):
    pass

# ________________________________________________________________________________________________________________________
class Director:
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()
    
    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if self.__director_full_name == other.director_full_name:
            return True
        else:
            return False

    def __lt__(self, other):
        unsortedOrder = [self.__director_full_name, other.director_full_name]
        sortedOrder = [self.__director_full_name, other.director_full_name]
        sortedOrder.sort()
        if (unsortedOrder == sortedOrder):
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__director_full_name)

class Genre:
    def __init__(self, genre_name: str):
        self.__genre_name = genre_name
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()
            
    @property
    def genre_name(self) -> str:
        return self.__genre_name

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if self.__genre_name == other.genre_name:
            return True
        else:
            return False


    def __lt__(self, other):
        unsortedOrder = [self.__genre_name, other.genre_name]
        sortedOrder = [self.__genre_name, other.genre_name]
        sortedOrder.sort()
        if (unsortedOrder == sortedOrder):
            return True
        else:
            return False


    def __hash__(self):
        return hash(self.__genre_name)

class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__colleagues = set()
    
    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.actor_full_name == self.__actor_full_name

    def __lt__(self, other):
        return self.__actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, self.__class__):
            self.__colleagues.add(colleague)
    
    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__colleagues

class Movie:
    def __init__(self, title: str, release_year: int, movie_id: int):
        if title == None or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()
        if type(release_year) is str or type(release_year) is int:
            try:
                release_year = int(release_year)
                if release_year < 1900:
                    self.__release_year = None
                else:
                    self.__release_year = int(release_year)
            except ValueError:
                release_year = None

        if type(movie_id) is not int:
            self.__movie_id = None
        else:
            self.__movie_id = movie_id
        self.__description = ""
        self.__director = Director("")
        self.__actors = []
        self.__genres = []
        self.__runtime_minutes = 0
        self.__hyperlink = None
    
    @property
    def title(self) -> str:
        return self.__title
    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def movie_id(self) -> int:
        return self.__movie_id

    @property
    def description(self) -> str:
        return self.__description
    @description.setter
    def description(self, description):
        if description == "" or type(description) is not str:
            self.__description = None
        else:
            self.__description = description.strip()
     
    @property
    def director(self) -> Director:
        return self.__director

    @director.setter
    def director(self, director):
        if type(director) is not Director:
            self.__director = Director("")
        else:
            self.__director = director

    @property
    def actors(self) -> []:
        return self.__actors
    @actors.setter
    def actors(self, actors):
        if type(actors) is list:
            self.__actors = actors

    @property
    def genres(self) -> []:
        return self.__genres
    @genres.setter
    def genres(self, genres):
        if type(genres) is list:
            self.__genres = genres
    
    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes
    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if type(runtime_minutes) is not int:
            raise ValueError
        else:
            if runtime_minutes > 0:
                self.__runtime_minutes = runtime_minutes
            else:
                raise ValueError

    @property
    def hyperlink(self) -> str:
        return self._hyperlink
    @genres.setter
    def hyperlink(self, hyperlink):
        if type(hyperlink) is str:
            self.__hyperlink = hyperlink

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if self.__title == other.title and self.__release_year == other.release_year:
            return True
        else:
            return False

    def __lt__(self, other):
        # if self.title == other.title:
        #     return self.release_year < other.release_year
        # return self.title < other.title
        return self.movie_id < other.movie_id
    
    def __hash__(self):
        combinedStr = self.__title + str(self.__release_year)
        return hash(combinedStr)
    
    def add_actor(self,actor):
        if type(actor) is Actor:
            self.__actors += [actor]
    
    def remove_actor(self,actor):
        if type(actor) is Actor:
            if actor in self.__actors:
                self.__actors.remove(actor)

    def add_genre(self,genre):
        if type(genre) is Genre:
            self.__genres += [genre]

    def remove_genre(self,genre):
        if type(genre) is Genre:
            if genre in self.__genres:
                self.__genres.remove(genre)

class Review:
    def __init__(self, movie: Movie, review_text: str, rating: int):
        if type(movie) is not Movie:
            self.__movie = Movie(None,None)
        else:
            self.__movie = movie
        if review_text == "" or type(review_text) is not str:
            self.__review_text = None
        else:
            self.__review_text = review_text.strip()
        if rating < 1 or rating > 10 or type(rating) is not int:
            self.__rating = None
        else:
            self.__rating = rating
        self.__timestamp = datetime.now()
            
    @property
    def movie(self) -> Movie:
        return self.__movie
    @property
    def review_text(self) -> str:
        return self.__review_text
    @property
    def rating(self) -> int:
        return self.__rating

    def __repr__(self):
        return f"<Review {self.__movie}, {self.__review_text}, {self.__rating}, {self.__rating}, {self.__timestamp}>"

    def __eq__(self, other):
        if self.__movie == other.movie and self.__review_text == other.review_text and self.__rating == other.rating and self.__timestamp == other.__timestamp:
            return True
        else:
            return False

class User:

    def __init__(self, user_name: str, password: str):
        if user_name == "" or type(user_name) is not str:
            self.__user_name = None
        else:
            self.__user_name = user_name.strip().lower()
        if password == "" or type(password) is not str:
            self.__password = None
        else:
            self.__password = password
        self.__watched_movies = list()
        self.__reviews = list()
        self.__time_spent_watching_movies_minutes = 0

    @property
    def user_name(self) -> str:
        return self.__user_name

    @property
    def password(self) -> str:
        return self.__password

    @property
    def watched_movies(self) -> list:
        return self.__watched_movies

    @property
    def reviews(self) -> list:
        return self.__reviews

    @property
    def time_spent_watching_movies_minutes(self) -> int:
        return self.__time_spent_watching_movies_minutes

    def watch_movie(self, movie: Movie):
        if isinstance(movie, Movie):
            self.__watched_movies.append(movie)
            self.__time_spent_watching_movies_minutes += movie.runtime_minutes

    def add_review(self, review: Review):
        if isinstance(review, Review):
            self.__reviews.append(review)

    def __repr__(self):
        return f'<User {self.__user_name}>'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return other.user_name == self.__user_name

    def __lt__(self, other):
        return self.__user_name < other.user_name

    def __hash__(self):
        return hash(self.__user_name)
