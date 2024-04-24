# News Stand Vending Machine Test Bench using Cocotb
The RTL code simulates a newsstand vending machine. The DUT only accepts two types of coins: nickel (5C) and dime (10C). Newspapers cost 15C. The model has two outputs: 'newspaper' and 'change.' If the amount is exactly 15C, the 'newspaper' output asserts; if the amount is 20C, both outputs assert.

for example:
nickel -> nickel -> nickel = {'newspaper': 1, 'change': 0}
dime -> dime = {'newspaper': 1, 'change': 1}

## Coverage model
The coverage model gathers all valid transitions between FSM states (with some options omitted in the model(in todo list)). It utilizes the Cocotb-coverage package.

## Test Case
- Feature: News stand vending machine  
- Description: The DUT accepts either 5 or 10 cents and dispenses a newspaper if the total amount is 15 cents. If the total exceeds 15 cents, change is provided.  
## DUT
- Scenario: constraint random test
- Given: Unit Test Environment 
- When: Input is [(5C, 5C, 5C), (5C, 5C, 10C), (5C, 10C, 10C) ...]
- Then: Output is [(1,0), (1,1)...]

## Directories
- hdl: sv model
- tests: Cocotb bench

## What to install
- [install Icarus ](https://steveicarus.github.io/iverilog/usage/installation.html)
- [install cocotb] (https://docs.cocotb.org/en/stable/install.html)
- [install cocotb bus] (https://pypi.org/project/cocotb-bus/)
- [install cocotb coverage] (https://pypi.org/project/cocotb-coverage/)
- [install python-constraint] (https://pypi.org/project/python-constraint/)

## How to run
in tests directory run 'make'

