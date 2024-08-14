<h1>Kaverisovellus</h1>

- Käyttjät voivat luoda tilin sekä kirjatua sisään tai ulos.
- Käyttäjillä on oma profiili, jossa he voivat kertoa itsestä.
- Käyttäjät voivat muokata profiiliaan.
- Käyttäjät voivat katsoa muiden käyttäjien profiileita.
- Käyttäjät voivat lähetttää viestejä etusivulle.
- Käyttäjät voivat nähdä muiden käyttäjien viestit.
- Käyttäjät voivat kommentoida toisten viestejä
- Käyttäjät voivat lähettää kaveripyyntöjä
- Käyttäjät voivat hyväksyä tai hylätä toisten lähettämiä kaveripyyntöjä

<h2>Sovelluksen käyttö Linuxilla:</h2>

- Luo kansion friendapp juureen .env-tiedosto seuraavanlaisesti:<br>

DATABASE_URL=postgresql://käyttäjä:salasana@host:port/tietokanta<br>
SECRET_KEY=<salainen_avain><br>

- Kirjoita terminaaliin seuraavat komennot:

$cd friendapp <br>
$python3 -m venv venv <br>
$source venv/bin/activate <br>
$pip install flask <br>
$pip install flask-sqlalchemy <br>
$pip install psycopg2-binary <br>
$pip install python-dotenv <br>
$flask run <br>

