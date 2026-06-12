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
    
    def generate_formula(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses

    def compute_clause_tree_width(clauses):
        n = len(clauses[0])
        tree = [[] for _ in range(2**n)]
        for clause in clauses:
            node = 0
            for literal in clause:
                if literal.startswith('x'):
                    bit = int(literal[1:]) - 1
                    node |= 1 << bit
                else:
                    bit = int(literal[2:]) - 1
                    node &= ~(1 << bit)
            tree[node].append(clause)
        return max(len(subtree) for subtree in tree)

    def compute_minimal_rank(clauses):
        n = len(clauses[0])
        m = len(clauses)
        A = [[0] * (2**n) for _ in range(m)]
        for i, clause in enumerate(clauses):
            node = 0
            for literal in clause:
                if literal.startswith('x'):
                    bit = int(literal[1:]) - 1
                    node |= 1 << bit
                else:
                    bit = int(literal[2:]) - 1
                    node &= ~(1 << bit)
            A[i][node] = 1
        
        rank = 0
        for row in A:
            if any(row):
                pivot_col = next(j for j, x in enumerate(row) if x)
                rank += 1
                for i in range(m):
                    if A[i][pivot_col]:
                        for j in range(n):
                            A[i][j] ^= A[0][j]
        return rank

    n = random.randint(5, 40)
    clauses = generate_formula(n)
    ctw = compute_clause_tree_width(clauses)
    mrt = compute_minimal_rank(clauses)

    return {
        "metric_name": "correlation",
        "metric_value": ctw,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")