from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pprint
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

def write_to_json_file(all_locations):
    if not all_locations:
        return 
    
    if os.path.exists('locations.json'):
        with open('locations.json', 'r') as file:
            existing_locations = json.load(file)
    else:
        existing_locations = []

    existing_set = set(existing_locations)
    new_locations = [location for location in all_locations if location not in existing_set]

    if new_locations:
        existing_locations.extend(new_locations)  # Add new locations to existing ones
        with open('locations.json', 'w') as file:
            json.dump(existing_locations, file, indent=4)  # Write updated locations back to the file

@app.route('/api/scrape', methods=['GET'])
def scrape_data():
    ignore_list = ["Keldagrim entrance mine", 
                   "Mount Karuulm mine",
                    "Salvager Overlook in Varlamore",
                    "Miscellania mine (cip fairy ring)",
                    "Arceuus dense essence mine",
                    "Rellekka mine",
                    "Neitiznot south of rune rock",
                    "Keldagrim entrance mine",
                    "Jatizso mine entrance",
                    "Nw of Uzer (Eagle's Eyrie)",
                    "West of Grand Tree",
                    "Hosidius mine",
                    "Mount Karuulm bank",
                    "Abandoned Mine west of Burgh",
                    "wildy resource area in", 
                    "wildy resource area on",
                    "Chambers of Xeric bank",
                    "Wilderness Resource Area",
                    "Lunar Isle mine entrance",
                    "Lava maze runite mine (lvl 46 Wildy)",
                    "Nardah bank",
                    "Canifis bank",
                    "Piscatoris (akq fairy ring)",
                    "South Crandor",
                    "Gnome Stronghold spirit tree",
                    "Fossil Island rune rocks",
                    "Myths' Guild",
                    "Port Piscarilius mine in Kourend",
                    "Isafdar runite rocks",
                    "Nature Altar mine north of Shilo",
                    "Mos Le'Harmless west bank",
                    "Lletya",
                    "Prifddinas Zalcano entrance",
                    "South Lovakengj bank",
                    "Rantz cave",
                    "Fossil Island Volcanic Mine entrance",
                    "Hobgoblin mine (lvl 30 Wildy)",
                    "Corsair Cove bank (innit)",
                    "Corsair Resource Area",
                    "Desert Quarry mine",
                    "North Crandor",
                    "Shayzien mine south of Kourend Castle",
                    "Feldip Hills (aks fairy ring)",
                    "Mynydd nw of Prifddinas",
                    "Mine north-west of hunter guild",
                    "Pirates' Hideout (lvl 53 Wildy)",
                    "Burgh de Rott bank",
                    "Southwest of Brimhaven Poh",
                    "Yanille bank",
                    "South of Legends' Guild",
                    "Shilo Village gem mine",
                    "Varlamore colosseum entrance bank",
                    "Brimhaven northwest gold mine",
                    "Mage Arena bank (lvl 56 Wildy)",
                    "Crafting guild",
                    "North Dwarven Mine entrance",
                    "Theatre of Blood bank",
                    "Aldarin mine in Varlamore",
                    "Varlamore South East mine",
                    "Darkmeyer ess. mine entrance",
                    "varlamore west mine (just below tecu salamanders)",
                    "Arandar mine north of Lletya",
                    "Port Khazard mine",
                    "Kebos Swamp mine",
                    "Lovakite mine",
                    "prif world",
                    "Agility Pyramid mine",
                    "shayzien mines",
                    "Mage of Zamorak mine (lvl 7 Wildy)"
                    ]
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(), options=chrome_options)
    f2p_src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAMAAAAoLQ9TAAAAVFBMVEUAAADo6Ojh4eHc3NzY2NjQ0NDNzc3Ly8vHx8fCwsK+vr64uLi0tLSzs7OsrKyrq6ulpaWgoKCfn5+ZmZmXl5eRkZGOjo6Li4uFhYV/f390dHQ4JBg+AiwvAAAAAXRSTlMAQObYZgAAAIVJREFUeNpdT9sWwjAIo1qoA2zdzV3y///pcVt3nHkBckICRBsAgH6BsPwTM66zDhcJQtNWCTaExm3vCDGGqKrMEu83BmHKjbqymKmkF4gw9cVEPPtD+80Hb2fx4knH6svsxSUNNRhsXWYp5yXQdn6K9mvdsDwugLfrwcC6rxg+VuJ4fa8f8JkKodx5cm0AAAAASUVORK5CYII="

    try:
        url = "https://osrsportal.com/shooting-stars-tracker"
        driver.get(url)
        locations = set()

        time.sleep(0.5)

        data = []
        tbody = driver.find_element(By.CLASS_NAME, 'styleddtablebody')
        rows = tbody.find_elements(By.TAG_NAME, 'tr')

        for row in rows:
            cells = row.find_elements(By.TAG_NAME, 'td')
            
            time_ago = cells[0].text
            world = cells[1].text
            if cells[1].find_elements(By.XPATH, f".//img[@src='{f2p_src}']"): 
                world += "f2p"
            size = cells[2].text
            location = cells[3].text.strip()
            locations.add(location)
            
            if not any(item in ignore_list for item in [time_ago, world, size, location]) and 'f2p' not in world: 
                data.append([time_ago, world, size, location])

        write_to_json_file(locations)

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        driver.quit()
        
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
