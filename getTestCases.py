#!/usr/bin/python3

from urllib.request import urlopen
from sys import argv
from html.parser import HTMLParser
import requests

# This parse break should be the same in your run file
PARSE_BREAK = "BREAK PARSE HERE\n"

class problem_parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.reading = False
    self.input = []
    self.output = []
    self.buffer = ""
    self.atTests = False
    self.level = 0

  def handle_starttag(self, tag, attrs):
    if tag == 'div' and ('class', 'sample-tests') in attrs:
      self.atTests = True

    if self.atTests:
      self.level += 1

    if tag == "pre" and self.atTests:
      self.reading = True

  def handle_endtag(self, tag):
    if self.atTests:
      self.level -= 1
      if self.level == 0:
        self.atTests = False

    if tag == "pre" and self.atTests:
      self.reading = False
      if len(self.input) == len(self.output):
        self.input.append(self.buffer)
      else:
        self.output.append(self.buffer)
      self.buffer = ""

  def handle_data(self, data):
    if self.reading:
      self.buffer += data.strip() + '\n'

contest_number = argv[1]
response = requests.get('http://www.codeforces.com/api/contest.standings', params={'contestId': contest_number, 'handles': 'Goldsmith94'})

response.raise_for_status()
problem_names = map(lambda x: x['index'], response.json()['result']['problems'])
for problem_letter in problem_names:
  print("Fetching problem", problem_letter)
  url = 'http://codeforces.com/contest/' + contest_number + '/problem/' + problem_letter
  problem = urlopen(url)
  if problem.geturl() != url:
    print("Testcases not found")
    break
  else:
    print("Fetch successful")
    text = problem.read()
    parser = problem_parser()
    parser.feed(text.decode('utf-8'))
    if len(parser.input) != len(parser.output):
      print("Error with problem", problem_letter)
      print(parser.input)
      print(parser.output)
    else:
      inp = open(problem_letter + '.txt', 'w')
      inp.write(str(len(parser.input)) + '\n')
      for test_case in parser.input:
        inp.write(test_case)
        inp.write(PARSE_BREAK)
      inp.close()
      out = open(problem_letter + '.out', 'w')
      out.write(str(len(parser.output)) + '\n')
      for test_case in parser.output:
        out.write(test_case)
        out.write(PARSE_BREAK)
      out.close()
