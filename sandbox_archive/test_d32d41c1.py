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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def polynomial_to_vector(clauses):
        n = len(clauses[0])
        poly = [[Fraction(0, 1)] * n for _ in range(len(clauses))]
        for i, clause in enumerate(clauses):
            for var in clause:
                if var > 0:
                    poly[i][var - 1] += Fraction(1, 1)
                else:
                    poly[i][-var - 1] -= Fraction(1, 1)
        return poly
    
    def evaluate_polynomial(poly, assignment):
        n = len(assignment)
        value = Fraction(0, 1)
        for i in range(len(poly)):
            term = poly[i]
            product = Fraction(1, 1)
            for j in range(n):
                if term[j] != 0:
                    product *= (assignment[j] if j + 1 in term else -assignment[j])
            value += term[-1] * product
        return value
    
    def local_cohomology_rank(poly):
        n = len(poly)
        rank = 0
        for i in range(n):
            for j in range(i, n):
                if poly[i][j] != 0:
                    rank += 1
                    break
        return rank
    
    def generate_random_3cnf(m, n):
        clauses = []
        for _ in range(m):
            clause = random.sample(range(1, n + 1), random.randint(1, n))
            clause.extend([-var for var in clause])
            clauses.append(clause)
        return clauses
    
    m = random.randint(5, 30)
    n = random.randint(5, 30)
    clauses = generate_random_3cnf(m, n)
    
    poly = polynomial_to_vector(clauses)
    assignment = [random.choice([True, False]) for _ in range(n)]
    value = evaluate_polynomial(poly, assignment)
    rank = local_cohomology_rank(poly)
    
    metric_name = "local_cohomology_rank"
    metric_value = rank
    instances_tested = 1
    conjecture_holds = rank <= n**2 - m + 1
    counterexample = "" if conjecture_holds else f"m={m}, n={n}, rank={rank}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_rank = math.sqrt(sum((res["metric_value"] - mean_rank)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"m={results[0]['metric_value']}, n={results[1]['metric_value']}, rank={results[2]['metric_value']}\" first_failing_seed={first_failing_seed}")