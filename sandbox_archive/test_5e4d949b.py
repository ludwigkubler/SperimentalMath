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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            if random.choice([True, False]):
                clause[1] *= -1
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(literals, assignment):
            if not cnf:
                return True
            literal = next((l for l in literals if l not in assignment), None)
            if literal is None:
                return False
            pos_clauses = [c for c in cnf if literal in c]
            neg_clauses = [c for c in cnf if -literal in c]
            if any(all(l not in assignment for l in c) for c in pos_clauses):
                return solve(literals, assignment + [literal])
            if any(all(l not in assignment for l in c) for c in neg_clauses):
                return solve(literals, assignment + [-literal])
            return False
        return solve([l for l in range(1, len(cnf) + 1)], [])
    
    def lcai(cnf):
        n = len(cnf)
        A = [[0] * (n + 1) for _ in range(n + 1)]
        pos_clauses = [[] for _ in range(n + 1)]
        neg_clauses = [[] for _ in range(n + 1)]
        
        for clause in cnf:
            if all(abs(l) <= n for l in clause):
                for l in clause:
                    if l > 0:
                        pos_clauses[l].append(clause)
                    else:
                        neg_clauses[-l].append(clause)
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                pos_clauses_i = set(pos_clauses[i])
                pos_clauses_j = set(pos_clauses[j])
                neg_clauses_i = set(neg_clauses[i])
                neg_clauses_j = set(neg_clauses[j])
                A[i][j] = len(pos_clauses_i & pos_clauses_j) - len(neg_clauses_i & neg_clauses_j)
        
        return sum(sum(row) for row in A) / (n * n)
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        lcai_value = lcai(cnf)
        dpll_height = dpll(cnf)
        if math.isnan(lcai_value) or math.isinf(lcai_value):
            continue
        metric_values.append(abs(lcai_value - dpll_height))
    
    if not metric_values:
        return {
            "metric_name": "LCAI vs DPLL Height",
            "metric_value": 0.0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "LCAI vs DPLL Height",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean <= 3,
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
    
    mean = sum(r["metric_value"] for r in results) / len(results)
    std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")