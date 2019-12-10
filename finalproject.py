import json
import sys
import requests
import secret
from bs4 import BeautifulSoup
import sqlite3
from flask import Flask, render_template, request

API_KEY = secret.API_KEY
DBNAME = 'movies.db'

CACHE_FNAME = 'cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()


except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)


    if unique_ident in CACHE_DICTION:

        return CACHE_DICTION[unique_ident]


    else:
        
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]



class Genre:

    def __init__(self, genre=""):

        if genre=="":
            myinput = input("Welcome to the movie database.  Please enter a movie genre you would like to search for: \n")
            self.genre=myinput
        else:
            self.genre=genre

    def myGenre(self):

        variable = self.genre
        return variable


    def userSearch(self):
        genre = self.genre
        url = "https://www.imdb.com/search/title/?title_type=feature&genres=" + genre + "&count100"
        #resp = requests.get(url)
        resp = make_request_using_cache(url)
        soup = BeautifulSoup(resp, 'html.parser')
        #soup = BeautifulSoup(resp.text, 'html.parser')


        movieurllist = []
        movietitlelist = []
        movielistdict = {}
        s= soup.find_all('h3', class_="lister-item-header")
        for x in s:
            s2 = x.find_all('a')
            for item in s2:
                movieurllist.append("https://www.imdb.com" + item.get('href'))
                movietitlelist.append(item.text)
                k=item.text
                v ="https://www.imdb.com" + item.get('href')
                movielistdict[k] = v
        return movielistdict

    def scrapePageDataForEachMovie(self):

        imdb_results = self.userSearch()

        page_results_dict = {}

        final_movie_list = []
        movie_list = []

        title_list=[]
        year_list=[]
        duration_list=[]
        imdb_rating_list=[]
        country_list=[]
        advisory_rating_list=[]



        title_year_list = []
        for k,v in imdb_results.items():
            url = v
            #resp = requests.get(url)
            resp = make_request_using_cache(url)
            #soup = BeautifulSoup(resp.text, 'html.parser')
            soup = BeautifulSoup(resp, 'html.parser')

            #title/year of release
            h1 = soup.find_all('h1')
            for item in h1:
                itemss = item.text
                title = itemss[:-7]
                newtitle = title.replace('\xa0', '')
                year = itemss[-6:-2]
                title_list.append(newtitle)
                year_list.append(year)
                #print(newtitle)
                #print(year)
                #title_year_list.append(item.text)
            #print(title_year_list)


            #movie length
            dur = soup.find_all('time')
            movie_length=""
            for t in dur:
                movie_length =t.text.strip()
                #movie_dict["Duration"] = movie_length
            if movie_length != "":
                duration_list.append(movie_length)
            elif movie_length == "":
                duration_list.append("N/A")
            else:
                duration_list.append("N/A")
                #print(movie_length)

            #imdb rating

            imdb_rtg = soup.find_all("span", itemprop="ratingValue")
            var_rtg=""
            for r in imdb_rtg:
                var_rtg=r.text

            if var_rtg != "":
                imdb_rating_list.append(var_rtg)
            elif var_rtg =="":
                imdb_rating_list.append("N/A")
            else:
                imdb_rating_list.append("N/A")
                #print(r.text)
                #movie_dict["IMDB_Rating"] = r.text




            #country
            country = soup.find_all('h4', text = "Country:")
            cntrylist=[]
            for c in country:
                ccc = c.findNext('a')
                cc = ccc.text
                country_list.append(cc)
                #print(cc)
                #movie_dict["Country"]=cc

            #advisory rating

            try:
                cert = soup.find('a', text=" See all certifications")
                #print(cert)
                #for crt in cert:


                url_adv_rtg = cert.get('href')
                url2 = "https://www.imdb.com" + url_adv_rtg
                #print(url2)
                #resp2 = requests.get(url2)
                resp2 = make_request_using_cache(url2)
                soup2 = BeautifulSoup(resp2, 'html.parser')
                #soup2 = BeautifulSoup(resp2.text, 'html.parser')
                rating=""

                if soup2.find_all(text="United States:G") != []:
                    rating= "G"
                    advisory_rating_list.append(rating)
                            #rating_string = ss[0]
                            #print(rating_string[14:])
                elif soup2.find_all(text="United States:PG") != []:
                    rating= "PG"
                    advisory_rating_list.append(rating)
                elif soup2.find_all(text="United States:PG-13") != []:
                    rating= "PG-13"
                    advisory_rating_list.append(rating)
                elif soup2.find_all(text="United States:R") != []:
                    rating= "R"
                    advisory_rating_list.append(rating)
                elif soup2.find_all(text="United States:NC-17") != []:
                    rating= "NC-17"
                    advisory_rating_list.append(rating)
                elif soup2.find_all(text="United States:Approved") != []:
                    rating= "Approved"
                    advisory_rating_list.append(rating)
                else:
                    advisory_rating_list.append("N/A")
            except:
                advisory_rating_list.append("N/A")



                #print(rating)
                #movie_dict["Advisory_Rating"] = rating
                #final_movie_list.append(movie_dict)

        #print(title_list)
        #print(year_list)
        #print(duration_list)
        #print(imdb_rating_list)
        #print(country_list)
        #print(advisory_rating_list)


        print(advisory_rating_list)
        print(imdb_rating_list)
        print(duration_list)
        for ii in range(len(title_list)):
            movie_dict = {}
            movie_dict["Title"]=title_list[ii]
            movie_dict["Release_Year"]=year_list[ii]
            movie_dict["Duration"]=duration_list[ii]
            movie_dict["IMDB_Rating"]=imdb_rating_list[ii]
            movie_dict["Country"]=country_list[ii]
            movie_dict["Advisory_Rating"]=advisory_rating_list[ii]
            movie_list.append(movie_dict)

        #print(movie_list)
        return movie_list


    def getOmdbData(self):

        imdb_results = self.userSearch()
        resp_list=[]

        for k,v in imdb_results.items():
            imdb_id =v[27:36]


            #make_request_using_cache
            #movie_title = k
            #resp = requests.get("http://www.omdbapi.com/?apikey=" + API_KEY + "&i=+" + imdb_id)
            resp=make_request_using_cache("http://www.omdbapi.com/?apikey=" + API_KEY + "&i=+" + imdb_id)
            #resp_list.append(resp.json())
            #.append(resp)
            resp_list.append(json.loads(resp))
            #respjs = resp.json()
            #resp_list.append(respjs)
        return resp_list




        #print(resp.json())

        #return print(imdb_results)

    def init_db(self):
        conn = sqlite3.connect(DBNAME);
        cur = conn.cursor();


        statement ='''
            CREATE TABLE IF NOT EXISTS 'imdbMovies' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Title' TEXT NOT NULL,
                'ReleaseYear' TEXT NOT NULL,
                'Duration' TEXT NOT NULL,
                'imdbRating' TEXT NOT NULL,
                'Country' TEXT NOT NULL,
                'AdvisoryRating' TEXT NOT NULL
            );'''


        cur.execute(statement);
        conn.commit();

        statement ='''
            CREATE TABLE IF NOT EXISTS 'omdbMovies' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Title' TEXT NOT NULL,
                'Year' TEXT NOT NULL,
                'Rated' TEXT NOT NULL,
                'Released' TEXT NOT NULL,
                'Runtime' TEXT NOT NULL,
                'Genre' TEXT NOT NULL,
                'Director' TEXT NOT NULL,
                'Writer' TEXT NOT NULL,
                'Actors' TEXT NOT NULL,
                'Plot' TEXT NOT NULL,
                'Language' TEXT NOT NULL,
                'Country' TEXT NOT NULL,
                'Awards' TEXT NOT NULL,
                FOREIGN KEY(Title) REFERENCES imdbMovies(Title),
                FOREIGN KEY(Year) REFERENCES imdbMovies(ReleaseYear)
            );'''


        cur.execute(statement);
        conn.commit();
        conn.close();

    def insertOmdbData(self):

        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        #OMDB lists
        omdb_list = []

        o_Title=[]
        o_Year=[]
        o_Rated=[]
        o_Released=[]
        o_Runtime=[]
        o_Genre=[]
        o_Director=[]
        o_Writer=[]
        o_Actors=[]
        o_Plot=[]
        o_Language=[]
        o_Country=[]
        o_Awards=[]



        omdb_dict = self.getOmdbData()



        #print("Type =")
        #print(omdb_dict)

        for item in omdb_dict:
            o_Title.append(item['Title']);
            o_Year.append(item['Year']);
            o_Rated.append(item['Rated']);
            o_Released.append(item['Released']);
            o_Runtime.append(item['Runtime']);
            o_Genre.append(item['Genre']);
            o_Director.append(item['Director']);
            o_Writer.append(item['Writer']);
            o_Actors.append(item['Actors']);
            o_Plot.append(item['Plot']);
            o_Language.append(item['Language']);
            o_Country.append(item['Country']);
            o_Awards.append(item['Awards']);

        omdb_list = tuple(zip(o_Title, o_Year, o_Rated, o_Released, o_Runtime, o_Genre, o_Director, o_Writer, o_Actors, o_Plot, o_Language, o_Country, o_Awards));
        #print("HERE:")
        #print(omdb_list)
        #print(type(imdb_dict))

        for i in omdb_list:
            insertion = (None, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12])
            statement = 'INSERT INTO "omdbMovies" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)

        conn.commit()
        conn.close()

    def insertImdbData(self):

        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        #IMDB lists
        imdb_list=[]

        i_Title = []
        i_ReleaseYear = []
        i_Duration=[]
        i_imdbRating=[]
        i_Country=[]
        i_AdvisoryRating=[]

        imdb_dict = self.scrapePageDataForEachMovie()

        for itm in imdb_dict:
            i_Title.append(itm['Title'])
            i_ReleaseYear.append(itm['Release_Year'])
            i_Duration.append(itm['Duration'])
            i_imdbRating.append(itm['IMDB_Rating'])
            i_Country.append(itm['Country'])
            i_AdvisoryRating.append(itm['Advisory_Rating'])

        imdb_list = tuple(zip(i_Title, i_ReleaseYear, i_Duration, i_imdbRating, i_Country, i_AdvisoryRating))

        for ii in imdb_list:
            insertion = (None, ii[0], ii[1], ii[2], ii[3], ii[4], ii[5])
            statement = 'INSERT INTO "imdbMovies" '
            statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
            cur.execute(statement, insertion)

        conn.commit()
        conn.close()

    def getDbData(self):

        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement ="SELECT imdbMovies.Title, imdbMovies.ReleaseYear, imdbMovies.Duration, imdbMovies.AdvisoryRating, imdbMovies.Country, imdbMovies.imdbRating, omdbMovies.Language, omdbMovies.Director, omdbMovies.Actors, omdbMovies.Plot FROM imdbMovies JOIN omdbMovies ON omdbMovies.Title = imdbMovies.Title;"


        cur.execute(statement)

        final_movie_list = cur.fetchall()

        conn.commit()
        conn.close()
        return final_movie_list



    def sortAdvisory(self):

        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement ="SELECT imdbMovies.Title, imdbMovies.ReleaseYear, imdbMovies.Duration, imdbMovies.AdvisoryRating, imdbMovies.Country, imdbMovies.imdbRating, omdbMovies.Language, omdbMovies.Director, omdbMovies.Actors, omdbMovies.Plot FROM imdbMovies JOIN omdbMovies ON omdbMovies.Title = imdbMovies.Title ORDER BY imdbMovies.AdvisoryRating;"


        cur.execute(statement)

        advisory_sort_list = cur.fetchall()

        conn.commit()
        conn.close()
        return advisory_sort_list

    def sortReleaseYear(self):

        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement ="SELECT imdbMovies.Title, imdbMovies.ReleaseYear, imdbMovies.Duration, imdbMovies.AdvisoryRating, imdbMovies.Country, imdbMovies.imdbRating, omdbMovies.Language, omdbMovies.Director, omdbMovies.Actors, omdbMovies.Plot FROM imdbMovies JOIN omdbMovies ON omdbMovies.Title = imdbMovies.Title ORDER BY imdbMovies.ReleaseYear;"


        cur.execute(statement)

        year_sort_list = cur.fetchall()

        conn.commit()
        conn.close()
        return year_sort_list

    def sortDuration(self):

        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement ="SELECT imdbMovies.Title, imdbMovies.ReleaseYear, imdbMovies.Duration, imdbMovies.AdvisoryRating, imdbMovies.Country, imdbMovies.imdbRating, omdbMovies.Language, omdbMovies.Director, omdbMovies.Actors, omdbMovies.Plot FROM imdbMovies JOIN omdbMovies ON omdbMovies.Title = imdbMovies.Title ORDER BY imdbMovies.Duration;"


        cur.execute(statement)

        dur_sort_list = cur.fetchall()

        conn.commit()
        conn.close()
        return dur_sort_list

    def sortLanguage(self):

        conn = sqlite3.connect(DBNAME)
        cur = conn.cursor()

        statement ="SELECT imdbMovies.Title, imdbMovies.ReleaseYear, imdbMovies.Duration, imdbMovies.AdvisoryRating, imdbMovies.Country, imdbMovies.imdbRating, omdbMovies.Language, omdbMovies.Director, omdbMovies.Actors, omdbMovies.Plot FROM imdbMovies JOIN omdbMovies ON omdbMovies.Title = imdbMovies.Title ORDER BY omdbMovies.Language;"


        cur.execute(statement)

        lang_sort_list = cur.fetchall()

        conn.commit()
        conn.close()
        return lang_sort_list






def deleteData():

    conn = sqlite3.connect(DBNAME)
    cur = conn.cursor()

    statement ="DELETE FROM imdbMovies;"
    cur.execute(statement)
    conn.commit()

    statement ="DELETE FROM omdbMovies;"
    cur.execute(statement)
    conn.commit()


    conn.close()



#inst = Genre()

#inst.init_db()
#inst.insertOmdbData()
#inst.insertImdbData()
#inst.sortAdvisory()

#inst.getDbData()
#inst.scrapePageDataForEachMovie()



app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template("index.html")

@app.route('/movie_results', methods=['GET', 'POST'])
def movie_results():

    if request.method == 'POST':
        genre = request.form['genre']
    else:
        genre=""



    inst = Genre(genre)
    inst.init_db()
    inst.insertOmdbData()
    inst.insertImdbData()
    mygenre = inst.myGenre()
    db_list = inst.getDbData()

    return render_template("movie_results.html", genre=mygenre, your_list=db_list)

@app.route('/retry', methods=['GET', 'POST'])
def retry():
    deleteData()
    return render_template("retry.html")

@app.route('/movie_advisory_sort', methods=['GET', 'POST'])
def movie_advisory_sort():

    if request.method == 'POST':
        genre = request.form['genre']
    else:
        genre=""

    deleteData()

    inst = Genre(genre)
    inst.init_db()
    inst.insertOmdbData()
    inst.insertImdbData()
    mygenre = inst.myGenre()
    adv_list = inst.sortAdvisory()

    return render_template("movie_advisory_sort.html", genre=mygenre, your_list=adv_list)

@app.route('/movie_language_sort', methods=['GET', 'POST'])
def movie_language_sort():

    if request.method == 'POST':
        genre = request.form['genre']
    else:
        genre=""

    deleteData()

    inst = Genre(genre)
    inst.init_db()
    inst.insertOmdbData()
    inst.insertImdbData()
    mygenre = inst.myGenre()
    lang_list = inst.sortLanguage()

    return render_template("movie_language_sort.html", genre=mygenre, your_list=lang_list)

@app.route('/movie_year_sort', methods=['GET', 'POST'])
def movie_year_sort():

    if request.method == 'POST':
        genre = request.form['genre']
    else:
        genre=""

    deleteData()

    inst = Genre(genre)
    inst.init_db()
    inst.insertOmdbData()
    inst.insertImdbData()
    mygenre = inst.myGenre()
    yr_list = inst.sortReleaseYear()

    return render_template("movie_year_sort.html", genre=mygenre, your_list=yr_list)

@app.route('/movie_duration_sort', methods=['GET', 'POST'])
def movie_duration_sort():

    if request.method == 'POST':
        genre = request.form['genre']
    else:
        genre=""

    deleteData()

    inst = Genre(genre)
    inst.init_db()
    inst.insertOmdbData()
    inst.insertImdbData()
    mygenre = inst.myGenre()
    dur_list = inst.sortDuration()

    return render_template("movie_year_sort.html", genre=mygenre, your_list=dur_list)



if __name__ == '__main__':
    print('starting Flask app', app.name)
    app.run(debug=True)
