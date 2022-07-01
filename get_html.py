import webbrowser
import requests

webbrowser.open('https://aws.amazon.com/ru/big-data/getting-started/tutorials/')


res = requests.get('https://aws.amazon.com/ru/big-data/getting-started/tutorials/')

print(type(res))
print(res.status_code == requests.codes.ok)
print(len(res.text))
print(res.text[:250])

try:
    res.raise_for_status()
except Exception as exc:
    print('A problem has arisen: %s' % (exc))


playFile = open('index.html', 'wb')

for chunk in res.iter_content(100000): 
    playFile.write(chunk)

playFile.close()

