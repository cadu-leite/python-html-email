*****************
Python Email HTML
*****************


+------------------------+----------------------+--------------------+---------------------+
| Pypi Version           | Doc Status           | Coverage           | Downloads           |
+========================+======================+====================+=====================+
|  no pack               |  no docs             |  |badge_coverage|  |  no pypo yet        |
+------------------------+----------------------+--------------------+---------------------+



Envio de email com conteúdo HTML e imagens.

#. Prepare um template HTML
     #) Pode conter imagens, com paths relativos ao arquivo HTML (trabalhe normalmente)
#. Tenha em mãos
     #) Um servidor `smtp` (ex: Google-> `smtp.google,com`)
     #) #) A porta SMTP (ex. Google -> )
     #) Uma conta & senha (ex.: seu email@gmail.com & senha)
#. LIsta de emails para enivo 
     

USO
===


+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| Param   (Abv)          | Param             | descrição                                                                                                    |
+========================+===================+==============================================================================================================+
| -h                     | --help            | show this help message and exit                                                                              |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| -p PASSWORD            | --password        | password                                                                                                     |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| -f MAILFROM            | --mailfrom        | from email address                                                                                           |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| -t MAILTO [MAILTO ...] | --mailto          | to email adress(es) - 1 or "n"                                                                               |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| -x CONTENTTEXT         | --contenttext     | content - A Plain text message content                                                                       |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| -m CONTENTHTML         | --contenthtml     | content - A HTML message content - escape quotes for image tag `src` attribute value  (ex: src="image path") |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| -n CONTENTHTMLFILE     | --contenthtmlfile | content - A HTML file message content Template - use `-f` or `-m` exclusively                                |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+
| -s SUBJECT             | --subject         | Email subject - use "double quotes" ("") for frases                                                          |
+------------------------+-------------------+--------------------------------------------------------------------------------------------------------------+


..

Exemplo:

    python **-m** pyhtmlmail  **-f** <emailfrom>  **-t** <emailto * N>  **-p** <password>  **-n** <"template path">  **-x** <"mensagem de texto ">


Syntax:

    .. code-block:: bash

        $> python -m pyhtmlmail -s "teste envio" -f zenece@znc.com.br -t jose.dumb@email.com.br  silva.gomer@mail.com -p M3uP455_senha_password -n "/home/user/jose/html_mail/template/template_feliz_aniversario.html"  -x "textto plano"


Exemplo utilizando arquivo com argumentos... 

Aquivo:

.. warning:: 1 único argumento por linha. 

::

    --host=smtp.gmail.com
    --port=465
    --password=meupassword
    --mailfrom=meuemail@mail.com
    --mailto="mailpara@gmail.com"
    --contenttext="Olá - Boa tarde"
    --contenthtmlfile=pyhtmlmail/template/template_feliz_aniversario.html
    --subject="E-mail de teste"



Porque uma lib para envio de e-mail em formato HTML ?
=====================================================

Temos 2 desafios para enviar um email com HTML para formatar o conteúdo .


O primeiro, é a formatação
--------------------------

Em geral, um grid  CSS não funciona dentro de um leitor de email.

Mas este problema se resolve com `<table>` e design. ;) 


O segundo, imagens !
--------------------

Onde ficam as imagens ? 

Em uma página Web uma imagem fica hospedada em um servidor HTTP, 
e com uma URI é possível acessá-la. É possível hospedar uma imagem e usá-la com um link em uma mensagem de email, mas alguns leitores não irão carrgar. 

O problema, é para quem está escrevendo um email, primeiro ele precisa publicar aas imagens em um servidor. 

**Resumindo ...**

Temos 3 opções:
    #. Imagens "linkadas"
    #. Base64 (imagens embedadas em base 64)
    #. Content ID - (Imagens "anexas" e referenciadas no HTML como parte do conteúdo.)
       

    .. warning:: **Este código usa a terceira opção.**

Todos os métodos tem prós e contras. 



Base64 - Inline:
    - Aumenta o tamanho do email (assim como CID)
    - A maioria dos leitores Web não aceita.
    - Bloqueado por completo no OutLook
     
Imagens Linkadas:
    - Mesmo situação de bloqueio de Web readers
    - Requer download da imagem.



Objective
=========

easy send html email content for designers.


- ler aqruivos RFC822
- Multiple "Recipients"
- HTML templates content
- Custom message for recipients 
- Embed images automatically (throught CID)
- command line interface
- easy integration (Django, flask, other applications)


Keep it simple 

- less parameters
- good error messages

easy to use, easy to mantain

Especifictions
==============

RFC822 Format:
    ::

        From: someone@example.com
        To: someone_else@example.com
        Subject: An RFC 822 formatted message

        <body content after BLANK LINE>


Repients List:
    ::

        email address:
            content (may use HTML)

        email address:
            content (may use HTML)

        ...



https://github.com/lavr/python-emails
https://github.com/aspineux/pyzmail/
https://github.com/peterbe/premailer



.. |badge_coverage| image:: https://codecov.io/gh/cadu-leite/python-html-email/branch/main/graph/badge.svg?token=SCR7OQwsyb
    :target: https://codecov.io/gh/cadu-leite/python-html-email
    :alt: code coverage


