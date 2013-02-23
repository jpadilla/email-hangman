import re
import json
import sendgrid

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from .utils import Hangman as HangmanGame, generate_ascii
from .models import Hangman


def index(request):
    hangman = HangmanGame('hello')
    print ' '.join(hangman.keys)

    ascii = """
     __________
    |         |
    |         0
    |        /|\\
    |        / \\
    |
    |
    """
    print ascii

    return HttpResponse('Hello World')


@csrf_exempt
def webhook(request):
    # make a secure connection to SendGrid
    s = sendgrid.Sendgrid(settings.SENDGRID_USERNAME,
        settings.SENDGRID_PASSWORD, secure=True)

    post_data = request.POST
    envelope = json.loads(post_data['envelope'])
    subject = post_data['subject'].lower().strip()
    body_text = post_data['text']
    body_text_list = [line.lower().strip() for line in body_text.splitlines()]

    if 'create' in subject:
        player = body_text_list[0]
        word = body_text_list[1]

        Hangman.objects.create(sender=envelope['from'],
            player=player, word=word)

    elif ('re:' in subject and 'play' in subject) or ('re:' in subject and 'playing' in subject):
        email_pattern = re.compile("[-a-zA-Z0-9._]+@[-a-zA-Z0-9_]+.[a-zA-Z0-9_.]+")
        emails = re.findall(email_pattern, subject)
        email = emails[0]
        letter = body_text_list[0][0]

        h = Hangman.objects.get(sender=email, player=envelope['from'])
        used_letters = h.used_letters.split(',')
        keys = list(h.keys)

        if h.mistakes < 5:
            if letter in h.word:
                match = True
                indexes = [i for i, item in enumerate(h.word) if item == letter]
                for index in indexes:
                    keys[index] = letter
                    used_letters.append(letter)
            else:
                # guessed letter didn't match
                used_letters.append(letter)
                h.mistakes += 1
                match = False

            _keys = ''
            for key in keys:
                if key != '':
                    _keys += key
                else:
                    _keys += '_'

            h.keys = _keys
            h.used_letters = ','.join(set(used_letters))
            h.save()

            if match:
                if h.word == h.keys:
                    ascii_message = """
                    YOU WIN!

                        .-~~~~~~-.
                      .'          '.
                     /   O      O   \\
                    :                :
                    |                |
                    : ',          ,' :
                     \  '-......-'  /
                      '.          .'
                        '-......-'

                    The word was %s
                    """ % h.word

                    # make a message object
                    message = sendgrid.Message(
                        settings.SENDGRID_FROM,
                        'Playing Hangman game by %s' % h.sender,
                        ascii_message
                    )

                    # add a recipient
                    message.add_to(h.player)

                    h.delete()
                else:
                    ascii_message = """
                    Doing good!

                    You played the letter: %s

                    %s

                    Used Letters: %s

                    """ % (letter, ' '.join(keys), ', '.join(set(used_letters)))
                    ascii_message += generate_ascii(h.mistakes)

                    # make a message object
                    message = sendgrid.Message(
                        settings.SENDGRID_FROM,
                        'Playing Hangman game by %s' % h.sender,
                        ascii_message
                    )

                    # add a recipient
                    message.add_to(h.player)

                # use the Web API to send your message
                s.web.send(message)

            if not match and (h.mistakes >= 1 and h.mistakes <= 5):
                ascii_message = """
                Ouch!

                You played the letter: %s

                %s

                Used Letters: %s

                """ % (letter, ' '.join(keys), ', '.join(set(used_letters)))
                ascii_message += generate_ascii(h.mistakes)

            if not match and h.mistakes > 0:
                # make a message object
                message = sendgrid.Message(
                    settings.SENDGRID_FROM,
                    'Playing Hangman game by %s' % h.sender,
                    ascii_message
                )

                # add a recipient
                message.add_to(h.player)

                # use the Web API to send your message
                s.web.send(message)

        else:
            # loss
            ascii_message = """
            Sorry you lost!

                 .-~~~~~~-.
               .'          '.
              /   O      O   \\
             :           `    :
             |                |
             :    .------.    :
              \  '        '  /
               '.          .'
                 '-......-'

            The word was: %s

            """ % h.word
            ascii_message += generate_ascii(6)

            # make a message object
            message = sendgrid.Message(
                settings.SENDGRID_FROM,
                'You lost',
                ascii_message
            )

            # add a recipient
            message.add_to(h.player)

            # use the Web API to send your message
            s.web.send(message)

            h.delete()

    return HttpResponse('Hello Webhook')
