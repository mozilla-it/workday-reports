# python-library-template

A github repo template with some minimal best practices


## Development Environment Setup

### Pipenv Setup

Install all regular env dependencies of the Pipfile in the current directory:
* `pipenv install`

Install ALL deps including DEV env dependencies of the Pipfile in the current directory:
* `pipenv install -dev`

Opens shell with corresponding dependencies to the pipfile(.lock) in the directory that you make the call.
* `pipenv shell`


### Install Pre-commit

Using Pipenv (pre-commit is located in the [Pipfile](./Pipfile))
* `pipenv shell`
* `pre-commit install`

You should get the following response after installing pre-commit:

>`pre-commit installed at .git/hooks/pre-commit`

### Pre-commit, Run on the Entire Codebase

Run the following command where you installed pre-commit.
* `pre-commit run --all-files`

### Exiting Pipenv Shell

Run the following command to exit `pipenv shell` while in a shell.
* `exit`

The command `deactivate` will not work to full disengage the pipenv shell as it does with `venv`.



#### Setup Build

To build the Python binary distribution, execute the following command line statement
in a terminal after meeting the project prerequisites:

`python setup.py build`

### Best practices

Test coverage should be at least 80% and before merging it should be approved by at least one team member.

Before merging a PR, we can use pylint which provides good static analysis in addition of PEP-8 recommendations provided by PyCharm. Not all recommendations must be followed but it improves the code readability. It includes stuff like variables rename and spacing and documentation.

Another recommendation would be to run coverage which provides a good summary about test coverage. Posting the output would let the team members know if your additions increased or decreased test coverage.

Also, when adding unit tests, it would be good to post output of a unit test run of all modules, this makes sure your PR does not break your or anybody else's unit tests before the actual commit and travis finds out that something broke on last commit.

Unit tests best practices:\
  Unit Tests Should Be Trustworthy\
  Unit Tests Should Be Maintainable and Readable\
  Unit Tests Should Verify a Single-Use Case\
  Unit Tests Should Be Isolated\
  Unit Tests Should Be Automated\
  Use a Good Mixture of Unit and Integration Tests\
  Unit Tests Should Be Executed Within an Organized Test Practice
