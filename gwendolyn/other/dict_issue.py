

data = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
}

keys = ['one', 'two', 'three', 'four']
values = [1, 2, 3, 4]


data_keys = list(data.keys())
data_values = list(data.values())

def get_index_of(number):
    return data_keys.index(number)

process_data = lambda x: x**2

key_index = get_index_of('two') # I want a second element
key = data_keys[key_index]
# pass value to another function
print(process_data(data[key]))
