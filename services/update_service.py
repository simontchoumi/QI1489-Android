"""
QI1489 Android — Update Service
Fetches live country data from REST Countries API and generates all question types.
"""
import random

try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

# ------------------------------------------------------------------ #
#  STATIC DATA
# ------------------------------------------------------------------ #
CONTINENT_FR = {
    'Africa': 'Afrique', 'Americas': 'Ameriques',
    'Asia': 'Asie', 'Europe': 'Europe', 'Oceania': 'Oceanie',
}

HEADS_OF_STATE = {
    # Africa
    'Algeria': ('Abdelmadjid Tebboune', 'President'),
    'Angola': ('Joao Lourenco', 'President'),
    'Benin': ('Patrice Talon', 'President'),
    'Botswana': ('Duma Boko', 'President'),
    'Burkina Faso': ('Ibrahim Traore', 'President'),
    'Burundi': ('Evariste Ndayishimiye', 'President'),
    'Cameroon': ('Paul Biya', 'President'),
    'Cape Verde': ('Jose Maria Neves', 'President'),
    'Central African Republic': ('Faustin-Archange Touadera', 'President'),
    'Chad': ('Mahamat Idriss Deby', 'President'),
    'Comoros': ('Azali Assoumani', 'President'),
    'DR Congo': ('Felix Tshisekedi', 'President'),
    'Republic of the Congo': ('Denis Sassou Nguesso', 'President'),
    'Djibouti': ('Ismail Omar Guelleh', 'President'),
    'Egypt': ('Abdel Fattah el-Sisi', 'President'),
    'Equatorial Guinea': ('Teodoro Obiang Nguema Mbasogo', 'President'),
    'Eritrea': ('Isaias Afwerki', 'President'),
    'Eswatini': ('King Mswati III', 'King'),
    'Ethiopia': ('Sahle-Work Zewde', 'President'),
    'Gabon': ('Brice Clotaire Oligui Nguema', 'President'),
    'Gambia': ('Adama Barrow', 'President'),
    'Ghana': ('John Mahama', 'President'),
    'Guinea': ('Mamadi Doumbouya', 'President'),
    'Guinea-Bissau': ('Umaro Sissoco Embalo', 'President'),
    'Ivory Coast': ('Alassane Ouattara', 'President'),
    'Kenya': ('William Ruto', 'President'),
    'Lesotho': ('Sam Matekane', 'Prime Minister'),
    'Liberia': ('Joseph Boakai', 'President'),
    'Libya': ('Mohammed al-Menfi', 'Chairman'),
    'Madagascar': ('Andry Rajoelina', 'President'),
    'Malawi': ('Lazarus Chakwera', 'President'),
    'Mali': ('Assimi Goita', 'President'),
    'Mauritania': ('Mohamed Ould Ghazouani', 'President'),
    'Mauritius': ('Navin Ramgoolam', 'Prime Minister'),
    'Morocco': ('King Mohammed VI', 'King'),
    'Mozambique': ('Daniel Chapo', 'President'),
    'Namibia': ('Netumbo Nandi-Ndaitwah', 'President'),
    'Niger': ('Abdourahamane Tchiani', 'President'),
    'Nigeria': ('Bola Tinubu', 'President'),
    'Rwanda': ('Paul Kagame', 'President'),
    'Sao Tome and Principe': ('Carlos Vila Nova', 'President'),
    'Senegal': ('Bassirou Diomaye Faye', 'President'),
    'Sierra Leone': ('Julius Maada Bio', 'President'),
    'Somalia': ('Hassan Sheikh Mohamud', 'President'),
    'South Africa': ('Cyril Ramaphosa', 'President'),
    'South Sudan': ('Salva Kiir Mayardit', 'President'),
    'Sudan': ('Abdel Fattah al-Burhan', 'President'),
    'Tanzania': ('Samia Suluhu Hassan', 'President'),
    'Togo': ('Faure Gnassingbe', 'President'),
    'Tunisia': ('Kais Saied', 'President'),
    'Uganda': ('Yoweri Museveni', 'President'),
    'Zambia': ('Hakainde Hichilema', 'President'),
    'Zimbabwe': ('Emmerson Mnangagwa', 'President'),
    # Americas
    'Antigua and Barbuda': ('Gaston Browne', 'Prime Minister'),
    'Argentina': ('Javier Milei', 'President'),
    'Bahamas': ('Philip Davis', 'Prime Minister'),
    'Barbados': ('Mia Mottley', 'Prime Minister'),
    'Belize': ('John Briceno', 'Prime Minister'),
    'Bolivia': ('Luis Arce', 'President'),
    'Brazil': ('Luiz Inacio Lula da Silva', 'President'),
    'Canada': ('Mark Carney', 'Prime Minister'),
    'Chile': ('Gabriel Boric', 'President'),
    'Colombia': ('Gustavo Petro', 'President'),
    'Costa Rica': ('Rodrigo Chaves', 'President'),
    'Cuba': ('Miguel Diaz-Canel', 'President'),
    'Dominica': ('Sylvanie Burton', 'President'),
    'Dominican Republic': ('Luis Abinader', 'President'),
    'Ecuador': ('Daniel Noboa', 'President'),
    'El Salvador': ('Nayib Bukele', 'President'),
    'Grenada': ('Dickon Mitchell', 'Prime Minister'),
    'Guatemala': ('Bernardo Arevalo', 'President'),
    'Guyana': ('Mohamed Irfaan Ali', 'President'),
    'Haiti': ('Alix Didier Fils-Aime', 'Prime Minister'),
    'Honduras': ('Xiomara Castro', 'President'),
    'Jamaica': ('Andrew Holness', 'Prime Minister'),
    'Mexico': ('Claudia Sheinbaum', 'President'),
    'Nicaragua': ('Daniel Ortega', 'President'),
    'Panama': ('Jose Raul Mulino', 'President'),
    'Paraguay': ('Santiago Pena', 'President'),
    'Peru': ('Dina Boluarte', 'President'),
    'Saint Kitts and Nevis': ('Terrance Drew', 'Prime Minister'),
    'Saint Lucia': ('Philip Pierre', 'Prime Minister'),
    'Saint Vincent and the Grenadines': ('Ralph Gonsalves', 'Prime Minister'),
    'Suriname': ('Chan Santokhi', 'President'),
    'Trinidad and Tobago': ('Keith Rowley', 'Prime Minister'),
    'United States': ('Donald Trump', 'President'),
    'Uruguay': ('Yamandu Orsi', 'President'),
    'Venezuela': ('Nicolas Maduro', 'President'),
    # Asia
    'Afghanistan': ('Hibatullah Akhundzada', 'Supreme Leader'),
    'Armenia': ('Vahagn Khachaturyan', 'President'),
    'Azerbaijan': ('Ilham Aliyev', 'President'),
    'Bahrain': ('King Hamad bin Isa Al Khalifa', 'King'),
    'Bangladesh': ('Muhammad Yunus', 'Chief Adviser'),
    'Bhutan': ('Tshering Tobgay', 'Prime Minister'),
    'Brunei': ('Sultan Hassanal Bolkiah', 'Sultan'),
    'Cambodia': ('Hun Manet', 'Prime Minister'),
    'China': ('Xi Jinping', 'President'),
    'Cyprus': ('Nikos Christodoulides', 'President'),
    'Georgia': ('Mikheil Kavelashvili', 'President'),
    'India': ('Narendra Modi', 'Prime Minister'),
    'Indonesia': ('Prabowo Subianto', 'President'),
    'Iran': ('Masoud Pezeshkian', 'President'),
    'Iraq': ('Abdul Latif Rashid', 'President'),
    'Israel': ('Isaac Herzog', 'President'),
    'Japan': ('Shigeru Ishiba', 'Prime Minister'),
    'Jordan': ('King Abdullah II', 'King'),
    'Kazakhstan': ('Kassym-Jomart Tokayev', 'President'),
    'Kuwait': ('Emir Mishal Al-Ahmad Al-Sabah', 'Emir'),
    'Kyrgyzstan': ('Sadyr Japarov', 'President'),
    'Laos': ('Thongloun Sisoulith', 'President'),
    'Lebanon': ('Joseph Aoun', 'President'),
    'Malaysia': ('Anwar Ibrahim', 'Prime Minister'),
    'Maldives': ('Mohamed Muizzu', 'President'),
    'Mongolia': ('Ukhnaagiin Khurelsukh', 'President'),
    'Myanmar': ('Min Aung Hlaing', 'Prime Minister'),
    'Nepal': ('KP Sharma Oli', 'Prime Minister'),
    'North Korea': ('Kim Jong-un', 'Supreme Leader'),
    'Oman': ('Sultan Haitham bin Tariq', 'Sultan'),
    'Pakistan': ('Asif Ali Zardari', 'President'),
    'Palestine': ('Mahmoud Abbas', 'President'),
    'Philippines': ('Ferdinand Marcos Jr.', 'President'),
    'Qatar': ('Emir Tamim bin Hamad Al Thani', 'Emir'),
    'Saudi Arabia': ('King Salman bin Abdulaziz', 'King'),
    'Singapore': ('Tharman Shanmugaratnam', 'President'),
    'South Korea': ('Han Duck-soo', 'Acting President'),
    'Sri Lanka': ('Anura Kumara Dissanayake', 'President'),
    'Syria': ('Ahmad al-Sharaa', 'President'),
    'Taiwan': ('Lai Ching-te', 'President'),
    'Tajikistan': ('Emomali Rahmon', 'President'),
    'Thailand': ('Paetongtarn Shinawatra', 'Prime Minister'),
    'Timor-Leste': ('Jose Ramos-Horta', 'President'),
    'Turkmenistan': ('Serdar Berdimuhamedow', 'President'),
    'Turkey': ('Recep Tayyip Erdogan', 'President'),
    'United Arab Emirates': ('President Mohamed bin Zayed', 'President'),
    'Uzbekistan': ('Shavkat Mirziyoyev', 'President'),
    'Vietnam': ('Luong Cuong', 'President'),
    'Yemen': ('Rashad al-Alimi', 'President'),
    # Europe
    'Albania': ('Bajram Begaj', 'President'),
    'Andorra': ('Xavier Espot Zamora', 'Prime Minister'),
    'Austria': ('Alexander Van der Bellen', 'President'),
    'Belarus': ('Alexander Lukashenko', 'President'),
    'Belgium': ('Alexander De Croo', 'Prime Minister'),
    'Bosnia and Herzegovina': ('Denis Becirovic', 'Chairman'),
    'Bulgaria': ('Rumen Radev', 'President'),
    'Croatia': ('Zoran Milanovic', 'President'),
    'Czech Republic': ('Petr Pavel', 'President'),
    'Denmark': ('Mette Frederiksen', 'Prime Minister'),
    'Estonia': ('Alar Karis', 'President'),
    'Finland': ('Alexander Stubb', 'President'),
    'France': ('Emmanuel Macron', 'President'),
    'Germany': ('Friedrich Merz', 'Chancellor'),
    'Greece': ('Katerina Sakellaropoulou', 'President'),
    'Hungary': ('Tamas Sulyok', 'President'),
    'Iceland': ('Gudni Johannesson', 'President'),
    'Ireland': ('Micheal Martin', 'Taoiseach'),
    'Italy': ('Sergio Mattarella', 'President'),
    'Kosovo': ('Vjosa Osmani', 'President'),
    'Latvia': ('Edgars Rinkevics', 'President'),
    'Liechtenstein': ('Prince Hans-Adam II', 'Prince'),
    'Lithuania': ('Gitanas Nauseda', 'President'),
    'Luxembourg': ('Grand Duke Henri', 'Grand Duke'),
    'Malta': ('George Vella', 'President'),
    'Moldova': ('Maia Sandu', 'President'),
    'Monaco': ('Prince Albert II', 'Prince'),
    'Montenegro': ('Jakov Milatovic', 'President'),
    'Netherlands': ('Mark Rutte', 'Prime Minister'),
    'North Macedonia': ('Gordana Siljanovska-Davkova', 'President'),
    'Norway': ('Jonas Gahr Store', 'Prime Minister'),
    'Poland': ('Andrzej Duda', 'President'),
    'Portugal': ('Marcelo Rebelo de Sousa', 'President'),
    'Romania': ('Calin Georgescu', 'President'),
    'Russia': ('Vladimir Putin', 'President'),
    'San Marino': ('Francesca Civerchia', 'Captain Regent'),
    'Serbia': ('Aleksandar Vucic', 'President'),
    'Slovakia': ('Peter Pellegrini', 'President'),
    'Slovenia': ('Natasa Pirc Musar', 'President'),
    'Spain': ('Pedro Sanchez', 'Prime Minister'),
    'Sweden': ('Ulf Kristersson', 'Prime Minister'),
    'Switzerland': ('Karin Keller-Sutter', 'President'),
    'Ukraine': ('Volodymyr Zelensky', 'President'),
    'United Kingdom': ('Keir Starmer', 'Prime Minister'),
    'Vatican City': ('Pope Francis', 'Pope'),
    # Oceania
    'Australia': ('Anthony Albanese', 'Prime Minister'),
    'Fiji': ('Sitiveni Rabuka', 'Prime Minister'),
    'Kiribati': ('Taneti Maamau', 'President'),
    'Marshall Islands': ('Hilda Heine', 'President'),
    'Micronesia': ('Wesley Simina', 'President'),
    'Nauru': ('David Adeang', 'President'),
    'New Zealand': ('Christopher Luxon', 'Prime Minister'),
    'Palau': ('Surangel Whipps Jr.', 'President'),
    'Papua New Guinea': ('James Marape', 'Prime Minister'),
    'Samoa': ('Fiame Naomi Mata\'afa', 'Prime Minister'),
    'Solomon Islands': ('Jeremiah Manele', 'Prime Minister'),
    'Tonga': ('Siaosi Sovaleni', 'Prime Minister'),
    'Tuvalu': ('Feleti Teo', 'Prime Minister'),
    'Vanuatu': ('Charlot Salwai', 'Prime Minister'),
}

COUNTRY_CONTINENT = {
    'Algeria': 'Africa', 'Angola': 'Africa', 'Benin': 'Africa', 'Botswana': 'Africa',
    'Burkina Faso': 'Africa', 'Burundi': 'Africa', 'Cameroon': 'Africa', 'Cape Verde': 'Africa',
    'Central African Republic': 'Africa', 'Chad': 'Africa', 'Comoros': 'Africa',
    'DR Congo': 'Africa', 'Republic of the Congo': 'Africa', 'Djibouti': 'Africa',
    'Egypt': 'Africa', 'Equatorial Guinea': 'Africa', 'Eritrea': 'Africa',
    'Eswatini': 'Africa', 'Ethiopia': 'Africa', 'Gabon': 'Africa', 'Gambia': 'Africa',
    'Ghana': 'Africa', 'Guinea': 'Africa', 'Guinea-Bissau': 'Africa', 'Ivory Coast': 'Africa',
    'Kenya': 'Africa', 'Lesotho': 'Africa', 'Liberia': 'Africa', 'Libya': 'Africa',
    'Madagascar': 'Africa', 'Malawi': 'Africa', 'Mali': 'Africa', 'Mauritania': 'Africa',
    'Mauritius': 'Africa', 'Morocco': 'Africa', 'Mozambique': 'Africa', 'Namibia': 'Africa',
    'Niger': 'Africa', 'Nigeria': 'Africa', 'Rwanda': 'Africa',
    'Sao Tome and Principe': 'Africa', 'Senegal': 'Africa', 'Sierra Leone': 'Africa',
    'Somalia': 'Africa', 'South Africa': 'Africa', 'South Sudan': 'Africa',
    'Sudan': 'Africa', 'Tanzania': 'Africa', 'Togo': 'Africa', 'Tunisia': 'Africa',
    'Uganda': 'Africa', 'Zambia': 'Africa', 'Zimbabwe': 'Africa',
    'Antigua and Barbuda': 'Americas', 'Argentina': 'Americas', 'Bahamas': 'Americas',
    'Barbados': 'Americas', 'Belize': 'Americas', 'Bolivia': 'Americas', 'Brazil': 'Americas',
    'Canada': 'Americas', 'Chile': 'Americas', 'Colombia': 'Americas', 'Costa Rica': 'Americas',
    'Cuba': 'Americas', 'Dominica': 'Americas', 'Dominican Republic': 'Americas',
    'Ecuador': 'Americas', 'El Salvador': 'Americas', 'Grenada': 'Americas',
    'Guatemala': 'Americas', 'Guyana': 'Americas', 'Haiti': 'Americas', 'Honduras': 'Americas',
    'Jamaica': 'Americas', 'Mexico': 'Americas', 'Nicaragua': 'Americas', 'Panama': 'Americas',
    'Paraguay': 'Americas', 'Peru': 'Americas', 'Saint Kitts and Nevis': 'Americas',
    'Saint Lucia': 'Americas', 'Saint Vincent and the Grenadines': 'Americas',
    'Suriname': 'Americas', 'Trinidad and Tobago': 'Americas', 'United States': 'Americas',
    'Uruguay': 'Americas', 'Venezuela': 'Americas',
    'Afghanistan': 'Asia', 'Armenia': 'Asia', 'Azerbaijan': 'Asia', 'Bahrain': 'Asia',
    'Bangladesh': 'Asia', 'Bhutan': 'Asia', 'Brunei': 'Asia', 'Cambodia': 'Asia',
    'China': 'Asia', 'Cyprus': 'Asia', 'Georgia': 'Asia', 'India': 'Asia',
    'Indonesia': 'Asia', 'Iran': 'Asia', 'Iraq': 'Asia', 'Israel': 'Asia', 'Japan': 'Asia',
    'Jordan': 'Asia', 'Kazakhstan': 'Asia', 'Kuwait': 'Asia', 'Kyrgyzstan': 'Asia',
    'Laos': 'Asia', 'Lebanon': 'Asia', 'Malaysia': 'Asia', 'Maldives': 'Asia',
    'Mongolia': 'Asia', 'Myanmar': 'Asia', 'Nepal': 'Asia', 'North Korea': 'Asia',
    'Oman': 'Asia', 'Pakistan': 'Asia', 'Palestine': 'Asia', 'Philippines': 'Asia',
    'Qatar': 'Asia', 'Saudi Arabia': 'Asia', 'Singapore': 'Asia', 'South Korea': 'Asia',
    'Sri Lanka': 'Asia', 'Syria': 'Asia', 'Taiwan': 'Asia', 'Tajikistan': 'Asia',
    'Thailand': 'Asia', 'Timor-Leste': 'Asia', 'Turkmenistan': 'Asia', 'Turkey': 'Asia',
    'United Arab Emirates': 'Asia', 'Uzbekistan': 'Asia', 'Vietnam': 'Asia', 'Yemen': 'Asia',
    'Albania': 'Europe', 'Andorra': 'Europe', 'Austria': 'Europe', 'Belarus': 'Europe',
    'Belgium': 'Europe', 'Bosnia and Herzegovina': 'Europe', 'Bulgaria': 'Europe',
    'Croatia': 'Europe', 'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Estonia': 'Europe',
    'Finland': 'Europe', 'France': 'Europe', 'Germany': 'Europe', 'Greece': 'Europe',
    'Hungary': 'Europe', 'Iceland': 'Europe', 'Ireland': 'Europe', 'Italy': 'Europe',
    'Kosovo': 'Europe', 'Latvia': 'Europe', 'Liechtenstein': 'Europe', 'Lithuania': 'Europe',
    'Luxembourg': 'Europe', 'Malta': 'Europe', 'Moldova': 'Europe', 'Monaco': 'Europe',
    'Montenegro': 'Europe', 'Netherlands': 'Europe', 'North Macedonia': 'Europe',
    'Norway': 'Europe', 'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe',
    'Russia': 'Europe', 'San Marino': 'Europe', 'Serbia': 'Europe', 'Slovakia': 'Europe',
    'Slovenia': 'Europe', 'Spain': 'Europe', 'Sweden': 'Europe', 'Switzerland': 'Europe',
    'Ukraine': 'Europe', 'United Kingdom': 'Europe', 'Vatican City': 'Europe',
    'Australia': 'Oceania', 'Fiji': 'Oceania', 'Kiribati': 'Oceania',
    'Marshall Islands': 'Oceania', 'Micronesia': 'Oceania', 'Nauru': 'Oceania',
    'New Zealand': 'Oceania', 'Palau': 'Oceania', 'Papua New Guinea': 'Oceania',
    'Samoa': 'Oceania', 'Solomon Islands': 'Oceania', 'Tonga': 'Oceania',
    'Tuvalu': 'Oceania', 'Vanuatu': 'Oceania',
}

MONUMENTS_DATA = [
    {'name': 'Eiffel Tower', 'name_fr': 'Tour Eiffel', 'country': 'France', 'continent': 'Europe'},
    {'name': 'Statue of Liberty', 'name_fr': 'Statue de la Liberte', 'country': 'United States', 'continent': 'Americas'},
    {'name': 'Great Wall of China', 'name_fr': 'Grande Muraille de Chine', 'country': 'China', 'continent': 'Asia'},
    {'name': 'Colosseum', 'name_fr': 'Colisee', 'country': 'Italy', 'continent': 'Europe'},
    {'name': 'Taj Mahal', 'name_fr': 'Taj Mahal', 'country': 'India', 'continent': 'Asia'},
    {'name': 'Machu Picchu', 'name_fr': 'Machu Picchu', 'country': 'Peru', 'continent': 'Americas'},
    {'name': 'Pyramids of Giza', 'name_fr': 'Pyramides de Gizeh', 'country': 'Egypt', 'continent': 'Africa'},
    {'name': 'Big Ben', 'name_fr': 'Big Ben', 'country': 'United Kingdom', 'continent': 'Europe'},
    {'name': 'Sydney Opera House', 'name_fr': "Opera de Sydney", 'country': 'Australia', 'continent': 'Oceania'},
    {'name': 'Sagrada Familia', 'name_fr': 'Sagrada Familia', 'country': 'Spain', 'continent': 'Europe'},
    {'name': 'Christ the Redeemer', 'name_fr': 'Christ Redempteur', 'country': 'Brazil', 'continent': 'Americas'},
    {'name': 'Angkor Wat', 'name_fr': 'Angkor Vat', 'country': 'Cambodia', 'continent': 'Asia'},
    {'name': 'Burj Khalifa', 'name_fr': 'Burj Khalifa', 'country': 'United Arab Emirates', 'continent': 'Asia'},
    {'name': 'Acropolis', 'name_fr': 'Acropole', 'country': 'Greece', 'continent': 'Europe'},
    {'name': 'Stonehenge', 'name_fr': 'Stonehenge', 'country': 'United Kingdom', 'continent': 'Europe'},
    {'name': 'Alhambra', 'name_fr': 'Alhambra', 'country': 'Spain', 'continent': 'Europe'},
    {'name': 'Chichen Itza', 'name_fr': 'Chichen Itza', 'country': 'Mexico', 'continent': 'Americas'},
    {'name': 'Hagia Sophia', 'name_fr': 'Sainte-Sophie', 'country': 'Turkey', 'continent': 'Asia'},
    {'name': 'Petra', 'name_fr': 'Petra', 'country': 'Jordan', 'continent': 'Asia'},
    {'name': 'Mount Rushmore', 'name_fr': 'Mont Rushmore', 'country': 'United States', 'continent': 'Americas'},
    {'name': 'Leaning Tower of Pisa', 'name_fr': 'Tour de Pise', 'country': 'Italy', 'continent': 'Europe'},
    {'name': 'Kremlin', 'name_fr': 'Kremlin', 'country': 'Russia', 'continent': 'Europe'},
    {'name': 'Louvre Museum', 'name_fr': 'Musee du Louvre', 'country': 'France', 'continent': 'Europe'},
    {'name': 'Parthenon', 'name_fr': 'Parthenon', 'country': 'Greece', 'continent': 'Europe'},
    {'name': 'Vatican Museums', 'name_fr': 'Musees du Vatican', 'country': 'Vatican City', 'continent': 'Europe'},
    {'name': 'Notre-Dame Cathedral', 'name_fr': 'Cathedrale Notre-Dame', 'country': 'France', 'continent': 'Europe'},
    {'name': 'Forbidden City', 'name_fr': 'Cite Interdite', 'country': 'China', 'continent': 'Asia'},
    {'name': 'Golden Gate Bridge', 'name_fr': 'Pont du Golden Gate', 'country': 'United States', 'continent': 'Americas'},
    {'name': 'Neuschwanstein Castle', 'name_fr': 'Chateau de Neuschwanstein', 'country': 'Germany', 'continent': 'Europe'},
    {'name': 'Niagara Falls', 'name_fr': 'Chutes du Niagara', 'country': 'Canada', 'continent': 'Americas'},
]

SPORTS_DATA = [
    {'name': 'Cristiano Ronaldo', 'country': 'Portugal', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Europe'},
    {'name': 'Lionel Messi', 'country': 'Argentina', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Americas'},
    {'name': 'Serena Williams', 'country': 'United States', 'sport': 'Tennis', 'sport_fr': 'Tennis', 'continent': 'Americas'},
    {'name': 'LeBron James', 'country': 'United States', 'sport': 'Basketball', 'sport_fr': 'Basketball', 'continent': 'Americas'},
    {'name': 'Usain Bolt', 'country': 'Jamaica', 'sport': 'Athletics', 'sport_fr': 'Athletisme', 'continent': 'Americas'},
    {'name': 'Roger Federer', 'country': 'Switzerland', 'sport': 'Tennis', 'sport_fr': 'Tennis', 'continent': 'Europe'},
    {'name': 'Michael Phelps', 'country': 'United States', 'sport': 'Swimming', 'sport_fr': 'Natation', 'continent': 'Americas'},
    {'name': 'Neymar Jr.', 'country': 'Brazil', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Americas'},
    {'name': 'Novak Djokovic', 'country': 'Serbia', 'sport': 'Tennis', 'sport_fr': 'Tennis', 'continent': 'Europe'},
    {'name': 'Rafael Nadal', 'country': 'Spain', 'sport': 'Tennis', 'sport_fr': 'Tennis', 'continent': 'Europe'},
    {'name': 'Kylian Mbappe', 'country': 'France', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Europe'},
    {'name': 'Simone Biles', 'country': 'United States', 'sport': 'Gymnastics', 'sport_fr': 'Gymnastique', 'continent': 'Americas'},
    {'name': 'Mohamed Salah', 'country': 'Egypt', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Africa'},
    {'name': 'Eliud Kipchoge', 'country': 'Kenya', 'sport': 'Marathon', 'sport_fr': 'Marathon', 'continent': 'Africa'},
    {'name': 'Didier Drogba', 'country': 'Ivory Coast', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Africa'},
    {'name': 'Lewis Hamilton', 'country': 'United Kingdom', 'sport': 'Formula 1', 'sport_fr': 'Formule 1', 'continent': 'Europe'},
    {'name': 'Tiger Woods', 'country': 'United States', 'sport': 'Golf', 'sport_fr': 'Golf', 'continent': 'Americas'},
    {'name': 'Sachin Tendulkar', 'country': 'India', 'sport': 'Cricket', 'sport_fr': 'Cricket', 'continent': 'Asia'},
    {'name': 'Yao Ming', 'country': 'China', 'sport': 'Basketball', 'sport_fr': 'Basketball', 'continent': 'Asia'},
    {'name': 'Naomi Osaka', 'country': 'Japan', 'sport': 'Tennis', 'sport_fr': 'Tennis', 'continent': 'Asia'},
    {'name': 'Pele', 'country': 'Brazil', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Americas'},
    {'name': 'Wayne Gretzky', 'country': 'Canada', 'sport': 'Ice Hockey', 'sport_fr': 'Hockey sur glace', 'continent': 'Americas'},
    {'name': 'Carl Lewis', 'country': 'United States', 'sport': 'Athletics', 'sport_fr': 'Athletisme', 'continent': 'Americas'},
    {'name': 'Zinedine Zidane', 'country': 'France', 'sport': 'Football', 'sport_fr': 'Football', 'continent': 'Europe'},
    {'name': 'Michael Jordan', 'country': 'United States', 'sport': 'Basketball', 'sport_fr': 'Basketball', 'continent': 'Americas'},
]

MUSIC_DATA = [
    {'name': 'Beyonce', 'country': 'United States', 'genre': 'R&B/Pop', 'genre_fr': 'R&B/Pop', 'continent': 'Americas'},
    {'name': 'Michael Jackson', 'country': 'United States', 'genre': 'Pop', 'genre_fr': 'Pop', 'continent': 'Americas'},
    {'name': 'Bob Marley', 'country': 'Jamaica', 'genre': 'Reggae', 'genre_fr': 'Reggae', 'continent': 'Americas'},
    {'name': 'Celine Dion', 'country': 'Canada', 'genre': 'Pop', 'genre_fr': 'Pop', 'continent': 'Americas'},
    {'name': 'Shakira', 'country': 'Colombia', 'genre': 'Latin Pop', 'genre_fr': 'Pop latin', 'continent': 'Americas'},
    {'name': 'Rihanna', 'country': 'Barbados', 'genre': 'Pop/R&B', 'genre_fr': 'Pop/R&B', 'continent': 'Americas'},
    {'name': 'Adele', 'country': 'United Kingdom', 'genre': 'Pop/Soul', 'genre_fr': 'Pop/Soul', 'continent': 'Europe'},
    {'name': 'Ed Sheeran', 'country': 'United Kingdom', 'genre': 'Pop', 'genre_fr': 'Pop', 'continent': 'Europe'},
    {'name': 'Stromae', 'country': 'Belgium', 'genre': 'Electronic/Hip-hop', 'genre_fr': 'Electronique/Hip-hop', 'continent': 'Europe'},
    {'name': 'Angele', 'country': 'Belgium', 'genre': 'Pop', 'genre_fr': 'Pop', 'continent': 'Europe'},
    {'name': 'Youssou N\'Dour', 'country': 'Senegal', 'genre': 'World/Mbalax', 'genre_fr': 'Musique du monde/Mbalax', 'continent': 'Africa'},
    {'name': 'Fela Kuti', 'country': 'Nigeria', 'genre': 'Afrobeat', 'genre_fr': 'Afrobeat', 'continent': 'Africa'},
    {'name': 'Burna Boy', 'country': 'Nigeria', 'genre': 'Afrobeats', 'genre_fr': 'Afrobeats', 'continent': 'Africa'},
    {'name': 'Wizkid', 'country': 'Nigeria', 'genre': 'Afropop', 'genre_fr': 'Afropop', 'continent': 'Africa'},
    {'name': 'Davido', 'country': 'Nigeria', 'genre': 'Afrobeats', 'genre_fr': 'Afrobeats', 'continent': 'Africa'},
    {'name': 'BTS', 'country': 'South Korea', 'genre': 'K-Pop', 'genre_fr': 'K-Pop', 'continent': 'Asia'},
    {'name': 'Psy', 'country': 'South Korea', 'genre': 'K-Pop', 'genre_fr': 'K-Pop', 'continent': 'Asia'},
    {'name': 'A.R. Rahman', 'country': 'India', 'genre': 'Film Music', 'genre_fr': 'Musique de film', 'continent': 'Asia'},
    {'name': 'Jay Chou', 'country': 'Taiwan', 'genre': 'Mandopop', 'genre_fr': 'Mandopop', 'continent': 'Asia'},
    {'name': 'Kylie Minogue', 'country': 'Australia', 'genre': 'Pop', 'genre_fr': 'Pop', 'continent': 'Oceania'},
    {'name': 'Drake', 'country': 'Canada', 'genre': 'Hip-Hop/R&B', 'genre_fr': 'Hip-Hop/R&B', 'continent': 'Americas'},
    {'name': 'Taylor Swift', 'country': 'United States', 'genre': 'Pop/Country', 'genre_fr': 'Pop/Country', 'continent': 'Americas'},
    {'name': 'Elton John', 'country': 'United Kingdom', 'genre': 'Rock/Pop', 'genre_fr': 'Rock/Pop', 'continent': 'Europe'},
    {'name': 'Freddie Mercury', 'country': 'United Kingdom', 'genre': 'Rock', 'genre_fr': 'Rock', 'continent': 'Europe'},
    {'name': 'David Bowie', 'country': 'United Kingdom', 'genre': 'Rock', 'genre_fr': 'Rock', 'continent': 'Europe'},
]

GEOGRAPHY_DATA = {
    'rivers': [
        {'name': 'Nile', 'name_fr': 'Nil', 'continent': 'Africa', 'countries': ['Egypt', 'Sudan', 'Ethiopia']},
        {'name': 'Amazon', 'name_fr': 'Amazone', 'continent': 'Americas', 'countries': ['Brazil', 'Peru', 'Colombia']},
        {'name': 'Yangtze', 'name_fr': 'Yangzi Jiang', 'continent': 'Asia', 'countries': ['China']},
        {'name': 'Mississippi', 'name_fr': 'Mississippi', 'continent': 'Americas', 'countries': ['United States']},
        {'name': 'Volga', 'name_fr': 'Volga', 'continent': 'Europe', 'countries': ['Russia']},
        {'name': 'Congo', 'name_fr': 'Congo', 'continent': 'Africa', 'countries': ['DR Congo', 'Republic of the Congo']},
        {'name': 'Niger', 'name_fr': 'Niger', 'continent': 'Africa', 'countries': ['Nigeria', 'Mali', 'Niger']},
        {'name': 'Mekong', 'name_fr': 'Mekong', 'continent': 'Asia', 'countries': ['China', 'Laos', 'Thailand', 'Cambodia', 'Vietnam']},
        {'name': 'Danube', 'name_fr': 'Danube', 'continent': 'Europe', 'countries': ['Germany', 'Austria', 'Hungary', 'Romania']},
        {'name': 'Rhine', 'name_fr': 'Rhin', 'continent': 'Europe', 'countries': ['Germany', 'Netherlands', 'Switzerland']},
    ],
    'oceans': [
        {'name': 'Pacific Ocean', 'name_fr': 'Ocean Pacifique'},
        {'name': 'Atlantic Ocean', 'name_fr': 'Ocean Atlantique'},
        {'name': 'Indian Ocean', 'name_fr': 'Ocean Indien'},
        {'name': 'Arctic Ocean', 'name_fr': 'Ocean Arctique'},
        {'name': 'Southern Ocean', 'name_fr': 'Ocean Antarctique'},
    ],
    'seas': [
        {'name': 'Mediterranean Sea', 'name_fr': 'Mer Mediterranee', 'continent': 'Europe'},
        {'name': 'Caribbean Sea', 'name_fr': 'Mer des Caraibes', 'continent': 'Americas'},
        {'name': 'Red Sea', 'name_fr': 'Mer Rouge', 'continent': 'Africa'},
        {'name': 'Black Sea', 'name_fr': 'Mer Noire', 'continent': 'Europe'},
        {'name': 'South China Sea', 'name_fr': 'Mer de Chine meridionale', 'continent': 'Asia'},
        {'name': 'Arabian Sea', 'name_fr': 'Mer d\'Arabie', 'continent': 'Asia'},
    ],
    'deserts': [
        {'name': 'Sahara Desert', 'name_fr': 'Desert du Sahara', 'continent': 'Africa'},
        {'name': 'Arabian Desert', 'name_fr': 'Desert d\'Arabie', 'continent': 'Asia'},
        {'name': 'Gobi Desert', 'name_fr': 'Desert de Gobi', 'continent': 'Asia'},
        {'name': 'Kalahari Desert', 'name_fr': 'Desert du Kalahari', 'continent': 'Africa'},
        {'name': 'Patagonian Desert', 'name_fr': 'Desert de Patagonie', 'continent': 'Americas'},
        {'name': 'Great Victoria Desert', 'name_fr': 'Grand Desert de Victoria', 'continent': 'Oceania'},
        {'name': 'Syrian Desert', 'name_fr': 'Desert de Syrie', 'continent': 'Asia'},
        {'name': 'Namib Desert', 'name_fr': 'Desert du Namib', 'continent': 'Africa'},
    ],
}


# ------------------------------------------------------------------ #
#  FETCH FROM INTERNET
# ------------------------------------------------------------------ #
def fetch_countries_data():
    if not HAS_REQUESTS:
        return []
    try:
        resp = requests.get('https://restcountries.com/v3.1/all', timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"[!] REST Countries API failed: {e}")
        return []


# ------------------------------------------------------------------ #
#  QUESTION GENERATORS
# ------------------------------------------------------------------ #
def _other_options(pool, correct, n=3):
    others = [x for x in pool if x != correct]
    random.shuffle(others)
    return others[:n]


def generate_capital_questions(countries_data):
    questions = []
    if not countries_data:
        return questions
    name_capital = []
    for c in countries_data:
        name = c.get('name', {}).get('common', '')
        caps = c.get('capital', [])
        if name and caps:
            name_capital.append((name, caps[0]))
    all_capitals = [cap for _, cap in name_capital]
    all_countries = [n for n, _ in name_capital]
    for country, capital in name_capital:
        opts = _other_options(all_capitals, capital)
        if len(opts) < 3:
            continue
        # EN
        questions.append({
            'category': 'capitals', 'question_en': f"What is the capital of {country}?",
            'question_fr': f"Quelle est la capitale de {country}?",
            'answer': capital, 'option1': opts[0], 'option2': opts[1], 'option3': opts[2],
            'country': country, 'continent': _get_continent_from_api(c),
            'difficulty': 'medium', 'source': 'api',
        })
        # Reverse
        opt_countries = _other_options(all_countries, country)
        if len(opt_countries) >= 3:
            questions.append({
                'category': 'capitals', 'question_en': f"Which country has {capital} as its capital?",
                'question_fr': f"Quel pays a {capital} comme capitale?",
                'answer': country, 'option1': opt_countries[0], 'option2': opt_countries[1],
                'option3': opt_countries[2], 'country': country,
                'continent': _get_continent_from_api(c), 'difficulty': 'hard', 'source': 'api',
            })
    return questions


def generate_currency_questions(countries_data):
    questions = []
    if not countries_data:
        return questions
    name_currency = []
    for c in countries_data:
        name = c.get('name', {}).get('common', '')
        currencies = c.get('currencies', {})
        if name and currencies:
            cur_names = [v.get('name', k) for k, v in currencies.items()]
            name_currency.append((name, cur_names[0], _get_continent_from_api(c)))
    all_currencies = list({cur for _, cur, _ in name_currency})
    for country, currency, continent in name_currency:
        opts = _other_options(all_currencies, currency)
        if len(opts) < 3:
            continue
        questions.append({
            'category': 'currencies', 'question_en': f"What is the currency of {country}?",
            'question_fr': f"Quelle est la monnaie de {country}?",
            'answer': currency, 'option1': opts[0], 'option2': opts[1], 'option3': opts[2],
            'country': country, 'continent': continent, 'difficulty': 'medium', 'source': 'api',
        })
    return questions


def generate_president_questions():
    questions = []
    all_names = [name for name, _ in HEADS_OF_STATE.values()]
    for country, (leader_name, title) in HEADS_OF_STATE.items():
        opts = _other_options(all_names, leader_name)
        if len(opts) < 3:
            continue
        continent = COUNTRY_CONTINENT.get(country, '')
        questions.append({
            'category': 'presidents',
            'question_en': f"Who is the {title} of {country}?",
            'question_fr': f"Qui est le/la {title} de {country}?",
            'answer': leader_name, 'option1': opts[0], 'option2': opts[1], 'option3': opts[2],
            'country': country, 'continent': continent, 'difficulty': 'medium', 'source': 'static',
        })
    return questions


def generate_geography_questions():
    questions = []
    # Rivers
    all_rivers = [r['name'] for r in GEOGRAPHY_DATA['rivers']]
    for r in GEOGRAPHY_DATA['rivers']:
        country = r['countries'][0] if r['countries'] else ''
        opts = _other_options(all_rivers, r['name'])
        if len(opts) < 3:
            continue
        questions.append({
            'category': 'geography',
            'question_en': f"In which continent is the {r['name']} river located?",
            'question_fr': f"Sur quel continent se trouve le fleuve {r['name_fr']}?",
            'answer': r['continent'],
            'option1': _other_continent(r['continent']),
            'option2': _other_continent(r['continent']),
            'option3': _other_continent(r['continent']),
            'country': country, 'continent': r['continent'], 'source': 'static', 'difficulty': 'medium',
        })
    # Deserts
    all_deserts = [d['name'] for d in GEOGRAPHY_DATA['deserts']]
    for d in GEOGRAPHY_DATA['deserts']:
        opts = _other_options(all_deserts, d['name'])
        if len(opts) < 3:
            continue
        questions.append({
            'category': 'geography',
            'question_en': f"In which continent is the {d['name']} located?",
            'question_fr': f"Sur quel continent se trouve le {d['name_fr']}?",
            'answer': d['continent'],
            'option1': _other_continent(d['continent']),
            'option2': _other_continent(d['continent']),
            'option3': _other_continent(d['continent']),
            'country': '', 'continent': d['continent'], 'source': 'static', 'difficulty': 'easy',
        })
    # Seas
    all_seas = [s['name'] for s in GEOGRAPHY_DATA['seas']]
    for s in GEOGRAPHY_DATA['seas']:
        opts = _other_options(all_seas, s['name'])
        if len(opts) < 3:
            opts = (all_seas + all_seas)[:3]
        questions.append({
            'category': 'geography',
            'question_en': f"In which continent is the {s['name']} mainly located?",
            'question_fr': f"Sur quel continent se trouve principalement la {s['name_fr']}?",
            'answer': s['continent'],
            'option1': _other_continent(s['continent']),
            'option2': _other_continent(s['continent']),
            'option3': _other_continent(s['continent']),
            'country': '', 'continent': s['continent'], 'source': 'static', 'difficulty': 'medium',
        })
    return questions


def generate_monument_questions():
    questions = []
    all_countries = list({m['country'] for m in MONUMENTS_DATA})
    all_monuments = [m['name'] for m in MONUMENTS_DATA]
    for m in MONUMENTS_DATA:
        country_opts = _other_options(all_countries, m['country'])
        if len(country_opts) < 3:
            continue
        questions.append({
            'category': 'monuments',
            'question_en': f"In which country is the {m['name']} located?",
            'question_fr': f"Dans quel pays se trouve {m['name_fr']}?",
            'answer': m['country'],
            'option1': country_opts[0], 'option2': country_opts[1], 'option3': country_opts[2],
            'country': m['country'], 'continent': m['continent'], 'source': 'static', 'difficulty': 'medium',
        })
        other_m = _other_options(all_monuments, m['name'])
        if len(other_m) >= 3:
            questions.append({
                'category': 'monuments',
                'question_en': f"Which famous monument is located in {m['country']}?",
                'question_fr': f"Quel monument celebre se trouve en/au/aux {m['country']}?",
                'answer': m['name'],
                'option1': other_m[0], 'option2': other_m[1], 'option3': other_m[2],
                'country': m['country'], 'continent': m['continent'], 'source': 'static', 'difficulty': 'easy',
            })
    return questions


def generate_sports_questions():
    questions = []
    all_countries = list({s['country'] for s in SPORTS_DATA})
    all_sports = list({s['sport'] for s in SPORTS_DATA})
    for s in SPORTS_DATA:
        country_opts = _other_options(all_countries, s['country'])
        sport_opts = _other_options(all_sports, s['sport'])
        if len(country_opts) >= 3:
            questions.append({
                'category': 'sports',
                'question_en': f"Which country does {s['name']} represent in {s['sport']}?",
                'question_fr': f"Quel pays {s['name']} represente-t-il en {s['sport_fr']}?",
                'answer': s['country'],
                'option1': country_opts[0], 'option2': country_opts[1], 'option3': country_opts[2],
                'country': s['country'], 'continent': s['continent'], 'source': 'static', 'difficulty': 'medium',
            })
        if len(sport_opts) >= 3:
            questions.append({
                'category': 'sports',
                'question_en': f"In which sport is {s['name']} famous?",
                'question_fr': f"Dans quel sport {s['name']} est-il/elle celebre?",
                'answer': s['sport'],
                'option1': sport_opts[0], 'option2': sport_opts[1], 'option3': sport_opts[2],
                'country': s['country'], 'continent': s['continent'], 'source': 'static', 'difficulty': 'easy',
            })
    return questions


def generate_music_questions():
    questions = []
    all_countries = list({m['country'] for m in MUSIC_DATA})
    all_genres = list({m['genre'] for m in MUSIC_DATA})
    for m in MUSIC_DATA:
        country_opts = _other_options(all_countries, m['country'])
        genre_opts = _other_options(all_genres, m['genre'])
        if len(country_opts) >= 3:
            questions.append({
                'category': 'music',
                'question_en': f"Which country is {m['name']} from?",
                'question_fr': f"De quel pays vient {m['name']}?",
                'answer': m['country'],
                'option1': country_opts[0], 'option2': country_opts[1], 'option3': country_opts[2],
                'country': m['country'], 'continent': m['continent'], 'source': 'static', 'difficulty': 'medium',
            })
        if len(genre_opts) >= 3:
            questions.append({
                'category': 'music',
                'question_en': f"What genre of music is {m['name']} known for?",
                'question_fr': f"Dans quel genre musical {m['name']} est-il/elle connu(e)?",
                'answer': m['genre'],
                'option1': genre_opts[0], 'option2': genre_opts[1], 'option3': genre_opts[2],
                'country': m['country'], 'continent': m['continent'], 'source': 'static', 'difficulty': 'easy',
            })
    return questions


# ------------------------------------------------------------------ #
#  HELPERS
# ------------------------------------------------------------------ #
def _get_continent_from_api(country_data):
    region = country_data.get('region', '')
    sub = country_data.get('subregion', '')
    if region == 'Africa':
        return 'Africa'
    if region in ('North America', 'South America', 'Caribbean'):
        return 'Americas'
    if 'America' in region or 'America' in sub:
        return 'Americas'
    if region == 'Asia':
        return 'Asia'
    if region == 'Europe':
        return 'Europe'
    if region in ('Oceania', 'Antarctic'):
        return 'Oceania'
    return ''


_CONTINENTS = ['Africa', 'Americas', 'Asia', 'Europe', 'Oceania']


def _other_continent(current):
    others = [c for c in _CONTINENTS if c != current]
    return random.choice(others)


# ------------------------------------------------------------------ #
#  MAIN UPDATE FUNCTION
# ------------------------------------------------------------------ #
def update_all_questions(db):
    added = updated = 0

    def upsert_batch(batch):
        nonlocal added, updated
        for q in batch:
            result = db.upsert_question(q)
            if result == 'added':
                added += 1
            else:
                updated += 1

    # Internet-based
    countries_data = fetch_countries_data()
    if countries_data:
        upsert_batch(generate_capital_questions(countries_data))
        upsert_batch(generate_currency_questions(countries_data))

    # Static data
    upsert_batch(generate_president_questions())
    upsert_batch(generate_geography_questions())
    upsert_batch(generate_monument_questions())
    upsert_batch(generate_sports_questions())
    upsert_batch(generate_music_questions())

    return {'added': added, 'updated': updated, 'total': added + updated}
