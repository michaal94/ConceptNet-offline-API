from conceptNet import ConceptNet
import time

# conceptnet = ConceptNet('assertions.csv', language='english', save_language=True)


conceptnet = ConceptNet('assertions_english.pkl')
start_time = time.time()
# a = conceptnet.get_query(start=['apple'])
dog = conceptnet.get_query(start='dog', end=['cat', 'car'])
# raw_data = a.get_raw_dataframe()
end_time = time.time()
# print(end_time - start_time)
start_time = time.time()
# j = raw_data.JSON
# print(raw_data.to_string())
# print(j)
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

