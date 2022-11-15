import sqlite3
con = sqlite3.connect("dances.db")

tables_whitelist = [
    'artists',
    'tracks',
    'dances'
]

def setup_tables():
    con.execute('''
        CREATE TABLE IF NOT EXISTS Artists(
            id_artist integer PRIMARY KEY,
            name TEXT,
            country TEXT,
            birthday TEXT
        );
    ''')
    con.execute('''
        CREATE TABLE IF NOT EXISTS Tracks(
            id_track integer PRIMARY KEY,
            id_artist integer,
            title TEXT,
            duration integer,
            FOREIGN KEY (id_artist)
                REFERENCES Artists(id_artist)
        );
    ''')

    con.execute('''
        CREATE TABLE IF NOT EXISTS Dances(
            id_dance integer PRIMARY KEY, 
            title TEXT,
            difficulty INTEGER,
            id_track INTEGER,
            FOREIGN KEY (id_track)
               REFERENCES Tracks(id_track)
        );
    ''')

def add_test_data():
    con.execute('''
        INSERT INTO Artists(name, country, birthday) VALUES
        ('Mishlawi', 'USA', '1996-09-25'),
        ('Lil Nas X', 'USA', '1999-04-09'),
        ('Верка Сердючка', 'UA', '1973-10-02')
    ''')

    con.execute('''
        INSERT INTO Tracks(id_artist, title, duration) VALUES
        (1, 'All Night', 192),
        (2, 'Industry Baby', 202),
        (3, 'Все будет хорошо', 254)
    ''')

    con.execute('''
        INSERT INTO Dances(title, difficulty, id_track) VALUES
        ('Shuffle', 4, 1),
        ('Hustle', 3, 2),
        ('Гопак', 5, 3)
    ''')
    con.commit()

def execute_fetch(sql):
    cur = con.cursor()
    cur.execute(sql)
    data = cur.fetchall()
    cur.close()
    return data

def execute_insert_commit(sql, data):
    cur = con.cursor()
    cur.execute(sql, data)
    con.commit()

def get_all_dances_joined():
    sql = '''
        SELECT Dances.id_dance, Dances.title as dance_title, difficulty, Tracks.title as track_title, duration, Artists.name as artist_name, birthday, country FROM Dances 
        JOIN Tracks ON Dances.id_track = Tracks.id_track 
        JOIN Artists ON Tracks.id_artist = Artists.id_artist
    '''
    return execute_fetch(sql)

def get_all_tracks_joined():
    sql = '''
        SELECT Tracks.id_track, Tracks.title as track_title, duration, Artists.name as artist_name, birthday, country FROM Tracks 
        JOIN Artists ON Tracks.id_artist = Artists.id_artist
    '''
    return execute_fetch(sql)

def get_all_artists():
    sql = '''
        SELECT id_artist, Artists.name as artist_name, birthday, country FROM Artists 
    '''
    return execute_fetch(sql)

def add_artist(name, birthday, country):
    sql = 'INSERT INTO Artists(name, country, birthday) VALUES (?, ?, ?)'
    execute_insert_commit(sql, (name, country, birthday))

def add_track(artist_id, title, duration):
    sql = 'INSERT INTO Tracks(id_artist, title, duration) VALUES (?, ?, ?)'
    execute_insert_commit(sql, (artist_id, title, duration))

def add_dance(title, difficulty, track_id):
    sql = 'INSERT INTO Dances(title, difficulty, id_track) VALUES (?, ?, ?)'
    execute_insert_commit(sql, (title, difficulty, track_id))
