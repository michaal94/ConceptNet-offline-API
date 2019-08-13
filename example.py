from conceptNet import ConceptNet
from argparse import ArgumentParser

parser = ArgumentParser(description="Simple example for ConceptNet offline API")
parser.add_argument('-p', '--path', default='assertions.csv', help='Path to database')
parser.add_argument('-s', '--start', default='dog', help='Start node')
parser.add_argument('-e', '--end', default=['cat', 'tail', 'pet'], help='End node')
parser.add_argument('-r', '--relation', default='IsA', help='Relation between nodes')
args = parser.parse_args()


def main(args):
    db_path = args.path
    if 'assertions.csv' in db_path:
        # If the full db used let's reduce to english
        conceptnet = ConceptNet(db_path, language='english', save_language=True)
    else:
        conceptnet = ConceptNet(db_path)

    start = args.start
    end = args.end
    relation = args.relation

    print('Database has %d entries' % len(conceptnet))
    print('')

    print('You can use couple of arguments for the query at the same time.')
    print('The following results are obtained, when searching for %s as a start node and %s as the end.' % (start, end))
    start_end = conceptnet.get_query(start=start, end=end, timing=True)

    print('')
    print('Raw form of data:')
    print(start_end.get_raw_dataframe().head())

    print('')
    print('You can process data to more clear format:')
    start_end.process_data()
    print(start_end.processed_df.to_string())

    print('')
    print('You can call query on query, so that just by calling results on the previous answer, you obtain:')
    print('You are now querying the database with only %d entries' % len(start_end))
    full_query = start_end.get_query(relation=relation, timing=True)
    full_query.process_data()
    print(full_query.processed_df.to_string())


if __name__ == "__main__":
    main(args)
