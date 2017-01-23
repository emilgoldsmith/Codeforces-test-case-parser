#!/usr/bin/python3
from sys import argv
from subprocess import run, PIPE
from time import time

# This parse break should be the same in your get test cases file
PARSE_BREAK = "BREAK PARSE HERE\n"

problem_letter = argv[1].lower()
check_output = len(argv) > 2 and int(argv[2])
inp = open(problem_letter.upper() + '.txt', 'r')
out = open(problem_letter.upper() + '.out', 'r')
num_cases = int(inp.readline())
for i in range(1, num_cases + 1):
  case_input = ""
  line = inp.readline()
  while line != PARSE_BREAK:
    case_input += line
    line = inp.readline()
  start_time = time()
  output = run(["./" + problem_letter + ".exe"],
    input=case_input.encode('utf-8'), stdout=PIPE).stdout.decode('utf-8')
  time_taken = time()-start_time
  if check_output:
    case_output = ""
    line = out.readline()
    while line != PARSE_BREAK:
      case_output += line
      line = out.readline()
    print("Case #{}: {}".format(i, case_output == output))
    print("Time taken: {}".format(time_taken))
    if case_output != output:
      print("Input:")
      print(case_input, end='')
      print("Your output:")
      print(output, end='')
      print("Correct output:")
      print(case_output, end='')
  else:
    print("Case #{}:".format(i))
    print(output, end='')
    print("Time taken: {}".format(time_taken))
  print()
inp.close()
out.close()