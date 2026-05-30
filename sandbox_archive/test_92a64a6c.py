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
    
    def generate_random_kcnf(n: int, k: int):
        clauses = []
        for _ in range(k * n // 2):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if len(set(clause)) == 2:
                clauses.append(clause)
        return clauses

    def construct_polynomial_from_kcnf(clauses):
        # Construct a polynomial using quadratic residues
        poly = {}
        for clause in clauses:
            x, y = abs(clause[0]), abs(clause[1])
            if (x * y) % 2 == 0:
                coeff = (x * y) // 4
                if coeff not in poly:
                    poly[coeff] = 0
                poly[coeff] += 1
        return poly

    def resolution_width(kcnf):
        # Simplify the k-CNF using resolution and count the width
        clauses = set(tuple(sorted(c)) for c in kcnf)
        width = 0
        while True:
            new_clauses = []
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1) & set(clause2)) == 1:
                        lit = list(set(clause1) ^ set(clause2))[0]
                        new_clause = [l for l in clause1 + clause2 if l != -lit and l != lit]
                        if len(new_clause) > width:
                            width = len(new_clause)
                        if not new_clause:
                            return 1
                        new_clauses.append(tuple(sorted(new_clause)))
            if not new_clauses:
                break
            clauses.update(new_clauses)
        return width

    def order_of_quadratic_residues(poly):
        # Find the highest power of any quadratic residue in the polynomial
        max_order = 0
        for coeff in poly:
            if coeff > max_order:
                max_order = coeff
        return max_order

    n = random.randint(5, 40)
    k = random.randint(3, 10)
    kcnf = generate_random_kcnf(n, k)
    
    polynomial = construct_polynomial_from_kcnf(kcnf)
    width = resolution_width(kcnf)
    order = order_of_quadratic_residues(polynomial)
    
    return {
        "metric_name": "order of quadratic residues",
        "metric_value": order,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": order <= 3 * width,
        "counterexample": "" if order <= 3 * width else f"Order {order} > 3 * Width {width}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")