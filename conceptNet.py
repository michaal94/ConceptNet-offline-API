import pandas as pd
import os
import numpy as np
import time


# TODO: fill langs list
lang_dict = {
    'english': 'en'
}


class ConceptNet():
    def __init__(self, data_path, language=None, save_language=False):
        # Check extenstion and load data to pandas dataframe
        base, extention = os.path.splitext(data_path)
        if extention == '.csv':
            df = pd.read_csv(data_path, sep='\t', header=None,
                             names=['URI', 'relation', 'start', 'end', 'JSON'])
        elif extention == '.pkl':
            df = pd.read_pickle(data_path)

        # strip non-relevant languages (a lot of free memory)
        if language is not None:
            lang_abbr = '/' + get_language_abbr(language) + '/'
            index = df[~df.start.str.contains(lang_abbr)].index
            df.drop(index, inplace=True)
            index = df[~df.end.str.contains(lang_abbr)].index
            df.drop(index, inplace=True)
            # save if needed for further use
            if save_language:
                df.to_pickle(base + '_' + language + '.pkl')

        self.df = df

    # Functions to query relevant fields
    def get_edges_from_start(self, start_tokens, dataframe=None):
        start_tokens = self.process_tokens(start_tokens)
        if dataframe is None:
            edges = self.df[self.df.start.str.contains('|'.join(start_tokens))]
        else:
            edges = dataframe[dataframe.start.str.contains('|'.join(start_tokens))]
        return edges

    def get_edges_to_end(self, end_tokens, dataframe=None):
        end_tokens = self.process_tokens(end_tokens)
        if dataframe is None:
            edges = self.df[self.df.end.str.contains('|'.join(end_tokens))]
        else:
            edges = dataframe[dataframe.end.str.contains('|'.join(end_tokens))]
        return edges

    def get_edges_by_relation(self, relation_tokens, dataframe=None):
        relation_tokens = self.process_tokens(relation_tokens, relation=True)
        if dataframe is None:
            edges = self.df[self.df.relation.str.contains('|'.join(relation_tokens))]
        else:
            edges = dataframe[dataframe.relation.str.contains('|'.join(relation_tokens))]
        return edges

    # Full query for all possible fields
    def get_query(self, start=None, end=None, relation=None, timing=False):
        if timing:
            start_time = time.time()
        edges = self.df
        if start is not None:
            edges = self.get_edges_from_start(start, dataframe=edges)
        if end is not None:
            edges = self.get_edges_to_end(end, dataframe=edges)
        if relation is not None:
            edges = self.get_edges_by_relation(relation, dataframe=edges)
        # make a copy of small portion of data
        # you can then work on and change small queries without changing main
        edges = edges.copy()
        # reset indices - mainly because it looks much nicer
        edges.reset_index(drop=True, inplace=True)
        if timing:
            time_passed = time.time() - start_time
            print("Query returned in %.4f", )
        return EdgeFrame(edges)

    def process_tokens(self, token_list, relation=False):
        processed_list = []
        for token in token_list:
            new_token = token
            # lower case as the concept net is
            if not relation:
                new_token = token.lower().replace(' ', '_')
            # Put regex such that word starts with / (like /c/en/word)
            # and ends up with / or nothing - in order to match exact words
            # Basically mach the exact word after two preceeding symbols
            # beginning with /
            new_token = ('^\\/[^\\/]*\\/[^\\/]*\\/' + new_token +
                         '\\/|^\\/[^\\/]*\\/[^\\/]*\\/' + new_token + '$')
            processed_list.append(new_token)
        return processed_list

    def __len__(self):
        return len(self.df)


class EdgeFrame(ConceptNet):
    def __init__(self, dataframe):
        self.df = dataframe

    def get_raw_dataframe(self):
        return self.df

    def process_data(self):
        self.processed_df = self.df.copy()
        self.processed_df = self.processed_df.reindex(columns=(list(self.processed_df.columns.values) + ['startPoS', 'endPoS', 'startHypernym', 'endHypernym', 'startSurface', 'endSurface', 'surfaceText', 'weight']))
        # Deal with empty query case
        if len(self.processed_df) != 0:
            self.processed_df[['start', 'startPoS', 'startHypernym']] = self.processed_df[['start', 'startPoS', 'startHypernym']].apply(process_node_tokens, axis=1)
            self.processed_df[['end', 'endPoS', 'endHypernym']] = self.processed_df[['end', 'endPoS', 'endHypernym']].apply(process_node_tokens, axis=1)
            self.processed_df[['startSurface', 'endSurface', 'surfaceText', 'weight']] = self.processed_df[['JSON']].apply(process_JSON, axis=1)
            self.processed_df['relation'] = self.processed_df['relation'].map(process_relation)
        self.processed_df.drop(columns=['URI', 'JSON'], inplace=True)


def process_node_tokens(cols):
    split = cols[0].strip('/').split('/')[2:]
    name, pos, hypernym = np.nan, np.nan, np.nan
    if len(split) > 2:
        if split[2] in ['wp', 'wn']:
            hypernym = split[3]
            split = split[:-2]
    if len(split) > 1:
        pos = split[1]
    name = split[0]
    return pd.Series([name, pos, hypernym])


def process_relation(relation):
    split = relation.strip('/').split('/')
    if len(split) > 2:
        return split[2]
    else:
        return split[1]


def process_JSON(json_col):
    json_col = eval(json_col.values[0])
    startSurface, endSurface, surfaceText, weight = np.nan, np.nan, np.nan, np.nan
    if 'surfaceStart' in json_col:
        startSurface = json_col['surfaceStart']
    if 'surfaceEnd' in json_col:
        endSurface = json_col['surfaceEnd']
    if 'surfaceText' in json_col:
        surfaceText = json_col['surfaceText']
    if 'weight' in json_col:
        weight = json_col['weight']

    series = [startSurface, endSurface, surfaceText, weight]

    return pd.Series(series)


def get_language_abbr(language):
    if language in lang_dict:
        return lang_dict[language]
    else:
        raise NotImplementedError('Language not implemented or not present')
