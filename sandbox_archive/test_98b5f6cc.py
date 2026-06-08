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

def generate_random_cnf(n, m):
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(abs(c) != abs(clause[0]) for c in clause[1:]):
            clauses.append(clause)
    return clauses

def dpll_solve(cnf):
    def solve(assignment, literals):
        if not literals:
            return True
        literal = literals[0]
        pos_var = abs(literal)
        neg_var = -pos_var
        if pos_var in assignment and assignment[pos_var] != (literal > 0):
            return False
        if neg_var in assignment and assignment[neg_var] != (literal < 0):
            return False
        assignment[pos_var] = literal > 0
        if solve(assignment, literals[1:]):
            return True
        del assignment[pos_var]
        assignment[neg_var] = literal < 0
        if solve(assignment, literals[1:]):
            return True
        del assignment[neg_var]
        return False
    
    assignment = {}
    literals = [i for i in range(1, n + 1)] + [-i for i in range(1, n + 1)]
    return solve(assignment, literals)

def construct_formal_context(cnf):
    minterms = set()
    non_minterms = set()
    for clause in cnf:
        minterm = tuple(sorted(clause))
        if all(abs(lit) in minterm for lit in clause):
            minterms.add(minterm)
        else:
            non_minterms.add(minterm)
    universe = sorted(minterms | non_minterms)
    relation = [[0] * len(universe) for _ in range(len(universe))]
    for i, x in enumerate(universe):
        for j, y in enumerate(universe):
            if all(lit in x and lit in y or -lit not in x and -lit not in y for lit in cnf):
                relation[i][j] = 1
    return universe, relation

def min_rank(relation):
    n = len(relation)
    rank = 0
    for i in range(n):
        if any(relation[j][i] == 1 for j in range(i)):
            continue
        rank += 1
        for j in range(n):
            if relation[i][j] == 1:
                relation[j] = [x ^ y for x, y in zip(relation[j], relation[i])]
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            cnf = generate_random_cnf(n, n * (n - 1) // 2)
            width = dpll_solve(cnf)
            if width is None:
                continue
            universe, relation = construct_formal_context(cnf)
            rank = min_rank(relation)
            results.append({"width": width, "rank": rank})
    
    if not results:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_width = sum(r["width"] for r in results) / len(results)
    mean_rank = sum(r["rank"] for r in results) / len(results)
    variance_width = sum((r["width"] - mean_width) ** 2 for r in results) / len(results)
    variance_rank = sum((r["rank"] - mean_rank) ** 2 for r in results) / len(results)
    std_dev_width = math.sqrt(variance_width)
    std_dev_rank = math.sqrt(variance_rank)
    
    if std_dev_width == 0 or std_dev_rank == 0:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": 0,
            "instances_tested": len(results),
            "n_max": 40,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = sum((r["width"] - mean_width) * (r["rank"] - mean_rank) for r in results) / (len(results) * std_dev_width * std_dev_rank)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": 40,
        "conjecture_holds": abs(correlation_coefficient) > 0.9 and all(abs(r["rank"] - math.log(r["width"])) <= 5 for r in results),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")