# recommendationShow
**COMP 4462 Data Mining – Final Project**

First, the user is accessing http://barkinkoroglu.pythonanywhere.com website. The user is expected to enter their username and log in. We checked the mock viewer data (viewer_df.csv) for the username they provided. If the username exists in the data, they are logged into the system.

![image](https://github.com/barkinkoroglu/recommendationShow/assets/54675420/9da96a7e-9f19-4937-a987-e0c8a3c6ea4b)

<p align="center">Figure 1. Login Page </p>

If such a username does not exist, we provide an error message as shown below and ask them to try again.

![image](https://github.com/barkinkoroglu/recommendationShow/assets/54675420/ab995443-e73b-4064-8670-28746459f2d4)

<p align="center">Figure 2. No data found Page </p>

When the user logs in, they are shown 5 shows based on the shows they have previously watched. These shows are randomly selected from the top 20 most-watched shows in their cluster.
 
 ![image](https://github.com/barkinkoroglu/recommendationShow/assets/54675420/28347231-3240-4715-b1ea-5465454bb261)

<p align="center">Figure 3. Recommendations Page </p>

The user can click on the desired show and see the most-watched shows associated with the opened show (up to a maximum of 7 shows) through association learning.
 
 ![image](https://github.com/barkinkoroglu/recommendationShow/assets/54675420/7d69ea16-1f33-4ca4-8ff6-9865c0639eab)

<p align="center">Figure 4. Similar Shows Page </p>

Flask Application Report
This report describes the outline and features of a Flask-based movie/TV show recommendation application. The application aims to provide personalized recommendations based on the content users have watched. The functionality is explained through the following steps:

<h1>Importing Required Libraries and Modules:</h1> Flask, pandas, sklearn, mlxtend, and other relevant libraries are included in the application.
Loading the Dataset: Data related to the content watched by users is loaded from the "viewer_df.csv" file. The dataset includes information such as movie/TV show titles, watch percentages, country details, and dates.

<h1>Data Preprocessing:</h1> Various preprocessing steps are performed on the dataset. These include converting date columns to datetime format, applying one-hot encoding to categorical data, and normalizing the data.

<h1>Creating the Clustering Model:</h1> The dataset is clustered based on user profiles using the KMeans algorithm to create a clustering model. This allows grouping users with similar viewing habits into the same cluster.

<h1>Generating Association Rules:</h1> Association rules are created based on users' viewing data using the Apriori algorithm. These rules provide insights into which other titles might interest users when they watch a specific movie/TV show.

<h1>Building the Web Interface:</h1> The Flask application presents a web interface where users can see recommendation results. Users enter their username and receive personalized recommendations based on their saved viewing data.

<h1>Displaying Recommendation Results:</h1> Using the user's viewing data and the clustering model, personalized recommendation results are presented to the user. These results are selected from titles watched by other users with similar viewing habits.

<h1>Showing Movie Details:</h1> When a user wants to view details of a recommended movie/TV show, the application provides this information. Details include a list of similar titles in the same genre and the poster of the corresponding movie/TV show.
<br> 
<br>
The application encompasses important steps such as loading a dataset, performing data processing steps, creating a clustering model, finding association rules, and enabling user interaction using Flask and related libraries. This report explains the overall functioning and key features of the Flask application.

