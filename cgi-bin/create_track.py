import cgi
import sys 
import os
import inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import db


msg = ''

form = cgi.FieldStorage()
artist_id = form.getfirst("artist_id")
track_title = form.getfirst("track_title")
track_duration = form.getfirst("track_duration")
if (artist_id is not None) and (track_title is not None) and (track_duration is not None):
    db.add_track(artist_id, track_title, track_duration)
    msg = '''
        <br>
        <div class="card">
            <div class="card-body">
                Трек успешно добавлен
            </div>
        </div>
    '''


artists = db.get_all_artists()
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
            <div class="ps-4 pe-4">
                <form method="GET">
                    <label class="form-label" for="artist_id">Имя артиста</label>
                    <select class="form-select" aria-label="Default select example" name="artist_id" required>
                        {artist_options}
                    </select>
                    <br>
                    <label class="form-label" for="track_title">Название трека</label>
                    <input class="form-control" type="text" name="track_title" required>
                    <br>
                    <label class="form-label" for="track_duration">Длительность трека (сек)</label>
                    <input class="form-control" type="number" name="track_duration" required>
                    <br>
                    <input type="submit" class="btn btn-primary">
                </form>

                {msg}
            </div>
        </body>
    </html>
'''

artist_options = ''
for artist in artists:
    artist_options += f'<option value="{artist[0]}">{artist[1]}</option>'

print("Content-Type: text/html\n")
print(template.format(msg=msg, artist_options=artist_options))