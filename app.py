from datetime import datetime
import json
from pathlib import Path
import pickle
from flask import Flask, render_template, request, redirect, url_for, send_from_directory,jsonify
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import datetime as dt
import requests
import mlxtend
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import random

app = Flask(__name__)

viewer_df = pd.read_csv('static/viewer_df.csv')
api_key = 'a2f2ad9c67f9e9c271b7e838141417b6'


temp_df = pd.DataFrame()
temp_df['Country'] = viewer_df['Country']
temp_df['Title'] = viewer_df['Title']
temp_df['Percentage Watched'] = viewer_df['Percentage Watched']

date_convert = viewer_df.columns[viewer_df.columns.str.contains("Date Watched")]
viewer_df[date_convert] = viewer_df[date_convert].apply(pd.to_datetime)
# Converting the above mentioned column types from object to datetime format
viewer_df["Date Watched"].max()
today_date = dt.datetime(2023, 5, 31)
temp_df["LastWatchDays"] = (today_date - viewer_df["Date Watched"]).dt.days


temp_df= pd.get_dummies(temp_df)
#normalize data
scaler = StandardScaler()
scaler.fit(temp_df)
scaled_data = scaler.transform(temp_df)

kmeans_model = KMeans(n_clusters = 5)
kmeans_model.fit(scaled_data)
#add clusters to df
viewer_df["clusters"] = kmeans_model.labels_
temp_df["clusters"] = kmeans_model.labels_


    ######

features = ['Country', 'Title', 'Date Watched', 'Percentage Watched']
bcd = viewer_df[features].copy()
bcd = pd.get_dummies(bcd)

def create_apriori_datastructure(dataframe, username_col='Username', item_col='Title'):
  grouped = dataframe.groupby([username_col, item_col], as_index=False).size()
  apriori_datastructure = pd.pivot(data=grouped, index=username_col, columns=item_col, values='size').fillna(0).applymap(lambda x: 1 if x > 0 else 0)
  return apriori_datastructure

def get_rules(apriori_df, min_support=0.01):
    # Possibilities of all possible product combinations
    # We say that the products that can be watched together with a min 0.01 probability should come. the probability that each product will be watched together with each other. Applying apriori algorithm.
    frequent_itemsets = apriori(
        apriori_df, min_support=min_support, use_colnames=True)
    # Extracting Association Rules
    # We extract association rules by using the support metric from the dataset that we applied the apriori algorithm.
    rules = association_rules(
        frequent_itemsets, metric="support", min_threshold=min_support)
    return rules

def recommend_products(rules_df, product_id, rec_count=7):
    sorted_rules = rules_df.sort_values('lift', ascending=False)
    recommended_products = []

    for i, product in sorted_rules["antecedents"].items():
        for j in list(product):
            if j == product_id:
                # Check if product_id is not in the consequents list
                if product_id not in sorted_rules.iloc[i]["consequents"]:
                    recommended_products.append(
                        list(sorted_rules.iloc[i]["consequents"]))

    recommended_products = list({item for item_list in recommended_products for item in item_list})
    return recommended_products[:rec_count]

def get_golden_shot(target_id,rules):
    recomended_product_ids = recommend_products(rules, target_id)
    #print(f'Recommended Products: {recomended_product_ids}\nProduct Names: ')
    return recomended_product_ids

apriori_df = create_apriori_datastructure(viewer_df)
viewer_df_rules = get_rules(apriori_df)
viewer_df_rules.sort_values(by='lift',ascending=False)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')
    #return "Hello World"

@app.route('/recommend',methods = ['POST'])
def result():
    username = request.form['username']

    # Prepare user data for clustering
    user_data = viewer_df[viewer_df['Username'] == username]
    user_watched_title = user_data['Title']

    if user_data.empty:
        return render_template('userError.html', username=username)
        
    date_convert = user_data.columns[user_data.columns.str.contains("Date Watched")]
    user_data[date_convert] = user_data[date_convert].apply(pd.to_datetime)

    today_date = dt.datetime(2023, 5, 31)
    user_data["Date Watched"].max()
    user_data["Date Watched"] = (today_date - user_data["Date Watched"]).dt.days

    user_data_encoded = pd.get_dummies(user_data[features]).reindex(columns=bcd.columns, fill_value=0)

    # Find the cluster for the user
    user_cluster = kmeans_model.predict(user_data_encoded)[0]

    # Get viewers in the same cluster as the user
    cluster_viewers = viewer_df[viewer_df['clusters'] == user_cluster]

    # Count the occurrences of each title in the recommendations
    title_counts = cluster_viewers['Title'].value_counts()
    #title_counts = cluster_viewers[cluster_viewers['Title'] != user_watched_title]['Title'].value_counts()
    
    # Get the top 5 most frequent titles
    top_titles = title_counts.index[:20].tolist()  # Convert the top 20 titles to a list
    random.shuffle(top_titles)  # Shuffle the titles
    top_titles = top_titles[:5]  # Select the first 5 random titles.

     # Fetch movie poster URLs using The Movie DB API
    movie_posters = []
    for title in top_titles:
        movie_poster = get_tv_show_poster(title)
        movie_posters.append(movie_poster)


     # Render the recommendations template with the top_titles
    return render_template('recommend.html', username=username, recommendations=top_titles, posters=movie_posters,zip=zip)

def get_tv_show_poster(title):
    url = f'https://api.themoviedb.org/3/search/tv?api_key={api_key}&query={title}'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
        return poster_url

    url = f'https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={title}'
    response = requests.get(url)
    data = response.json()
    if data['results']:
        poster_path = data['results'][0]['poster_path']
        poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
        return poster_url
    return None

@app.route('/recommend/<title>')
def movie_details(title):
    similar_shows= get_golden_shot(title,viewer_df_rules)

    tittle_movie_poster = []
   
    movie_poster_title = get_tv_show_poster(title)
    tittle_movie_poster.append(movie_poster_title)

     # Fetch movie poster URLs using The Movie DB API
    movie_posters = []
    for titles in similar_shows:
        movie_poster = get_tv_show_poster(titles)
        movie_posters.append(movie_poster)

    return render_template('movie_details.html', tittle_movie_poster=tittle_movie_poster, title=title, similar_shows=similar_shows,posters=movie_posters,zip=zip)


if __name__ == '__main__':
   app.run(debug=True)
   