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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def is_quadratic_residue(n, p):
    if n == 0 or n == 1:
        return True
    if n < 0 or p <= 0:
        return False
    n %= p
    if gcd(n, p) != 1:
        return False
    for i in range(2, int(math.sqrt(p)) + 1):
        if (i * i % p == n):
            return True
    return False

def quadratic_residues_in_ap(a, d, n):
    residues = set()
    for i in range(n):
        residues.add((a + i * d) % n)
    return len(residues)

def generate_tseitin_formula(n):
    variables = [f'x{i}' for i in range(1, n+1)]
    clauses = []
    for var in variables:
        clauses.append([var])
        clauses.append(['~', var])
    for i in range(1, n):
        for j in range(i+1, n+1):
            clauses.append([f'x{i}', f'x{j}'])
            clauses.append(['~', f'x{i}', '~', f'x{j}'])
    return variables, clauses

def resolution_width(clauses):
    queue = list(clauses)
    assignment = {}
    while queue:
        clause = queue.pop(0)
        if not any(var in assignment for var in clause):
            continue
        unit_clause = [var for var in clause if var[1:] not in assignment or assignment[var[1:]] != var[0]]
        if len(unit_clause) == 1:
            var = unit_clause[0]
            value = '~' + var[1:] if var[0] == 'x' else var[1:]
            for c in clauses:
                if any(var in c and (assignment[var[1:]] == var[0] or assignment[var[1:]] == '~' + var[0]) for var in c):
                    queue.remove(c)
                    new_clause = [v for v in c if v != var]
                    if not any(v in assignment for v in new_clause):
                        queue.append(new_clause)
            assignment[var[1:]] = value
        else:
            return len(assignment)
    return len(assignment)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    total_widths = []
    max_n = 0
    conjecture_holds = True
    counterexample = ""

    for n in n_values:
        variables, clauses = generate_tseitin_formula(n)
        width = resolution_width(clauses)
        total_widths.append(width)
        max_n = max(max_n, n)

        qr_count = quadratic_residues_in_ap(0, 1, n)
        if width > qr_count + 3:
            conjecture_holds = False
            counterexample = f"n={n}, width={width}, QR count={qr_count}"

    return {
        "metric_name": "resolution_width",
        "metric_value": sum(total_widths) / len(total_widths),
        "instances_tested": 6,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []

    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")

    mean_width = sum(result["metric_value"] for result in results) / len(results)
    std_width = math.sqrt(sum((result["metric_value"] - mean_width) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_width} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")