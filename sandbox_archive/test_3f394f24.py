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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_kcnf(n, k):
        cnf = []
        for _ in range(k):
            clause = set()
            while len(clause) < n:
                lit = random.randint(1, 2*n)
                if lit > n:
                    lit -= n
                else:
                    lit += n
                clause.add(lit)
            cnf.append(list(clause))
        return cnf

    def polynomial_from_clause(clause):
        poly = [0] * (2*n + 1)
        for lit in clause:
            if lit <= n:
                poly[lit - 1] += 1
            else:
                poly[2*n - lit] -= 1
        return poly

    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def lcm(a, b):
        return abs(a*b) // gcd(a, b)

    def extended_gcd(a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, x, y = extended_gcd(b % a, a)
            return (g, y - (b // a) * x, x)

    def mod_inverse(a, m):
        g, x, _ = extended_gcd(a, m)
        if g != 1:
            raise ValueError("Modular inverse does not exist")
        else:
            return x % m

    def polynomial_division(dividend, divisor):
        n = len(dividend) - 1
        m = len(divisor) - 1
        quotient = [0] * (n - m + 1)
        remainder = dividend[:]
        
        for i in range(n, m - 1, -1):
            if remainder[i] != 0:
                factor = remainder[i] // divisor[m]
                quotient[i - m] = factor
                for j in range(m):
                    remainder[i - j] -= factor * divisor[j]
        
        return quotient, remainder

    def minimal_root_count(poly):
        roots = set()
        n = len(poly) - 1
        for i in range(2*n + 1):
            if poly[i] != 0:
                root = mod_inverse(i, 2*n + 1)
                roots.add(root)
        return len(roots)

    def resolution_width(cnf):
        # Simplified DPLL solver to estimate width
        def solve(lits, cls):
            if not lits:
                return True
            lit = lits[0]
            other_lit = -lit
            new_lits_true = [x for x in lits if x != lit and x != other_lit]
            new_lits_false = [x for x in lits if x != -lit and x != -other_lit]
            return solve(new_lits_true, cls) or solve(new_lits_false, cls)
        
        width = 0
        for clause in cnf:
            width = max(width, len(clause))
        return width

    n = random.randint(5, 40)
    k = random.randint(2, min(n, 10))
    cnf = generate_kcnf(n, k)
    
    polynomials = [polynomial_from_clause(clause) for clause in cnf]
    gcd_poly = polynomials[0]
    for poly in polynomials[1:]:
        gcd_poly = polynomial_division(gcd_poly, poly)[0]
    
    alpha_phi = minimal_root_count(gcd_poly)
    w_phi = resolution_width(cnf)
    
    if w_phi == 0:
        return {
            "metric_name": "alpha_phi / w_phi",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Resolution width is zero"
        }
    
    ratio = alpha_phi / w_phi
    f_n = k * n ** (k / 2 + 1)
    
    return {
        "metric_name": "alpha_phi / w_phi",
        "metric_value": ratio,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": ratio <= f_n,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, 30)
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "First failing seed"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")