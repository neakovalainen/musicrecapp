# musicrecapp
The main idea of the website is to share what kind of music you like (songs/artists/genres) and to be able to see what music your friends like. 
Some functionalities that I've thought of so far:
- the user can sign in to their own account (and of course sign up when using for the first time)
- the user can make posts (at least text based, not sure yet if image sharing is difficult to implement)
- the user can follow others
- the user can like their friends' posts (maybe also comment?)
- the user will get recommended music based on what their friends have posted (something very simple, I don't want to overdo it)
- i like the idea that the user could personalise their own profile, but I'm not yet sure 

what is the current situation of the app?
- the user can register their account
- the user can log in
    - currently logging in is possible just by simply pressing the button because i wanted to implement proper logging in at a later stage (meaning you can simply press log in without writing a username or a password)
- there is a home page where the user can post text based messages
    - when the message is shown at the homepage, the user can see the time when the message was sent
    - because logging in doesn't work properly yet, the user cannot see who posted the message as of now (@ghostposter placeholder)
- from the homepage the user can navigate to their profile
    - in profile there are written the fuctionalities i want to add 
    - again, because logging in doesn't yet work correctly, the profile will at this point look identical to all users
- from the homepage the user can log out
    - as of now it's just a href that takes the user to the logging in page
- at this point, the user cannot add friends
- the user cannot like any posts yet

## How to use the app
Follow the instructions in the course materials.

1. Install dependancies with `pip install -r requirements.txt`
2. Create a database with Postgresql
3. Add `DATABASE_URL` and `SECRET_KEY` to your `.env` file
4. Add tables to your database with `psql < src/tables.sql`
5. Run the app with `flask --app src/app.py run`