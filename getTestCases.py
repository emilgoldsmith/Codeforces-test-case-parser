#!/usr/bin/python3

from urllib.request import urlopen
from sys import argv
from html.parser import HTMLParser

# This parse break should be the same in your run file
PARSE_BREAK = "BREAK PARSE HERE\n"

class problem_parser(HTMLParser):
  def __init__(self):
    HTMLParser.__init__(self)
    self.reading = False
    self.input = []
    self.output = []
    self.buffer = ""

  def handle_starttag(self, tag, attrs):
    if tag == "pre":
      self.reading = True

  def handle_endtag(self, tag):
    if tag == "pre":
      self.reading = False
      if len(self.input) == len(self.output):
        self.input.append(self.buffer)
      else:
        self.output.append(self.buffer)
      self.buffer = ""

  def handle_data(self, data):
    if self.reading:
      self.buffer += data + '\n'

contest_number = argv[1]

problem_letter = 'A'
while True:
  url = 'http://codeforces.com/contest/' + contest_number + '/problem/' + problem_letter
  problem = urlopen(url)
  if problem.geturl() != url:
    break
  else:
    print("Fetching problem", problem_letter)
    text = problem.read()
    parser = problem_parser()
    parser.feed(text.decode('utf-8'))
    if len(parser.input) != len(parser.output):
      print("Error with problem", problem_letter)
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
  print("Fetch successful")
  problem_letter = chr(ord(problem_letter)+1)

