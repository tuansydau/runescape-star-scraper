# Star Tracker

This is a web app that scrapes all existing shooting stars in Runescape detected with the shooting-stars plugin, and then filters out the star locations I hate the most. This app is what I used to get [my main account](https://oldschool.runescape.wiki/w/Money_making_guide/Mining_crashed_stars) to 99 mining, and [my group ironman](https://wiseoldman.net/players/moo%20has%20fren) to 93. 

## Demo
<img width="753" alt="image" src="https://github.com/user-attachments/assets/e85f4105-3280-44db-b23e-b02ed613acd5" />

## Setup

There are two parts to run: the frontend and the backend. This assumes that you have a chromium-based browser installed on your machine.

### Frontend

1. After cloning the repository, go into `runescape-stars/` and run `npm i`.
2. If you are running this locally, you can run `npm run dev`, and the frontend should be working.
3. If you are hosting this, run `npm run build` and then `npm start`.

If your server does not have sufficient resources to build the project on the serverside you can run: 
1. Run `npm run build` on your local machine.
2. Run `scp -r .next [username]@[server_ip_address]:/destination/runescape-stars` on your local machine.
3. Run `npm start` on your server.

### Backend

1. Go into the `/backend` folder
2. Run `pip install -r requirements.txt`
3. Run `python star-scraper.py`

Startup should take around 15 seconds, as it needs to download the right chromedriver for your browser on server startup.

## Using

Go to your browser and navigate to `localhost:3000` to use. If you'd like to change your block list, you can change the `ignore_list` variable in backend/star-scraper.py @ line 48 and enter the locations you wouldn't like to see.
