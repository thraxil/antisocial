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
* Celery/RabbitMQ fetch/parse pipeline (in the works. cronjob for now)

Built by Anders Pearson <anders@columbia.edu>

License: BSD
