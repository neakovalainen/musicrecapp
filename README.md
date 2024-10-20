# musicrecapp
The main idea of the website is to share what kind of music you like (songs/artists/genres) and to be able to see what music your friends like. 
Some functionalities that I've thought of so far:
- the user can sign in to their own account (and of course sign up when using for the first time)
- the user can make posts 
- the user can follow others
- the user can like their friends' posts 
- the user can personalize their profile bio

## What is the current situation of the app?
- the user can register their account
- the user can log in and log out
- there is a home page where the user can post text based messages
    - when the message is shown at the homepage, the user can see the time when the message was posted and who posted it
- from the homepage the user can add friends and access their profiles
    - if the user is viewing their own profile, they can change their bio
    - the user can only view the profiles of their friends
          - if the user is viewing their friend's profile, the user will see a bio that the friend wrote
- the posts that the user has liked are shown on their profiles 
- from the homepage the user can like posts
- the user can delete their own posts

## In the future
-I would like to add profile pictures
- possibility to delete likes and comment on posts
- like and friends counts on profiles


## How to use the app
Follow the instructions in the course materials.

1. Install dependencies with `pip install -r requirements.txt`
2. Create a database with Postgresql
3. Add `DATABASE_URL` and `SECRET_KEY` to your `.env` file
4. Add tables to your database with `psql < src/tables.sql`
5. Run the app with `flask --app src/app.py run`
