import sendgrid

from django.db import models
from django.conf import settings

from .utils import Hangman as HangmanGame, generate_ascii


class Hangman(models.Model):
    sender = models.EmailField()
    player = models.EmailField()
    word = models.CharField(max_length=255)
    used_letters = models.TextField(blank=True, null=True)
    keys = models.CharField(max_length=255)
    mistakes = models.IntegerField(default=0)

    def __unicode__(self):
        return self.word

    def save(self, *args, **kwargs):
        if not self.pk:
            # make a secure connection to SendGrid
            s = sendgrid.Sendgrid(settings.SENDGRID_USERNAME,
                settings.SENDGRID_PASSWORD, secure=True)

            hangman = HangmanGame(self.word)

            self.keys = ''.join(hangman.keys)

            used_letters = []

            for key in self.keys:
                if key != '_':
                    used_letters.append(key)

            self.used_letters = ','.join(set(used_letters))

            ascii_message = """
            %s

            """ % ' '.join(hangman.keys)

            ascii_message += generate_ascii(0)

            ascii_message += """

            How to play:
            Reply to this email and guess one letter. You'll get another email
            that will tell you if your letter was found or not in the word. If
            it doesn't match you'll get another part of the hangman body.
            """

            # make a message object
            message = sendgrid.Message(
                settings.SENDGRID_FROM,
                '%s invited you to play Hangman' % self.sender,
                ascii_message
            )

            # add a recipient
            message.add_to(self.player)

            # use the Web API to send your message
            s.web.send(message)

        return super(Hangman, self).save(*args, **kwargs)
