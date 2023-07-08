import pandas as pd
import numpy as np
import warnings
from branca.element import Figure

def add_noise(position, std_dev):
    noise = np.random.normal(0, std_dev, size=2)
    return position + noise

def fill_geo_position(row, geo_dict, std_dev_street_only, std_dev_neighborhood, neighborhood_position):
    street = row['adress_street']
    number = row['adress_number']
    position = row['adress_geoPosition']
    
    if pd.notnull(street) and pd.notnull(number):
        if pd.isnull(position):
            warnings.warn(f"Missing 'adress_geoPosition' for index {index}.")
        return row
    
    if pd.notnull(street):
        position = add_noise(geo_dict.get(street), std_dev_street_only)
    else:
        position = add_noise(neighborhood_position, std_dev_neighborhood)
    
    row['adress_geoPosition'] = f"{position[0]}, {position[1]}"
    return row

def main():
    file_path = 'data.xlsx'
    df = pd.read_excel(file_path)

    adress_geo_dictionary = {
        "רמת אביב": "32.107803983256574, 34.79745911801873",
        "רדינג": "32.10863280135009, 34.79420501778429",
        "נח": "32.10867937529205, 34.796604614274045", 
        "יהודה קרני": "32.105881575738216, 34.79391990908976", 
        "בארט": "32.11400349388932, 34.799108845360664",
        "שמעוני": "32.107415018542625, 34.79331004144532",
        "טאגור": "32.11652765239608, 34.7964749105849",
        "איינשטיין": "32.11302490792603, 34.79702834072538", 
        "אשר ברש": "32.109866233713205, 34.79498203490411",
        "הסבוראים": "32.117055556255345, 34.79423856441824",
        "חיים לבנון": "32.107203461864216, 34.80084437994166",
        "פיליכובסקי": "32.1165368380021, 34.80069234263218",
        "פסטרנק": "32.11796141491212, 34.79644879937829",
        "פרנקל": "32.111223911856165, 34.79937541655008",
        "ברזיל": "32.11111337366112, 34.79504005683053"
    }

    geo_dict = {street: np.array(position.split(', '), dtype=float)
                for street, position in adress_geo_dictionary.items()}

    std_dev_street_only = 0.0001
    std_dev_neighborhood = 0.001

    neighborhood_position = geo_dict["רמת אביב"]

    df = df.apply(fill_geo_position, args=(geo_dict, std_dev_street_only, std_dev_neighborhood, neighborhood_position), axis=1)

    # Further processing or analysis

if __name__ == "__main__":
    main()
