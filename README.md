Kaverisovellus

- Käyttjät voivat luoda tilin sekä kirjatua sisään tai ulos.
- Käyttäjillä on oma profiili, jossa he voivat kertoa itsestä.
- Käyttäjät voivat muokata profiiliaan.
- Käyttäjät voivat katsoa muiden käyttäjien profiileita.
- Käyttäjät voivat lähetttää viestejä etusivulle.
- Käyttäjät voivat nähdä muiden käyttäjien viestit.

Sovelluksen käyttö Linuxilla:

- Luo kansion friendapp juureen .env tiedosto seuraavanlaisesti:

DATABASE_URL=postgresql://<käyttäjä>:<salasana>@<host>:<port>/<tietokanta>
SECRET_KEY=<salainen_avain>

-Kirjoita terminaaliin seuraavat komennot:

$cd friendapp
$python3 -m venv venv
$source venv/bin/activate
$pip install flask
$pip install flask-sqlalchemy
$pip install psycopg2-binary
$pip install python-dotenv
$flask run

