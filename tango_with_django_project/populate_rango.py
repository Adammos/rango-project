import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tango_with_django_project.settings')

import django
django.setup()

from rango.models import Category, Page

def populate():
    python_cat = add_cat('Python',64,128)

    add_page(cat=python_cat,
            title="Official Python Tutorial",
            url="http://docs.python.org/2/tutorial/",
            views=3)

    add_page(cat=python_cat, 
            title="How to Think like a computer Scientist",
            url="http://www.greenteapress.com/thinkpython/",
            views=4)

    add_page(cat=python_cat,
            title="Learn Python in 10 minutes",
            url="http://www.korokithakis.net/tutorials/python/",
            views=1)

    django_cat = add_cat("Django",32,64)

    add_page(cat=django_cat,
            title="Official Django Tutorial",
            url="https://docs.djangooproject.com/en/1.5/intro/tutorial01")

    add_page(cat=django_cat,
            title="Django Rocks",
            url="http://www.djangorocks.com/")

    add_page(cat=django_cat,
            title="How to Tango with Django",
            url="http://www.tangowithdjango.com/")

    frame_cat = add_cat("Other Frameworks",16,32)

    add_page(cat=frame_cat,
            title="Bottle",
            url="http://bottlepy.org/docs/dev")

    add_page(cat=frame_cat,
            title="Flask",
            url="http://flask.pocoo.org")

    #print out what we have added to the user
    for c in Category.objects.all():
        for p in Page.objects.filter(category=c):
            print "- {0} - {1}".format(str(c), str(p))

def add_page(cat, title, url, views=0):
    p = Page.objects.get_or_create(category=cat, title=title)[0]
    p.url=url
    p.views=views
    p.save()
    return p

def add_cat(name,likes, views):
    c = Category.objects.get_or_create(name=name)[0]
    c.likes = likes
    c.views = views
    c.save()
    return c

if __name__ == '__main__':
    print "Starting Rango population script..."
    populate()
