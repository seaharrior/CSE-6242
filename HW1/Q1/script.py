import sys
import requests
import time

start = time.time()

f1 = open("movie_ID_name.csv", 'w')
f2 = open("movie_ID_sim_movie_ID.csv", 'w')

api_key = str(sys.argv[1])

count = 0

total_similar_list = []

for page in range(18):
    page = page + 1
    api_link_drama = 'https://api.themoviedb.org/3/discover/movie?api_key={}&sort_by=popularity.desc&page={}&primary_release_date.gte=2004-01-01&with_genres=18'.format(
        api_key, page)
    request_drama = requests.get(api_link_drama)
    data_drama = request_drama.json()
    drama_movie_list = data_drama['results']
    for movie in drama_movie_list:
        count = count + 1
        print(count)
        print(time.time() - start)
        movie_id = movie['id']
        title = movie['title']
        if ',' in title:
            title = '"' + title + '"'
        drama_csv_string = str(movie_id) + ',' + title + '\n'
        if count <= 350:
            f1.write(drama_csv_string)
        if count % 35 == 0:
            time.sleep(10)
        api_link_similar = 'https://api.themoviedb.org/3/movie/{}/similar?api_key={}&language=en-US&page=1'.format(
            movie_id, api_key)
        request_similar = requests.get(api_link_similar)
        data_similar = request_similar.json()
        similar_movie_list = data_similar['results'][0:5]
        for similar in similar_movie_list:
            total_similar_list.append((movie_id, similar['id']))

exclude_list = [(id_m, id_s) for (id_m, id_s) in total_similar_list if
                (id_s, id_m) in total_similar_list and id_s >= id_m]
non_duplicate_list = [value for value in total_similar_list if value not in exclude_list]
[f2.write(str(id_m) + ',' + str(id_s) + '\n') for (id_m, id_s) in non_duplicate_list]
f1.close()
f2.close()
