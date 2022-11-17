import cgi
import sys 
import os
import inspect
import xml.etree.ElementTree as ET
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import db


msg = ''

form = cgi.FieldStorage()
artist_name = form.getfirst("artist_name")
artist_birthday = form.getfirst("artist_birthday")
artist_country = form.getfirst("artist_country")
if (artist_name is not None) and (artist_birthday is not None) and (artist_country is not None):
    db.add_artist(artist_name, artist_birthday, artist_country)
    msg = '''
        <br>
        <div class="card">
            <div class="card-body">
                Артист успешно добавлен
            </div>
        </div>
    '''

artists_xml = form.getfirst("xml_file")
if artists_xml is not None:
    root = ET.fromstring(artists_xml.decode("utf-8"))
    success_cnt = 0
    for child in root:
        artist = {}
        for a_ch in child:
            if a_ch.tag == 'name':
                artist['name'] = a_ch.text
            if a_ch.tag == 'country':
                artist['country'] = a_ch.text
            if a_ch.tag == 'birthday':
                artist['birthday'] = a_ch.text
        if ('name' in artist) and ('country' in artist) and ('birthday' in artist):
            db.add_artist(artist['name'], artist['birthday'], artist['country'])
            success_cnt += 1

    msg = f'''
        <br>
        <div class="card">
            <div class="card-body">
                Успешно загружено {success_cnt} артистов
            </div>
        </div>
    '''

template = '''
    <!DOCTYPE html>
    <html lang="en-US">
        <head>
            <meta charset="UTF-8">
            <!-- CSS only -->
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
            <!-- JavaScript Bundle with Popper -->
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
        </head>
        <body>
            <h1>Создание артиста</h1>
            <a class="h3 link-primary" href="/">На главную</a>
            <div class="ps-4 pe-4">
                <form method="GET">
                    <label class="form-label" for="artist_name">Имя артиста</label>
                    <input class="form-control" type="text" name="artist_name" required>
                    <br>
                    <label class="form-label" for="artist_birthday">ДР артиста (yyyy-mm-dd)</label>
                    <input class="form-control" type="text" name="artist_birthday" required>
                    <br>
                    <label class="form-label" for="artist_country">Страна артиста</label>
                    <input class="form-control" type="text" name="artist_country" required>
                    <br>
                    <input type="submit" class="btn btn-primary">
                </form>

                {msg}
            </div>

             <h1>Загрузить из XML</h1>
             <div class="ps-4 pe-4">
                <form method="post" enctype="multipart/form-data">
                    <label class="form-label" for="xml_file">XML Файл</label>
                    <input class="form-control" name="xml_file" type="file" accept=".xml">
                    <br>
                    <input type="submit" class="btn btn-primary">
                </form>
             </div>
        </body>
    </html>
'''


print("Content-Type: text/html\n")
print(template.format(msg=msg))