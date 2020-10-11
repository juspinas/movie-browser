from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.utilities as utilities
import mbrowser.movies.services as services

# from mbrowser.authentication.authentication import login_required


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)

@movies_blueprint.route('/movies_by_title', methods=['GET'])
def movies_by_title():
    letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    movies_per_page = 20

    # Read query parameters.
    letter = request.args.get('letter')

    cursor = request.args.get('cursor')

    # article_to_show_comments = request.args.get('view_comments_for')

    # if article_to_show_comments is None:
    #     # No view-comments query parameter, so set to a non-existent article id.
    #     article_to_show_comments = -1
    # else:
    #     # Convert article_to_show_comments from string to int.
    #     article_to_show_comments = int(article_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for articles that are tagged with tag_name.
    movie_ids = range(1,1001)

    # Retrieve the batch of articles to display on the Web page.
    all_movies = services.get_movies_by_id(movie_ids, repo.repo_instance)
    movies = list()
    for movie in all_movies:
        if movie['title'][0] == letter:
            movies.append(movie)
        elif letter == '#' and not movie['title'][0].isalpha():
            movies.append(movie)
    movies = sorted(movies, key = lambda i: (i['title'], i['release_year']))
    shown_movies = movies[cursor:cursor + movies_per_page]
    # all_movies = services.get_all_movies(repo.repo_instance)
    # movies = all_movies[cursor:cursor + movies_per_page]

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_title', letter = letter, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_title', letter = letter)

    if cursor + movies_per_page < len(movies):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_title', letter = letter, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movies) / movies_per_page)
        if len(movies) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_title', letter = letter, cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    # for article in articles:
    #     article['view_comment_url'] = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
    #     article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

    # Generate the webpage to display the articles.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Browse Movies',
        movies=shown_movies,
        # selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        current_letter=letter,
        letters=letters,
        letter_urls=utilities.get_letter_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        # show_comments_for_article=article_to_show_comments
    )

@movies_blueprint.route('/movies_by_rank', methods=['GET'])
def movies_by_rank():
    movies_per_page = 20

    # Read query parameters.
    # tag_name = request.args.get('tag')
    cursor = request.args.get('cursor')
    # article_to_show_comments = request.args.get('view_comments_for')

    # if article_to_show_comments is None:
    #     # No view-comments query parameter, so set to a non-existent article id.
    #     article_to_show_comments = -1
    # else:
    #     # Convert article_to_show_comments from string to int.
    #     article_to_show_comments = int(article_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for articles that are tagged with tag_name.
    movie_ids = range(1,1001)

    # Retrieve the batch of articles to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_rank', cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_rank')

    if cursor + movies_per_page < len(movie_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_rank', cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_rank', cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    # for article in articles:
    #     article['view_comment_url'] = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
    #     article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

    # Generate the webpage to display the articles.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Showing 1000 Movies By Rank',
        movies=movies,
        # selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        # show_comments_for_article=article_to_show_comments
    )

@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 20

    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')
    # article_to_show_comments = request.args.get('view_comments_for')

    # if article_to_show_comments is None:
    #     # No view-comments query parameter, so set to a non-existent article id.
    #     article_to_show_comments = -1
    # else:
    #     # Convert article_to_show_comments from string to int.
    #     article_to_show_comments = int(article_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for articles that are tagged with tag_name.
    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)

    # Retrieve the batch of articles to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    # for article in articles:
    #     article['view_comment_url'] = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
    #     article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

    # Generate the webpage to display the articles.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Showing ' + genre_name + ' Movies',
        movies=movies,
        # selected_movies=utilities.get_selected_movies(len(movies) * 2),
        genre_urls=utilities.get_genres_and_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
        # show_comments_for_article=article_to_show_comments
    )

# @movies_blueprint.route('/movies_by_year', methods=['GET'])
# def movies_by_year():
#     # Read query parameters.
#     target_year = request.args.get('year')
#     # article_to_show_comments = request.args.get('view_comments_for')

#     # Fetch the first and last articles in the series.
#     first_movie = services.get_first_movie(repo.repo_instance)
#     last_movie = services.get_last_movie(repo.repo_instance)

#     if target_year is None:
#         # No date query parameter, so return articles from day 1 of the series.
#         target_year = first_movie['release_year']
#     # else:
#         # Convert target_date from string to date.
#         # target_date = date.fromisoformat(target_date)

#     # if article_to_show_comments is None:
#     #     # No view-comments query parameter, so set to a non-existent article id.
#     #     article_to_show_comments = -1
#     # else:
#     #     # Convert article_to_show_comments from string to int.
#     #     article_to_show_comments = int(article_to_show_comments)

#     # Fetch article(s) for the target date. This call also returns the previous and next dates for articles immediately
#     # before and after the target date.
#     movies = services.get_movies_by_release_year(target_year, repo.repo_instance)

#     first_article_url = None
#     last_article_url = None
#     next_article_url = None
#     prev_article_url = None

#     if len(movies) > 0:
#         # There's at least one article for the target date.
#         if previous_date is not None:
#             # There are articles on a previous date, so generate URLs for the 'previous' and 'first' navigation buttons.
#             prev_article_url = url_for('news_bp.articles_by_date', date=previous_date.isoformat())
#             first_article_url = url_for('news_bp.articles_by_date', date=first_article['date'].isoformat())

#         # There are articles on a subsequent date, so generate URLs for the 'next' and 'last' navigation buttons.
#         if next_date is not None:
#             next_article_url = url_for('news_bp.articles_by_date', date=next_date.isoformat())
#             last_article_url = url_for('news_bp.articles_by_date', date=last_article['date'].isoformat())

#         # Construct urls for viewing article comments and adding comments.
#         for article in articles:
#             article['view_comment_url'] = url_for('news_bp.articles_by_date', date=target_date, view_comments_for=article['id'])
#             article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

#         # Generate the webpage to display the articles.
#         return render_template(
#             'news/articles.html',
#             title='Articles',
#             articles_title=target_date.strftime('%A %B %e %Y'),
#             articles=articles,
#             selected_articles=utilities.get_selected_articles(len(articles) * 2),
#             tag_urls=utilities.get_tags_and_urls(),
#             first_article_url=first_article_url,
#             last_article_url=last_article_url,
#             prev_article_url=prev_article_url,
#             next_article_url=next_article_url,
#             show_comments_for_article=article_to_show_comments
#         )

#     # No articles to show, so return the homepage.
#     return redirect(url_for('home_bp.home'))


# @news_blueprint.route('/articles_by_tag', methods=['GET'])
# def articles_by_tag():
#     articles_per_page = 3

#     # Read query parameters.
#     tag_name = request.args.get('tag')
#     cursor = request.args.get('cursor')
#     article_to_show_comments = request.args.get('view_comments_for')

#     if article_to_show_comments is None:
#         # No view-comments query parameter, so set to a non-existent article id.
#         article_to_show_comments = -1
#     else:
#         # Convert article_to_show_comments from string to int.
#         article_to_show_comments = int(article_to_show_comments)

#     if cursor is None:
#         # No cursor query parameter, so initialise cursor to start at the beginning.
#         cursor = 0
#     else:
#         # Convert cursor from string to int.
#         cursor = int(cursor)

#     # Retrieve article ids for articles that are tagged with tag_name.
#     article_ids = services.get_article_ids_for_tag(tag_name, repo.repo_instance)

#     # Retrieve the batch of articles to display on the Web page.
#     articles = services.get_articles_by_id(article_ids[cursor:cursor + articles_per_page], repo.repo_instance)

#     first_article_url = None
#     last_article_url = None
#     next_article_url = None
#     prev_article_url = None

#     if cursor > 0:
#         # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
#         prev_article_url = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor - articles_per_page)
#         first_article_url = url_for('news_bp.articles_by_tag', tag=tag_name)

#     if cursor + articles_per_page < len(article_ids):
#         # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
#         next_article_url = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor + articles_per_page)

#         last_cursor = articles_per_page * int(len(article_ids) / articles_per_page)
#         if len(article_ids) % articles_per_page == 0:
#             last_cursor -= articles_per_page
#         last_article_url = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=last_cursor)

#     # Construct urls for viewing article comments and adding comments.
#     for article in articles:
#         article['view_comment_url'] = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
#         article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

#     # Generate the webpage to display the articles.
#     return render_template(
#         'news/articles.html',
#         title='Articles',
#         articles_title='Articles tagged by ' + tag_name,
#         articles=articles,
#         selected_articles=utilities.get_selected_articles(len(articles) * 2),
#         tag_urls=utilities.get_tags_and_urls(),
#         first_article_url=first_article_url,
#         last_article_url=last_article_url,
#         prev_article_url=prev_article_url,
#         next_article_url=next_article_url,
#         show_comments_for_article=article_to_show_comments
#     )


# @news_blueprint.route('/comment', methods=['GET', 'POST'])
# @login_required
# def comment_on_article():
#     # Obtain the username of the currently logged in user.
#     username = session['username']

#     # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
#     # the form with an article id, when subsequently called with a HTTP POST request, the article id remains in the
#     # form.
#     form = CommentForm()

#     if form.validate_on_submit():
#         # Successful POST, i.e. the comment text has passed data validation.
#         # Extract the article id, representing the commented article, from the form.
#         article_id = int(form.article_id.data)

#         # Use the service layer to store the new comment.
#         services.add_comment(article_id, form.comment.data, username, repo.repo_instance)

#         # Retrieve the article in dict form.
#         article = services.get_article(article_id, repo.repo_instance)

#         # Cause the web browser to display the page of all articles that have the same date as the commented article,
#         # and display all comments, including the new comment.
#         return redirect(url_for('news_bp.articles_by_date', date=article['date'], view_comments_for=article_id))

#     if request.method == 'GET':
#         # Request is a HTTP GET to display the form.
#         # Extract the article id, representing the article to comment, from a query parameter of the GET request.
#         article_id = int(request.args.get('article'))

#         # Store the article id in the form.
#         form.article_id.data = article_id
#     else:
#         # Request is a HTTP POST where form validation has failed.
#         # Extract the article id of the article being commented from the form.
#         article_id = int(form.article_id.data)

#     # For a GET or an unsuccessful POST, retrieve the article to comment in dict form, and return a Web page that allows
#     # the user to enter a comment. The generated Web page includes a form object.
#     article = services.get_article(article_id, repo.repo_instance)
#     return render_template(
#         'news/comment_on_article.html',
#         title='Edit article',
#         article=article,
#         form=form,
#         handler_url=url_for('news_bp.comment_on_article'),
#         selected_articles=utilities.get_selected_articles(),
#         tag_urls=utilities.get_tags_and_urls()
#     )


# class ProfanityFree:
#     def __init__(self, message=None):
#         if not message:
#             message = u'Field must not contain profanity'
#         self.message = message

#     def __call__(self, form, field):
#         if profanity.contains_profanity(field.data):
#             raise ValidationError(self.message)


# class CommentForm(FlaskForm):
#     comment = TextAreaField('Comment', [
#         DataRequired(),
#         Length(min=4, message='Your comment is too short'),
#         ProfanityFree(message='Your comment must not contain profanity')])
#     article_id = HiddenField("Article id")
#     submit = SubmitField('Submit')