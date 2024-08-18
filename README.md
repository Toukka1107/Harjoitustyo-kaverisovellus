<h1>Kaverisovellus</h1>

- Käyttäjät voivat luoda tilin sekä kirjautua sisään tai ulos.
- Käyttäjillä on oma profiili, jossa he voivat kertoa itsestä. Profiilia voi myös muokata.
- Käyttäjät voivat katsoa muiden käyttäjien profiileita.
- Käyttäjät voivat lähetttää viestejä etusivulle ja muut käyttäjät voivat katsoa niitä.
- Käyttäjät voivat kommentoida toisten viestejä.
- Käyttäjät voivat lähettää kaveripyyntöjä.
- Käyttäjät voivat hyväksyä tai hylätä toisten lähettämiä kaveripyyntöjä.

<h2>Tulevat toiminnot:</h2>

- Käyttäjät voivat muokata tai poistaa itse lähettämiään viestejä.
- Käyttäjät voivat ladata profiilikuvan. Tällä hetkellä profiilkuvan tilalla on pinkki ruutu.
- Jos kaksi käyttäjää ovat kavereita, profiilikuvan ylänurkassa näkyy pieni sydän.
- Käyttäjät voivat poistaa toisia käyttäjiä kavereista.

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

