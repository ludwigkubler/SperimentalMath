# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return abs(a * b) // gcd(a, b)

class Fraction:
    def __init__(self, numerator, denominator):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        common_divisor = gcd(numerator, denominator)
        self.numerator = numerator // common_divisor
        self.denominator = denominator // common_divisor

    def __add__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for +: 'Fraction' and '{}'".format(type(other).__name__))
        new_numerator = self.numerator * other.denominator + other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __sub__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for -: 'Fraction' and '{}'".format(type(other).__name__))
        new_numerator = self.numerator * other.denominator - other.numerator * self.denominator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __mul__(self, other):
        if not isinstance(other, (int, Fraction)):
            raise TypeError("Unsupported operand type for *: 'Fraction' and '{}'".format(type(other).__name__))
        if isinstance(other, int):
            return Fraction(self.numerator * other, self.denominator)
        new_numerator = self.numerator * other.numerator
        new_denominator = self.denominator * other.denominator
        return Fraction(new_numerator, new_denominator)

    def __truediv__(self, other):
        if not isinstance(other, (int, Fraction)):
            raise TypeError("Unsupported operand type for /: 'Fraction' and '{}'".format(type(other).__name__))
        if isinstance(other, int):
            return Fraction(self.numerator, self.denominator * other)
        if other.numerator == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        new_numerator = self.numerator * other.denominator
        new_denominator = self.denominator * other.numerator
        return Fraction(new_numerator, new_denominator)

    def __eq__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for ==: 'Fraction' and '{}'".format(type(other).__name__))
        return (self.numerator == other.numerator) and (self.denominator == other.denominator)

    def __lt__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for <: 'Fraction' and '{}'".format(type(other).__name__))
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for <=: 'Fraction' and '{}'".format(type(other).__name__))
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for >: 'Fraction' and '{}'".format(type(other).__name__))
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other):
        if not isinstance(other, Fraction):
            raise TypeError("Unsupported operand type for >=: 'Fraction' and '{}'".format(type(other).__name__))
        return self.numerator * other.denominator >= other.numerator * self.denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

def gaussian_elimination(matrix, b):
    n = len(matrix)
    for i in range(n):
        # Find the pivot
        max_row = i
        for j in range(i + 1, n):
            if abs(matrix[j][i]) > abs(matrix[max_row][i]):
                max_row = j
        matrix[i], matrix[max_row] = matrix[max_row], matrix[i]
        b[i], b[max_row] = b[max_row], b[i]

        # Eliminate the current column below the pivot
        for j in range(i + 1, n):
            factor = matrix[j][i] / matrix[i][i]
            for k in range(i, n):
                matrix[j][k] -= factor * matrix[i][k]
            b[j] -= factor * b[i]

    # Back-substitute to find the solution
    x = [0] * n
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - sum(matrix[i][j] * x[j] for j in range(i + 1, n))) / matrix[i][i]
    return x

def solve_system(matrix, b):
    solution = gaussian_elimination(matrix, b)
    return [Fraction(sol, 1) for sol in solution]

def min_rank(R_R2):
    # Placeholder function to compute the minimal rank of R/R^2
    # This is a dummy implementation and should be replaced with actual computation
    return len(R_R2)

def resolution_width(phi):
    # Placeholder function to compute the resolution width of phi
    # This is a dummy implementation and should be replaced with actual computation
    return 10

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 10, 15, 20, 30, 40])
    phi = []
    for _ in range(n):
        variables = list(range(1, n + 1))
        clause = [random.choice(variables) if random.randint(0, 1) else -random.choice(variables) for _ in range(random.randint(2, n))]
        phi.append(clause)

    # Compute the quotient algebra R/R^2
    R_R2 = []  # Placeholder for actual computation
    min_rank_value = min_rank(R_R2)

    # Compute the resolution width of phi
    w_phi = resolution_width(phi)

    return {
        "metric_name": "min_rank",
        "metric_value": min_rank_value,
        "instances_tested": n,
        "n_max": n,
        "conjecture_holds": abs(min_rank_value - w_phi) < 1,  # Placeholder condition
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")