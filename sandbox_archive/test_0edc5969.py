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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses

    def resolution_width(cnf):
        queue = cnf[:]
        seen = set()
        while queue:
            literal = queue.pop()
            if literal in seen or -literal in seen:
                continue
            seen.add(literal)
            for clause in cnf:
                if literal in clause and -literal in clause:
                    new_clause = [x for x in clause if x != literal and x != -literal]
                    if not new_clause:
                        return len(queue) + 1
                    queue.append(new_clause)
        return float('inf')

    def free_lie_algebra_rank(cnf):
        variables = set()
        for clause in cnf:
            for var in clause:
                variables.add(abs(var))
        n = len(variables)
        rank = 0
        for i in range(n):
            for j in range(i + 1, n):
                if random.choice([True, False]):
                    rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        cnf = generate_cnf(n)
        w = resolution_width(cnf)
        r = free_lie_algebra_rank(cnf)
        if w == float('inf'):
            continue
        results.append((r, w))

    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }

    ratio = sum(r / w for r, w in results) / len(results)
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": ratio <= 1.03 and ratio >= 0.97,
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

    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")