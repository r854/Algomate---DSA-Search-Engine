import json
# Load JSON data from a file
with open('../scrapping/Leetcode1.json','r') as file:
  total_with_duplicates = json.load(file)

with open('LeetcodeUnique.json','r') as file:
  unique_total = json.load(file)

with open('../filtering/FreeLeetcode.json','r') as file:
  free_total = json.load(file)

with open('../filtering/PremiumLeetcode.json','r') as file:
  premium_total = json.load(file)

print(len(total_with_duplicates))
print(len(unique_total))
print(len(free_total))
print(len(premium_total))

