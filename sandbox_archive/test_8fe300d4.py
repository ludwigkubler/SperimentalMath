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

def generate_k_cnf(n, q):
    clauses = []
    for _ in range(q):
        literals = set()
        while len(literals) < 2:
            literal = random.randint(1, n)
            if random.choice([True, False]):
                literal = -literal
            literals.add(literal)
        clause = tuple(sorted(literals))
        clauses.append(clause)
    return clauses

def construct_matrix(clauses, q):
    n = len(clauses[0])
    matrix = [[Fraction(0) for _ in range(n + 1)] for _ in range(q)]
    for i, clause in enumerate(clauses):
        for literal in clause:
            if literal > 0:
                matrix[i][literal - 1] += Fraction(1)
            else:
                matrix[i][-literal] -= Fraction(1)
    return matrix

def min_rank(matrix):
    n = len(matrix[0])
    rank = 0
    for row in matrix:
        if any(row[j] != Fraction(0) for j in range(n)):
            rank += 1
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    q_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for q in q_values:
        n = q * 2
        clauses = generate_k_cnf(n, q)
        matrix = construct_matrix(clauses, q)
        rank = min_rank(matrix)
        
        metric_value = rank / (q ** (1/3) * (n ** (2/3)))
        instances_tested = len(clauses)
        conjecture_holds = metric_value >= 1
        counterexample = "" if conjecture_holds else "rank_too_low"
        
        results.append({
            "metric_name": "minimal_rank",
            "metric_value": metric_value,
            "instances_tested": instances_tested,
            "conjecture_holds": conjecture_holds,
            "counterexample": counterexample
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.extend(result["results"])
    
    mean_value = sum(r["metric_value"] for r in all_results) / len(all_results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(1 for r in all_results if r["conjecture_holds"]) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in all_results):
        first_failing_seed = next(r["seed"] for r in all_results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rank_too_low' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")