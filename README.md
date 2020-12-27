# Mindustry Logic Preprocessor

## What does it do?
This tool preprocesses a custom variant of Mindustry Logic (similar to Assembly). It takes as input either a file or
stdin, and outputs to either a file or stdout.

Currently, this tool supports:
* Labels
  ```
  jump :label1 notEqual @unit null
  ubind @mono
  label1:
  end
  ```
  becomes
  ```
  jump 3 notEqual @unit null
  ubind @mono
  end
  ```

## Requirements
* Python 3.6 or greater: https://www.python.org/downloads/

## Usage
Examples of how to use this tool are:
* `python mproc.py -f input.txt`
* `python mproc.py -f input.txt -o output.txt`
* `cat input.txt | python mproc.py`
