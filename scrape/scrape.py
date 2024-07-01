import requests
from bs4 import BeautifulSoup
import time
import logging
import json
import os
import hashlib

class AnimalDTO:
    def __init__(self, id, wiki_link, title, image_url, caption, interactivity, edition, continents, regions, iucn_status, biomes, group_size, reproduction, maturity, sterility, gestation_incubation, interbirth, animal_class, order, family, genus):
        self.id = id
        self.title = title
        self.wiki_link = wiki_link
        self.image_url = image_url
        self.caption = caption
        self.interactivity = interactivity
        self.edition = edition
        self.continents = continents
        self.regions = regions
        self.iucn_status = iucn_status
        self.biomes = biomes
        self.group_size = group_size
        self.reproduction = reproduction
        self.maturity = maturity
        self.sterility = sterility
        self.gestation_incubation = gestation_incubation
        self.interbirth = interbirth
        self.animal_class = animal_class
        self.order = order
        self.family = family
        self.genus = genus

def fetch_and_parse(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        return soup
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

def extract_group_data(soup, source_name, default_value = None):

    value_element = soup.select_one(f'[data-source="{source_name}"].pi-smart-data-value')
    if value_element:
        return value_element.get_text(strip=True)

    value_element = soup.select_one(f'[data-source="{source_name}"] .pi-data-value')
    if value_element:
        return value_element.get_text(strip=True)

    if default_value != None:
      return default_value

    raise Exception(f'Cannot read data-source {source_name}')


continents_mapping = {
        "Africa": ["Africa"],
        "North America": ["North America"],
        "Asia": ["Asia"],
        "South America": ["South America"],
        "Central America": ["Central America"],
        "Europe": ["Europe"],
        "Oceania": ["Oceania"],
        "North": ["North America"],
        "Central and South America": ["Central America", "South America"],
        "North and Central America": ["North America", "Central America"],
        "South America/Central America": ["South America", "Central America"],
        "South East Asia": ["Asia"],
        "Antarctica": ["Antarctica"],
        "Europe and Asia": ["Europe", "Asia"],
        "North and South America": ["North America", "South America"],
        "Oceania (occasional migrants found in Europe and Africa)": ["Oceania", "Europe", "Africa"],
        "now distributed worldwide": ["Antarctica", "Africa", "Asia", "Central America", "South America", "North America", "Oceania", "Europe"]
    }


def parse_animal_info(soup, wiki_link):
    title = soup.select_one('.pi-title').get_text(strip=True)
    image_url = soup.select_one('.pi-image img')['src']
    if '?' in image_url:
            image_url = image_url.split('?')[0]

    caption_elem = soup.select_one('.pi-caption')
    caption = caption_elem.get_text(strip=True) if caption_elem != None else title

    interactivity = extract_group_data(soup, 'exhibit')
    edition = extract_group_data(soup, 'edition')
    if edition:
        if edition == 'Standard':
            edition = 'Basegame'
        if '/' in edition:
            edition = edition.split('/')[0].strip()
        if edition.endswith('Animal Pack'):
            edition = edition.replace('Animal Pack', 'Pack').strip()
        if edition.endswith('Pack'):
            edition = edition.replace('Pack', 'DLC').strip()

    old_continents = extract_group_data(soup, 'continent')
    continents = []
    if old_continents:
        old_continents_list = [continent.strip() for continent in old_continents.split(',')]
        for old_continent in old_continents_list:
            if old_continent in continents_mapping:
                continents.extend(continents_mapping[old_continent])

    regions = extract_group_data(soup, 'region', '')
    iucn_status = soup.select_one('[data-source="iucnstatus"] img')['alt']

    biomes = [img['alt'] for img in soup.select('[data-source="biome"] img')]
    biomes = ['Tropical' if biome == 'TropicalIcon' else 'Temperate' if biome == 'TemperateIcon' else biome for biome in biomes]

    group_size = extract_group_data(soup, 'gsize')
    reproduction = extract_group_data(soup, 'reproduction', '')
    maturity = extract_group_data(soup, 'maturity')
    sterility = extract_group_data(soup, 'sterility')
    gestation_incubation = extract_group_data(soup, 'gestaincub')
    interbirth = extract_group_data(soup, 'interbirth')

    animal_class = extract_group_data(soup, 'class', '')
    order = extract_group_data(soup, 'order', '')
    family = extract_group_data(soup, 'family', '')
    genus = extract_group_data(soup, 'genus', '')

    id = hashlib.sha256(title.encode()).hexdigest()

    return AnimalDTO(
        id, wiki_link,
        title, image_url, caption, interactivity, edition, continents, regions, iucn_status,
        biomes, group_size, reproduction, maturity, sterility,
        gestation_incubation, interbirth, animal_class, order, family, genus
    )

# List of URLs to scrape
urls = [
  "https://planetzoo.fandom.com/wiki/Aardvark",
  "https://planetzoo.fandom.com/wiki/African_Buffalo",
  "https://planetzoo.fandom.com/wiki/African_Savannah_Elephant",
  "https://planetzoo.fandom.com/wiki/African_Wild_Dog",
  "https://planetzoo.fandom.com/wiki/Aldabra_Giant_Tortoise",
  "https://planetzoo.fandom.com/wiki/American_Bison",
  "https://planetzoo.fandom.com/wiki/Bactrian_Camel",
  "https://planetzoo.fandom.com/wiki/Baird%27s_Tapir",
  "https://planetzoo.fandom.com/wiki/Bengal_Tiger",
  "https://planetzoo.fandom.com/wiki/Black_Wildebeest",
  "https://planetzoo.fandom.com/wiki/Bongo",
  "https://planetzoo.fandom.com/wiki/Bonobo",
  "https://planetzoo.fandom.com/wiki/Bornean_Orangutan",
  "https://planetzoo.fandom.com/wiki/Cheetah",
  "https://planetzoo.fandom.com/wiki/Chinese_Pangolin",
  "https://planetzoo.fandom.com/wiki/Common_Ostrich",
  "https://planetzoo.fandom.com/wiki/Common_Warthog",
  "https://planetzoo.fandom.com/wiki/Formosan_Black_Bear",
  "https://planetzoo.fandom.com/wiki/Galapagos_Giant_Tortoise",
  "https://planetzoo.fandom.com/wiki/Gemsbok",
  "https://planetzoo.fandom.com/wiki/Gharial",
  "https://planetzoo.fandom.com/wiki/Giant_Panda",
  "https://planetzoo.fandom.com/wiki/Greater_Flamingo",
  "https://planetzoo.fandom.com/wiki/Grizzly_Bear",
  "https://planetzoo.fandom.com/wiki/Himalayan_Brown_Bear",
  "https://planetzoo.fandom.com/wiki/Hippopotamus",
  "https://planetzoo.fandom.com/wiki/Indian_Elephant",
  "https://planetzoo.fandom.com/wiki/Indian_Peafowl",
  "https://planetzoo.fandom.com/wiki/Indian_Rhinoceros",
  "https://planetzoo.fandom.com/wiki/Japanese_Macaque",
  "https://planetzoo.fandom.com/wiki/Mandrill",
  "https://planetzoo.fandom.com/wiki/Nile_Monitor",
  "https://planetzoo.fandom.com/wiki/Nyala",
  "https://planetzoo.fandom.com/wiki/Okapi",
  "https://planetzoo.fandom.com/wiki/Plains_Zebra",
  "https://planetzoo.fandom.com/wiki/Pronghorn_Antelope",
  "https://planetzoo.fandom.com/wiki/Red_Panda",
  "https://planetzoo.fandom.com/wiki/Red_Ruffed_Lemur",
  "https://planetzoo.fandom.com/wiki/Reticulated_Giraffe",
  "https://planetzoo.fandom.com/wiki/Ring_Tailed_Lemur",
  "https://planetzoo.fandom.com/wiki/Sable_Antelope",
  "https://planetzoo.fandom.com/wiki/Saltwater_Crocodile",
  "https://planetzoo.fandom.com/wiki/Siberian_Tiger",
  "https://planetzoo.fandom.com/wiki/Snow_Leopard",
  "https://planetzoo.fandom.com/wiki/Spotted_Hyena",
  "https://planetzoo.fandom.com/wiki/Springbok",
  "https://planetzoo.fandom.com/wiki/Timber_Wolf",
  "https://planetzoo.fandom.com/wiki/West_African_Lion",
  "https://planetzoo.fandom.com/wiki/Western_Chimpanzee",
  "https://planetzoo.fandom.com/wiki/Western_Lowland_Gorilla",
  "https://planetzoo.fandom.com/wiki/Black-and-White_Ruffed_Lemur",
  "https://planetzoo.fandom.com/wiki/Collared_Peccary",
  "https://planetzoo.fandom.com/wiki/Red_Deer",
  "https://planetzoo.fandom.com/wiki/Amazonian_Giant_Centipede",
  "https://planetzoo.fandom.com/wiki/Boa_Constrictor",
  "https://planetzoo.fandom.com/wiki/Brazilian_Salmon_Pink_Tarantula",
  "https://planetzoo.fandom.com/wiki/Brazilian_Wandering_Spider",
  "https://planetzoo.fandom.com/wiki/Common_Death_Adder",
  "https://planetzoo.fandom.com/wiki/Eastern_Brown_Snake",
  "https://planetzoo.fandom.com/wiki/Giant_Burrowing_Cockroach",
  "https://planetzoo.fandom.com/wiki/Giant_Desert_Hairy_Scorpion",
  "https://planetzoo.fandom.com/wiki/Giant_Forest_Scorpion",
  "https://planetzoo.fandom.com/wiki/Giant_Tiger_Land_Snail",
  "https://planetzoo.fandom.com/wiki/Gila_Monster",
  "https://planetzoo.fandom.com/wiki/Golden_Poison_Frog",
  "https://planetzoo.fandom.com/wiki/Goliath_Beetle",
  "https://planetzoo.fandom.com/wiki/Goliath_Birdeater",
  "https://planetzoo.fandom.com/wiki/Goliath_Frog",
  "https://planetzoo.fandom.com/wiki/Green_Iguana",
  "https://planetzoo.fandom.com/wiki/Lehmann%27s_Poison_Frog",
  "https://planetzoo.fandom.com/wiki/Lesser_Antillean_Iguana",
  "https://planetzoo.fandom.com/wiki/Mexican_Red_Knee_Tarantula",
  "https://planetzoo.fandom.com/wiki/Puff_Adder",
  "https://planetzoo.fandom.com/wiki/Titan_Beetle",
  "https://planetzoo.fandom.com/wiki/Western_Diamondback_Rattlesnake",
  "https://planetzoo.fandom.com/wiki/Yellow_Anaconda",
  "https://planetzoo.fandom.com/wiki/Komodo_Dragon",
  "https://planetzoo.fandom.com/wiki/Pygmy_Hippo",
  "https://planetzoo.fandom.com/wiki/Thomson%27s_Gazelle",
  "https://planetzoo.fandom.com/wiki/Arctic_Wolf",
  "https://planetzoo.fandom.com/wiki/Dall_Sheep",
  "https://planetzoo.fandom.com/wiki/Polar_Bear",
  "https://planetzoo.fandom.com/wiki/Reindeer",
  "https://planetzoo.fandom.com/wiki/Colombian_White-Faced_Capuchin_Monkey",
  "https://planetzoo.fandom.com/wiki/Giant_Anteater",
  "https://planetzoo.fandom.com/wiki/Jaguar",
  "https://planetzoo.fandom.com/wiki/Llama",
  "https://planetzoo.fandom.com/wiki/Red-Eyed_Tree_Frog",
  "https://planetzoo.fandom.com/wiki/Dingo",
  "https://planetzoo.fandom.com/wiki/Koala",
  "https://planetzoo.fandom.com/wiki/Red_Kangaroo",
  "https://planetzoo.fandom.com/wiki/Southern_Cassowary",
  "https://planetzoo.fandom.com/wiki/Eastern_Blue_Tongued_Lizard",
  "https://planetzoo.fandom.com/wiki/Cuvier%27s_Dwarf_Caiman",
  "https://planetzoo.fandom.com/wiki/Giant_Otter",
  "https://planetzoo.fandom.com/wiki/Grey_Seal",
  "https://planetzoo.fandom.com/wiki/King_Penguin",
  "https://planetzoo.fandom.com/wiki/Diamondback_Terrapin",
  "https://planetzoo.fandom.com/wiki/Binturong",
  "https://planetzoo.fandom.com/wiki/Clouded_Leopard",
  "https://planetzoo.fandom.com/wiki/Dhole",
  "https://planetzoo.fandom.com/wiki/Malayan_Tapir",
  "https://planetzoo.fandom.com/wiki/North_Sulawesi_Babirusa",
  "https://planetzoo.fandom.com/wiki/Proboscis_Monkey",
  "https://planetzoo.fandom.com/wiki/Sun_Bear",
  "https://planetzoo.fandom.com/wiki/Giant_Malaysian_Leaf_Insect",
  "https://planetzoo.fandom.com/wiki/African_Penguin",
  "https://planetzoo.fandom.com/wiki/Fennec_Fox",
  "https://planetzoo.fandom.com/wiki/Meerkat",
  "https://planetzoo.fandom.com/wiki/Southern_White_Rhinoceros",
  "https://planetzoo.fandom.com/wiki/Sacred_Scarab_Beetle",
  "https://planetzoo.fandom.com/wiki/American_Alligator",
  "https://planetzoo.fandom.com/wiki/Arctic_Fox",
  "https://planetzoo.fandom.com/wiki/Black-Tailed_Prairie_Dog",
  "https://planetzoo.fandom.com/wiki/California_Sea_Lion",
  "https://planetzoo.fandom.com/wiki/Cougar",
  "https://planetzoo.fandom.com/wiki/Moose",
  "https://planetzoo.fandom.com/wiki/North_American_Beaver",
  "https://planetzoo.fandom.com/wiki/American_Bullfrog",
  "https://planetzoo.fandom.com/wiki/Alpine_Ibex",
  "https://planetzoo.fandom.com/wiki/Eurasian_Lynx",
  "https://planetzoo.fandom.com/wiki/European_Badger",
  "https://planetzoo.fandom.com/wiki/European_Fallow_Deer",
  "https://planetzoo.fandom.com/wiki/Fire_Salamander",
  "https://planetzoo.fandom.com/wiki/Asian_Small-Clawed_Otter",
  "https://planetzoo.fandom.com/wiki/Capybara",
  "https://planetzoo.fandom.com/wiki/Nile_Lechwe",
  "https://planetzoo.fandom.com/wiki/Platypus",
  "https://planetzoo.fandom.com/wiki/Red-Crowned_Crane",
  "https://planetzoo.fandom.com/wiki/Spectacled_Caiman",
  "https://planetzoo.fandom.com/wiki/Wild_Water_Buffalo",
  "https://planetzoo.fandom.com/wiki/Danube_Crested_Newt",
  "https://planetzoo.fandom.com/wiki/Amur_Leopard",
  "https://planetzoo.fandom.com/wiki/Axolotl",
  "https://planetzoo.fandom.com/wiki/Przewalski%27s_Horse",
  "https://planetzoo.fandom.com/wiki/Scimitar-Horned_Oryx",
  "https://planetzoo.fandom.com/wiki/Siamang",
  "https://planetzoo.fandom.com/wiki/Common_Wombat",
  "https://planetzoo.fandom.com/wiki/Egyptian_Fruit_Bat",
  "https://planetzoo.fandom.com/wiki/Raccoon",
  "https://planetzoo.fandom.com/wiki/Red_Fox",
  "https://planetzoo.fandom.com/wiki/Striped_Skunk",
  "https://planetzoo.fandom.com/wiki/Blue_Wildebeest",
  "https://planetzoo.fandom.com/wiki/Caracal",
  "https://planetzoo.fandom.com/wiki/Cloudless_Sulphur",
  "https://planetzoo.fandom.com/wiki/Emu",
  "https://planetzoo.fandom.com/wiki/European_Peacock",
  "https://planetzoo.fandom.com/wiki/Maned_Wolf",
  "https://planetzoo.fandom.com/wiki/Menelaus_Blue_Morpho",
  "https://planetzoo.fandom.com/wiki/Monarch",
  "https://planetzoo.fandom.com/wiki/Nine-Banded_Armadillo",
  "https://planetzoo.fandom.com/wiki/Old_World_Swallowtail",
  "https://planetzoo.fandom.com/wiki/Red-Necked_Wallaby",
  "https://planetzoo.fandom.com/wiki/Striped_Hyena",
  "https://planetzoo.fandom.com/wiki/Asian_Water_Monitor",
  "https://planetzoo.fandom.com/wiki/Brown-throated_Sloth",
  "https://planetzoo.fandom.com/wiki/Fossa",
  "https://planetzoo.fandom.com/wiki/Lar_Gibbon",
  "https://planetzoo.fandom.com/wiki/Red_River_Hog",
  "https://planetzoo.fandom.com/wiki/Addax",
  "https://planetzoo.fandom.com/wiki/African_Crested_Porcupine",
  "https://planetzoo.fandom.com/wiki/Black_Rhinoceros",
  "https://planetzoo.fandom.com/wiki/Dama_Gazelle",
  "https://planetzoo.fandom.com/wiki/Desert_Horned_Viper",
  "https://planetzoo.fandom.com/wiki/Dromedary_Camel",
  "https://planetzoo.fandom.com/wiki/Sand_Cat",
  "https://planetzoo.fandom.com/wiki/Somali_Wild_Ass",
  "https://planetzoo.fandom.com/wiki/Little_Penguin",
  "https://planetzoo.fandom.com/wiki/North_Island_Brown_Kiwi",
  "https://planetzoo.fandom.com/wiki/Quokka",
  "https://planetzoo.fandom.com/wiki/Spectacled_Flying_Fox",
  "https://planetzoo.fandom.com/wiki/Tasmanian_Devil",
  "https://planetzoo.fandom.com/wiki/Hermann%27s_Tortoise",
  "https://planetzoo.fandom.com/wiki/Mute_Swan",
  "https://planetzoo.fandom.com/wiki/Saiga",
  "https://planetzoo.fandom.com/wiki/Sloth_Bear",
  "https://planetzoo.fandom.com/wiki/Takin",
  "https://planetzoo.fandom.com/wiki/Wild_Boar",
  "https://planetzoo.fandom.com/wiki/Wisent",
  "https://planetzoo.fandom.com/wiki/Wolverine",
  "https://planetzoo.fandom.com/wiki/Alpaca",
  "https://planetzoo.fandom.com/wiki/Alpine_Goat",
  "https://planetzoo.fandom.com/wiki/American_Standard_Donkey",
  "https://planetzoo.fandom.com/wiki/Highland_Cattle",
  "https://planetzoo.fandom.com/wiki/Hill_Radnor_Sheep",
  "https://planetzoo.fandom.com/wiki/Sussex_Chicken",
  "https://planetzoo.fandom.com/wiki/Tamworth_Pig"
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# Define the output file path
output_file = 'animals.json'
animals = []

# If the file already exists, load existing data
if os.path.exists(output_file):
    with open(output_file, 'r') as f:
        try:
            animals = json.load(f)
            logger.info(f"Loaded existing data from {output_file}")
        except json.JSONDecodeError:
            logger.info(f"Failed to load JSON from {output_file}. Starting with an empty list.")

scraped_urls = set(animal.get('wiki_link') for animal in animals)
if len(scraped_urls) == len(urls):
    logger.info("All animals already proccessed")
    exit()

for url in filter(lambda url: url not in scraped_urls, urls):
    logger.info(f"Processing URL: {url}")
    try:
        soup = fetch_and_parse(url)
        if soup:
            animal = parse_animal_info(soup, url)
            logger.info(f"Animal info extracted from {url}: {animal.__dict__}")
            animals.append(animal.__dict__)
        else:
            logger.warning(f"No data parsed from {url}")
            continue

        time.sleep(5)

    except Exception as e:
        logger.error(f"Failed to process URL {url}. Error: {str(e)}")

    with open(output_file, 'w') as f:
        json.dump(animals, f, indent=4)


logger.info(f"Animal data saved to {output_file}")
