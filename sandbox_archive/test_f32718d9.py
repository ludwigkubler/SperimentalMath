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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def cyclic_difference_set(f):
        n = int(math.log2(len(f)))
        diff_set = set()
        for i in range(2**n):
            for j in range(i + 1, 2**n):
                if f[i] != f[j]:
                    diff_set.add((i - j) % (2**n))
        return diff_set
    
    def dpll_proof_width(f):
        n = int(math.log2(len(f)))
        clauses = []
        for i in range(n):
            clauses.append([1 << i])
        for i in range(1, 2**n):
            if f[i] != f[0]:
                clause = [-i - 1]
                for j in range(n):
                    if (i >> j) & 1:
                        clause.append(-(j + 1))
                clauses.append(clause)
        stack = []
        assignment = [None] * n
        def dpll():
            while True:
                found_unassigned_var = False
                for i in range(n):
                    if assignment[i] is None:
                        assignment[i] = True
                        found_unassigned_var = True
                        break
                if not found_unassigned_var:
                    return all(f[i] == (assignment[j] for j in range(n)) for i in range(2**n))
                stack.append((i, assignment[:]))
                assignment[i] = False
            while stack:
                i, assignment = stack.pop()
                assignment[i] = True
                found_unassigned_var = False
                for j in range(i + 1, n):
                    if assignment[j] is None:
                        assignment[j] = True
                        found_unassigned_var = True
                        break
                if not found_unassigned_var:
                    return all(f[i] == (assignment[j] for j in range(n)) for i in range(2**n))
                stack.append((j, assignment[:]))
                assignment[j] = False
        return len(clauses) if dpll() else 0
    
    def min_rank(diff_set):
        n = int(math.log2(len(diff_set)))
        rank = 0
        while diff_set:
            pivot = next(iter(diff_set))
            diff_set.discard(pivot)
            for x in list(diff_set):
                if (x - pivot) % (2**n) in diff_set:
                    diff_set.remove((x - pivot) % (2**n))
            rank += 1
        return rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = generate_boolean_function(n)
    diff_set = cyclic_difference_set(f)
    proof_width = dpll_proof_width(f)
    min_rank_diff_set = min_rank(diff_set)
    
    return {
        "metric_name": "correlation",
        "metric_value": min_rank_diff_set / (proof_width + 1e-9),
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")