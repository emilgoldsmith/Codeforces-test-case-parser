# Codeforces Test Case Parser

This is two scripts that fit together. getTestCases.py accesses the Codeforces website, fetches the sample tests for each problem of the given contest, and puts them formatted into two seperate text files for input and correct output. run.py runs your executable on all the test cases, and if prompted to checks if they fit the correct answers.

## Usage

To get the test cases you need to first find the contest number (not the round number), which is found in the url of the contest amongst other places, if the number is for example 754 you run:

`./getTestCases.py 754`

and all the test cases will be downloaded to your current directory in the format "Problem Letter".txt and "Problem Letter".out.

To run your tests you should have your executable named "Lowercase Problem Letter".exe like for example a.exe, b.exe etc. run.py is run with two arguments: The problem letter and whether you want to check your output run like this:

`./run.py a`

for not checking answers, and:

`./run.py a 1`

for checking answers.
