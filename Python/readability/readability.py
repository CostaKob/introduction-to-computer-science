from cs50 import get_string



text = get_string("Text: " )

letters = 0.0
words = 0.0
sentences = 0.0

for char in text:
    if char.islower() or char.isupper():
        letters += 1
    if char == " ":
        words += 1
    if char == "." or char == "!" or char =="?":
        sentences += 1

words +=1

averageLetters = (letters / words) * 100
averageSentences = (sentences / words) * 100
index = round(0.0588 * averageLetters - 0.296 * averageSentences - 15.8)

if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")

