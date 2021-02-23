'''
test shell call

    python -m pyhtmlmail --host smtp.gmail.com --port 465 --password "xxxxx" --mailfrom "emailfrom@mail.com.br" --mailto mail01@mail.com.br mail02@mail.com  --contenttext "Hi there, its an email" --contenthtml "<html><head><style></style></head><body><h1>Titulo email teste</h1><table align='center' role='presentation' cellspacing='0' cellpadding='0' border='0' width='100%' style='margin: auto;'><tr><tb><img src=\"pyhtmlmail/images/feliz_aniversario_cartao.png\"></td></tr><tr><td><img src=\"pyhtmlmail/images/feliz_aniversario_code.png\"></td></tr></table></body></html>" --subject "PyHtmlMail Test Email"

'''


import unittest

import shutil
import tempfile

from os import path

from unittest import mock

from pyhtmlmail import __main__
from pyhtmlmail.mail import EmailMsg

import csv

from email.mime.multipart import MIMEMultipart

CONTENT_HTML = '''
<html>
    <head>
        <style></style>
    </head>
    <body>
        <h1>Titulo email teste</h1>
        <table align='center' role='presentation' cellspacing='0' cellpadding='0' border='0' width='100%' style='margin: auto;'>
        <tr><td>
            <img src="pyhtmlmail/images/feliz_aniversario_cartao.png">
        </td></tr>
        <tr><td>
            <img src="pyhtmlmail/images/feliz_aniversario_code.png">
        </td></tr>
        </table>
    </body>
</html>
'''

ADDRESSES = '''
Mr. W. Yeats; w.yeats@mail.com; Mail to the poetry
Ex. Visc. de Mauá; irineu.souza@mail.com; Mail to the entrepreneur
Ms Ada Lovelace; ada.love@mail.com; Mail to Ms Lovelace, a talented mathematician and programmer!
Ex Marques De Pombal; sebastiao.melo@mail.com; Mail to the Prime Minister
Mr Guido van Rossum; guido.rossum@mailcom; Mail to the creator of Python Language
Ms Jane Austen; jane.proud@mail.com; Mail to a great writer and thinker
'''

class TestClass(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        f = open(path.join(self.temp_dir, 'temp.html'), 'w')
        f.write(CONTENT_HTML)
        f.close()
        self.temp_file_path = path.join(self.temp_dir, 'temp.html')


    def tearDown(self):
        # deletes the temp dir (and all content)
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_instantiate(self):
        '''
        Instance is initialize correctly
        '''
        em = EmailMsg()
        self.assertIsInstance(em._msg, MIMEMultipart)

    def test_content_html_parsed_on_set_content_html(self):
        '''
        Check images parsed when `content_html` is set
        '''
        em = EmailMsg()
        em.content_html = CONTENT_HTML
        images = ['pyhtmlmail/images/feliz_aniversario_cartao.png', 'pyhtmlmail/images/feliz_aniversario_code.png']
        check = [img for cid, img in em._images_cids]
        # self.assertIn(images[0], check)
        # self.assertIn(images[1], check)
        # self.assertEqual(len(em._images_cids), 2)
        self.assertTrue(all([
            images[0] in check,
            images[1] in check,
            len(em._images_cids) == 2]))
        # when using ... self.assertListEqual(check, list) error ...
        # First differing element 0:
        # 'pyhtmlmail/images/feliz_aniversario_code.png'
        # 'pyhtmlmail/images/feliz_aniversario_cartao.png'

        # - ['pyhtmlmail/images/feliz_aniversario_code.png',
        # -  'pyhtmlmail/images/feliz_aniversario_cartao.png']
        # ? ^                                                ^

        # + ['pyhtmlmail/images/feliz_aniversario_cartao.png',
        # ? ^                                                ^

        # +  'pyhtmlmail/images/feliz_aniversario_code.png']

    def test_content_html_parsed_on_set_content_html_file(self):
        '''Check images parsed when `content_html_file` is set'''
        em = EmailMsg()
        em.content_html_file = self.temp_file_path
        images = ['pyhtmlmail/images/feliz_aniversario_cartao.png', 'pyhtmlmail/images/feliz_aniversario_code.png']
        check = [img for cid, img in em._images_cids]
        self.assertTrue(all([
            images[0] in check,
            images[1] in check,
            len(em._images_cids) == 2]))

    def test_content_html_setter_is_called(self):
        '''
        swap IMG `src` by cid when `_content_html_file` is set
        '''
        with mock.patch('pyhtmlmail.mail.EmailMsg.content_html', new_callable=mock.PropertyMock) as content_html_patched:
            emsg = EmailMsg()  # I believe this make one call to setter
            content_html_patched.reset_mock()  # ... so  <<<< todo: check TRICKY! ?!?!
            emsg.content_html_file = self.temp_file_path
            content_html_patched.assert_called()

    def test_send_smtp_called(self):
        '''
        swap IMG `src` by cid when `_content_html_file` is set
        '''
        with mock.patch('pyhtmlmail.mail.EmailMsg.smtp') as smtp_patched:
            emsg = EmailMsg()  # I believe this make one call to setter
            emsg.send()
            emsg.content_html_file = self.temp_file_path
            smtp_patched.assert_called()

    def test_csv_addresses_reading(self):
        '''
        given a CSV with name, email, personal content must return a list of namedtuples with those fields
        '''
        f = open(path.join(self.temp_dir, 'temp_addresses.csv'), 'w')
        f.write(ADDRESSES)
        f.close()

        with open(path.join(self.temp_dir, 'temp_addresses.csv')) as csvfile:
            csv_dialect = csv.Sniffer().sniff(csvfile.read())
            csv_reader = csv.reader(csvfile, csv_dialect)

            print(f'==>>[] self.temp_dir => [{self.temp_dir}]')
            
            print(f'==>>[] dialect => [{csv_dialect}]')
            print(f'==>>[] reader => [{csv_reader}]')

            for row in csv_reader:
                print('==============')
                print('\,'.join(row))
            print('==============')
            print(csvfile.read())


