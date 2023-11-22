# Functions to populate dev DB with sample Article model instances (22 articles), and also
# to delete them. Will be useful to test pagination, for example.

# Usage:
# In Python Console ran with "python manage.py shell" (or equivalent):
# from blog.utils import populate_dev_db_with_test_user_and_articles, delete_test_user_and_all_articles
# populate_dev_db_with_test_user_and_articles()
# delete_test_user_and_all_articles()

import datetime
import random

from django.contrib.auth.models import User

from blog.models import Article


def populate_dev_db_with_test_user_and_articles():
    user = User.objects.create(username="dev_user_auto", password="12345")
    for i in range(22):
        title = "Article Title " + str(i)
        slug = "article-title-" + str(i)
        content = "Article content. This might be lengthy - " + str(i)
        online = random.choice([True, False])
        pub_dttm = datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 100))
        a = Article.objects.create(title=title, slug=slug, content=content, online=online, pub_dttm=pub_dttm,
                                   author=user)
        a.pub_dttm = pub_dttm
        if i % 7 == 0:  # create some articles with empty content
            a.content = ""
        a.save()
    print("22 Articles were created. Enjoy.")


def delete_test_user_and_all_articles():
    accept = input("This will delete all articles and the test user. Are you sure? (y/n)")
    if accept == "y":
        Article.objects.all().delete()
        User.objects.filter(username="dev_user_auto").delete()
        print("Deleted.")
    else:
        print("Aborted.")
