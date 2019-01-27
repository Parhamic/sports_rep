from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from .game import Game


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(state='PB')


class NewsPost(models.Model):
    SPORTS = (('FB', 'Football'),
              ('BB', 'Basketball'))
    STATES = (('DR', 'Draft'),
              ('PB', 'Published'),
              ('GR', 'Game Related'))
    sport = models.CharField(max_length=2, choices=SPORTS)
    title = models.CharField(max_length=64, unique=True)
    slug = models.SlugField(blank=True, unique=True)
    image = models.ImageField(blank=True, null=True,
                              upload_to='posts_pictures')
    context = models.TextField()
    state = models.CharField(max_length=2, choices=STATES)
    created = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game,
                             blank=True, null=True, on_delete=models.CASCADE)

    related_posts = models.ManyToManyField('self', blank=True)

    objects = models.Manager()
    published = PublishedManager()

    def get_absolute_url(self):
        return reverse('post_view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(NewsPost, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created', )


class Comment(models.Model):
    post = models.ForeignKey(
        NewsPost, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(
        'accounts.User', related_name='comments', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    active = models.BooleanField(default=False)

    def __str__(self):
        return '{} on {}'.format(self.author.username, self.post.title)

    class Meta:
        ordering = ('-created', )
