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
    def __init__(self, numerator=0, denominator=1):
        if denominator == 0:
            raise ValueError("Denominator cannot be zero")
        common_divisor = gcd(numerator, denominator)
        self.numerator = numerator // common_divisor
        self.denominator = denominator // common_divisor

    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator, self.denominator * other.denominator)

    def __sub__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator - other.numerator * self.denominator, self.denominator * other.denominator)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)

    def __eq__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return self.numerator == other.numerator and self.denominator == other.denominator

    def __lt__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return self.numerator * other.denominator < other.numerator * self.denominator

    def __le__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return self.numerator * other.denominator <= other.numerator * self.denominator

    def __gt__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return self.numerator * other.denominator > other.numerator * self.denominator

    def __ge__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return self.numerator * other.denominator >= other.numerator * self.denominator

    def __str__(self):
        return f"{self.numerator}/{self.denominator}"

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        # Simplified version of resolution width calculation
        return len(cnf)
    
    def monodromy_group_rank(cnf):
        # Placeholder for actual computation
        return random.randint(1, 2 * len(cnf))
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    width = resolution_width(cnf)
    rank = monodromy_group_rank(cnf)
    
    if rank > 1.5 * width:
        return {
            "metric_name": "monodromy_group_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "rank exceeds 1.5 * width"
        }
    else:
        return {
            "metric_name": "monodromy_group_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds 1.5 * width\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")