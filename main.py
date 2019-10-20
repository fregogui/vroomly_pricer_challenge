import pandas as pd
import argparse

def compute_price(vehicle, intervention):
    if intervention == "front_brake_pads":
        return compute_price_front_brake_pads(vehicle)
    if intervention == "front_brake_rotors_and_pads":
        return compute_price_front_brake_rotors_and_pads(vehicle)
    if intervention == "oil_change":
        return compute_price_oil_change(vehicle)


def compute_price_front_brake_pads(vehicle):
    article_ids = get_article_ids(vehicle, "brake_pad")
    return 4 * get_median_price(article_ids, 4)

def compute_price_front_brake_rotors_and_pads(vehicle):
    article_ids_rotors = get_article_ids(vehicle, "brake_rotor")
    article_ids_brake_pad = get_article_ids(vehicle, "brake_pad")
    return 2 * get_median_price(article_ids_rotors, 2) + 4 * get_median_price(article_ids_brake_pad, 4)

def compute_price_oil_change(vehicle):
    year = int(list(vehicles[vehicles["id"] == vehicle]["production_start"])[0][:4])
    motor_oil_volume = (list(vehicles[vehicles["id"] == vehicle]["motor_oil_volume"])[0])
    oil_volumic_price = get_oil_volumic_price(year)
    return motor_oil_volume * oil_volumic_price + get_median_price(get_article_ids(vehicle,"fuel_filter"),1)


def get_article_ids(vehicle, type):
    articles_compatible = relations[relations["vehicle_id"] == vehicle]
    articles_compatible = pd.merge(articles_compatible, articles, left_on="article_id", right_on="id")
    articles_compatible = articles_compatible[articles_compatible["type"] == type]
    return list(articles_compatible["id"])

def get_median_price(article_ids, min_available):
    valid_references = catalog[(catalog["quantity"].astype(int) >= min_available) & (catalog["article_id"].isin(article_ids))]
    median_price = valid_references["price"].median()
    return median_price
    #prendre en compte pas de dispo

def parse_all_catalogs():
    catalog_1 = pd.read_csv("./data/catalogs/auto_distribution.csv", decimal=",")
    catalog_1.rename(columns={
        "Quantity": "quantity",
        "Price": "price",
        "Part number": "article_id",
    }, inplace=True)
    catalog_2 = pd.read_csv("./data/catalogs/acr.csv", decimal=".", delimiter=";")
    catalog_2.rename(columns={
        "qté": "quantity",
        "prix total HT": "price",
        "ref article": "article_id",
    }, inplace=True)

    catalog_3 = pd.read_csv("./data/catalogs/golda.csv")
    catalog_3.rename(columns={
        "Quantité": "quantity",
        "Prix total": "price",
        "Référence pièce": "article_id",
    }, inplace=True)
    return pd.concat([catalog_1, catalog_2, catalog_3])

def get_oil_volumic_price(year):
    if year >= 2007:
        return 8.0
    elif 2002 <= year < 2007:
        return 6.0
    else:
        return 5.0


if __name__ == "__main__":
    vehicles = pd.read_csv("./data/vehicles.csv")
    articles = pd.read_csv("./data/articles.csv")
    relations = pd.read_csv("./data/article_vehicle_relations.csv")
    catalog = parse_all_catalogs()

    parser = argparse.ArgumentParser()
    parser.add_argument('--intervention')
    parser.add_argument('--vehicle', type=int)
    args = parser.parse_args()


    price = compute_price(args.vehicle, args.intervention)
    print("Le prix : {}".format(str(price)))
