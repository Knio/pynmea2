import pynmea2

file = open('data.log', encoding='utf-8') # Replaced example/data.log with data.log

for line in file.readlines():
    try:
        msg = pynmea2.parse(line)
        print(repr(msg))
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue
