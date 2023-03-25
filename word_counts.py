from collections import Counter

with open(r"D:/C/The pot of basil.txt", "r", encoding = "latin-1") as file:
    text = file.read()
 
text.replace("\n", "")
text.replace("\r", "")
text = text.split(" ")
text = [word.strip() for word in text]

for (word, count) in Counter(text).items():
    print(f"{word} -> {count:6}")