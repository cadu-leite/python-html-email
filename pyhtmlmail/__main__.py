import argparse

import sys


from pyhtmlmail.mail import EmailMsg


def command_line_parser(sys_args):

    parser = argparse.ArgumentParser(description='', fromfile_prefix_chars='@')

    parser.add_argument(
        '-o', '--host',
        required=True,
        type=str,
        help='smtp host'
    )
    parser.add_argument(
        '-p', '--port',
        required=True,
        type=str,
        help='smtp host port'
    )

    parser.add_argument(
        '-s', '--password',
        required=True,
        type=str,
        help='password'
    )
    parser.add_argument(
        '-f', '--mailfrom',
        required=True,
        type=str,
        help='from email address'
    )

    # fix: todo: for some reason, is works for command line lists of email addresses, but not for args file.
    parser.add_argument(
        '-t', '--mailto',
        type=str,
        nargs='+',
        required=False,
        help='to email adress(es) - 1 or "n"'
    )

    parser.add_argument(
        '-u', '--mailtolistfile',
        type=str,
        required=False,
        help='recipients list file'
    )

    parser.add_argument(
        '-x', '--contenttext',
        type=str,
        required=False,
        help='content - A Plain text message content'
    )

    parser.add_argument(
        '-m', '--contenthtml',
        type=str,
        required=False,
        help='content - A HTML message content - escape quotes for image tag `src` attribute value (ex: src=\"image path\")'
    )

    parser.add_argument(
        '-n', '--contenthtmlfile',
        type=str,
        required=False,
        help='content - A HTML file message content Template -  use `-f` or `-m` exclusively '
    )

    parser.add_argument(
        '-b', '--subject',
        type=str,
        required=False,
        help='Email subject - use "double quotes" ("") for frases  '
    )

    args = parser.parse_args(sys_args)
    return args

def main(sys_args):

    args = command_line_parser(sys_args)
    email = EmailMsg()
    email.host = args.host
    email.port = args.port
    email.from_sender = args.mailfrom
    email.to_recipient = args.mailto
    email.subject = args.subject
    email.password = args.password
    email.content_html = args.contenthtml  # args.content_html
    email.content_text = args.contenttext  # args.content_text
    email.content_html_file = args.contenthtmlfile

    email.send()


if __name__ == '__main__':
    args = command_line_parser(sys.argv[1:])
    main(sys.argv[1:])

