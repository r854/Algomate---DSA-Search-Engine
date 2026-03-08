import json
#Filters out only the unique question from Leetcode1.json and writes it to LeetcodeUnique.json
input = "scrapping/Leetcode1.json"
output = "LeetcodeUnique.json"
# Read the JSON file
with open(input, 'r') as file:
    data = json.load(file)
print("Total No of Questions before cleaning : %d" %(len(data)))
# Create an empty list for unique elements
unique_elements = []

# Iterate over each JSON object
for item in data:
    # Check if the item is already in the unique list
    if item not in unique_elements:
        # Append the item to the unique list
        unique_elements.append(item)

print("Total No of questions after removing duplicates : %d "%(len(unique_elements)))
# Write the unique elements list to a new JSON file
with open(output, 'w') as file:
    json.dump(unique_elements, file, indent=4)
