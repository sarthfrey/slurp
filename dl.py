import requests

r = requests.get('http://norvig.com/ngrams/count_2w.txt')
f = open('bigram.txt', 'w')
f.write(r.content)
