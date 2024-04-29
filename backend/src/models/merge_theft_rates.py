import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

json_obj1 = load_json('predicted_theft_rates_2015_2024.json')
json_obj2 = load_json('n_nhtsa_theft_rates.json')

merged_dict = json_obj1.copy()
merged_dict.update(json_obj2)

with open('merged_theft_data.json', 'w') as file:
    json.dump(merged_dict, file, indent=4, sort_keys=True)

print("Merged JSON saved to 'path_to_output_file.json'")
