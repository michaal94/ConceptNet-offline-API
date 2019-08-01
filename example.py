from conceptNet import ConceptNet
from argparse import ArgumentParser

parser = ArgumentParser(description="Simple example for ConceptNet offline API")
parser.add_argument('-p', '--path', default='assertions.csv', help='Path to database')
args = parser.parse_args()


def main(args):
    db_path = args.path
    if 'assertions.csv' in db_path:
        # If the full db used let's reduce to english
        conceptnet = ConceptNet(db_path, language='english', save_language=True)
    else:
        conceptnet = ConceptNet(db_path)


    dog = conceptnet.get_query(start=['dog', 'cat'], end=['cat', 'car'])
    dog.process_data()
    print(dog.processed_df.to_string())
    dog_cat = dog.get_query(end=['cat'])
    dog_cat.process_data()
    print(dog_cat.processed_df.to_string())
    # print(len(conceptnet))

    # print(a.processed_df.JSON.to_string())
    # print(a.processed_df.JSON[0]['surfaceEnd'])

    # print(a.df.start)
    # b = conceptnet.get_query(start=['horse'], relation=['RelatedTo'])
    # print(b.df.start)


if __name__ == "__main__":
    main(args)
