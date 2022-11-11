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
dance_title = form.getfirst("dance_title")
dance_difficulty = form.getfirst("dance_difficulty")
track_id = form.getfirst("track_id")
if (dance_title is not None) and (dance_difficulty is not None) and (track_id is not None):
    db.add_dance(dance_title, dance_difficulty, track_id)
    msg = '''
        <br>
        <div class="card">
            <div class="card-body">
                Танец успешно добавлен
            </div>
        </div>
    '''


tracks = db.get_all_tracks_joined()
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
            <h1>Создание танца</h1>
            <a class="h3 link-primary" href="/">На главную</a>
            <div class="ps-4 pe-4">
                <form method="GET">
                    <label class="form-label" for="track_id">Трек</label>
                    <select class="form-select" aria-label="Default select example" name="track_id" required>
                        {track_options}
                    </select>
                    <br>
                    <label class="form-label" for="dance_title">Название танца</label>
                    <input class="form-control" type="text" name="dance_title" required>
                    <br>
                    <label class="form-label" for="dance_difficulty">Сложность танца</label>
                    <input class="form-control" type="number" name="dance_difficulty" required>
                    <br>
                    <input type="submit" class="btn btn-primary">
                </form>

                {msg}
            </div>
        </body>
    </html>
'''

track_options = ''
for track in tracks:
    track_options += f'<option value="{track[0]}">{track[1]}</option>'

print("Content-Type: text/html\n")
print(template.format(msg=msg, track_options=track_options))