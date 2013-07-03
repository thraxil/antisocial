> RSS readers are not as clumsy or random as a Twitter client. An
  elegant weapon for a more civilized age. -- <cite>@marksiegal</cite>

Antisocial is a reader for the true feed junky. The focus is on
efficiently and swiftly gathering information from hundreds of feeds
and feeding it to you in a streamlined manner. No share buttons, no
seeing what feeds your friends are reading. Those things just slow you
down. Antisocial is for information directly to your brain via your
eyeballs (best we can do until we get a direct neural interface
working).

Antisocial's opinions:

* one central stream that merges entries from all feeds
* feed entries are presented in chronological order
* 'j' and 'k' keys for moving through the stream. 'r' to reload and
  fetch any new items.
* every UI element that is not necessary for reading and processing
  large numbers of entries is eliminated.

Technology:

* Django backend (running on Ubuntu and PostgreSQL)
* Python feedparser module does the heavy lifting on parsing feeds
* Backbone.js frontend
* Celery/RabbitMQ fetch/parse pipeline

Built by Anders Pearson <anders@columbia.edu>

License: BSD

I've had a few requests for screenshots. Antisocial is purposely quite
minimal and design-wise it's pretty much just a standard Bootstrap
application, so I haven't seen much point in it. Still people keep
asking, so here's what it looks like:

[![Main Screen](http://reticulum.thraxil.org/image/8e1b05b1bcacf0dc2b004e5a4217f5eff9607a6c/600w/image.png)](http://reticulum.thraxil.org/image/8e1b05b1bcacf0dc2b004e5a4217f5eff9607a6c/full/image.png)

[![Subscriptions](http://reticulum.thraxil.org/image/10fb5d2583a388552e4dccb242f2fb68e04cbd57/600w/image.png)](http://reticulum.thraxil.org/image/10fb5d2583a388552e4dccb242f2fb68e04cbd57/full/image.png)

![add feed](http://reticulum.thraxil.org/image/413788efa82b5bb6328ef12193c92c7400df6509/full/image.png)

![add opml](http://reticulum.thraxil.org/image/e607029f5d686bbc817fb403dd8ccbd8826c3a7a/full/image.png)
