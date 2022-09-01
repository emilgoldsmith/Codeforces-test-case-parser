#!/usr/bin/python3
from sys import argv
from subprocess import STDOUT, run, PIPE
from time import time
import json

# This parse break should be the same in your get test cases file
PARSE_BREAK = "BREAK PARSE HERE\n"

problem_letter = argv[1].lower()
check_output = len(argv) > 2 and int(argv[2])
inp = open(problem_letter.upper() + ".txt", "r")
out = open(problem_letter.upper() + ".out", "r")
num_cases = int(inp.readline())
if int(out.readline()) != num_cases and check_output:
    print("Error: Number of test cases in input and answer files are different")
    exit()
for i in range(1, num_cases + 1):
    case_input = ""
    line = inp.readline()
    while line != PARSE_BREAK:
        case_input += line
        line = inp.readline()
    start_time = time()
    output = run(
        ["./" + problem_letter[0].lower() + ".exe"],
        input=case_input.encode("utf-8"),
        stdout=PIPE,
        stderr=PIPE,
    )
    time_taken = time() - start_time
    if check_output:
        case_output = ""
        line = out.readline()
        while line != PARSE_BREAK:
            case_output += line.rstrip() + "\n"
            line = out.readline()
        if output.stdout.decode("utf-8")[-1] != "\n":
            print("OUTPUT MUST END IN NEWLINE")
            break
        processed_actual_output = (
            "\n".join(
                map(lambda s: s.rstrip(), output.stdout.decode("utf-8").splitlines())
            )
            + "\n"
        )
        case_was_correct = case_output == processed_actual_output
        print("Case #{}: {}".format(i, case_was_correct))
        print("Time taken: {}".format(time_taken))
        if not case_was_correct:
            print("Input:")
            print(case_input, end="")
            print("Your stderr:")
            print(output.stderr.decode("utf-8"), end="")
            print("Your output:")
            print(processed_actual_output, end="")
            print("Correct output:")
            print(case_output, end="")
    else:
        print("Case #{}:".format(i))
        print(output, end="")
        print("Time taken: {}".format(time_taken))
inp.close()
out.close()
