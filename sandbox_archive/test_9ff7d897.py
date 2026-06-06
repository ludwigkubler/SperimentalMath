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

def gaussian_elimination(A):
    n = len(A)
    for i in range(n):
        if A[i][i] == 0:
            # Find a non-zero pivot below
            for j in range(i + 1, n):
                if A[j][i] != 0:
                    A[i], A[j] = A[j], A[i]
                    break
            else:
                raise ValueError("Matrix is singular")
        factor = Fraction(1, A[i][i])
        for k in range(n):
            A[i][k] *= factor
        for j in range(n):
            if j != i:
                factor = A[j][i]
                for k in range(n):
                    A[j][k] -= factor * A[i][k]
    return A

def fraction(a, b):
    gcd = math.gcd(a, b)
    return (a // gcd, b // gcd)

class Fraction:
    def __init__(self, numerator=0, denominator=1):
        if denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero")
        self.numerator, self.denominator = fraction(numerator, denominator)

    def __add__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator + other.numerator * self.denominator,
                        self.denominator * other.denominator)

    def __mul__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.numerator, self.denominator * other.denominator)

    def __truediv__(self, other):
        if isinstance(other, int):
            other = Fraction(other)
        return Fraction(self.numerator * other.denominator, self.denominator * other.numerator)

    def __repr__(self):
        return f"Fraction({self.numerator}, {self.denominator})"

def tseitin_formula(phi):
    # Construct Tseitin formula from CNF phi
    pass

def tropical_hodge_structure_rank(formula):
    # Compute minimal tropical Hodge structure rank of the formula
    pass

def dpll_proof_path_length(phi):
    # Run DPLL algorithm on phi and return proof path length
    pass

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = 10  # Start with a small size and increase
    instances_tested = 0
    h_phi_sum = 0
    l_phi_sum = 0
    n_max = 0
    conjecture_holds = True
    counterexample = ""

    for _ in range(30):
        phi = generate_random_cnf(n)
        tseitin_formula_ = tseitin_formula(phi)
        h_phi = tropical_hodge_structure_rank(tseitin_formula_)
        l_phi = dpll_proof_path_length(phi)

        if h_phi is None or l_phi is None:
            conjecture_holds = False
            counterexample = "Tropical Hodge Structure Rank or Proof Path Length computation failed"
            break

        h_phi_sum += h_phi
        l_phi_sum += l_phi
        instances_tested += 1
        n_max = max(n_max, n)

    if instances_tested < 30:
        conjecture_holds = False
        counterexample = "Insufficient instances tested"

    mean_h_phi = h_phi_sum / instances_tested
    mean_l_phi = l_phi_sum / instances_tested

    return {
        "metric_name": "Tropical Hodge Structure Rank vs DPLL Proof Path Length",
        "metric_value": mean_h_phi,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

def generate_random_cnf(n):
    # Generate a random CNF with n variables
    pass

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_h_phi = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_h_phi} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")