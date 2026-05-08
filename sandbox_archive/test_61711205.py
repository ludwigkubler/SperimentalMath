# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from itertools import combinations

def dpll(clauses, assignment={}):
    if not clauses:
        return True
    literal = next(l for l in range(1, len(assignment) + 2) if l not in assignment and -l not in assignment)
    positive_clauses = [c for c in clauses if literal in c]
    negative_clauses = [c for c in clauses if -literal in c]
    if dpll(positive_clauses, {**assignment, literal: True}):
        return True
    elif dpll(negative_clauses, {**assignment, literal: False}):
        return True
    else:
        return False

def build_clique_complex(clauses):
    n = max(abs(l) for l in set.union(*clauses))
    adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
    for clause in clauses:
        for i, j in combinations(sorted(abs(l) for l in clause), 2):
            adjacency_matrix[i][j] = 1
            adjacency_matrix[j][i] = 1
    return adjacency_matrix

def compute_persistent_homology_barcode_length(adjacency_matrix):
    n = len(adjacency_matrix)
    barcode_length = 0
    for i in range(1, n + 1):
        row_sum = sum(adjacency_matrix[i])
        if row_sum == i - 1:
            barcode_length += 1
    return barcode_length

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = []
    for _ in range(m):
        clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
        clauses.append(clause)
    
    adjacency_matrix = build_clique_complex(clauses)
    barcode_length = compute_persistent_homology_barcode_length(adjacency_matrix)
    dpll_tree_size = len(dpll(clauses))
    
    metric_value = abs(barcode_length * dpll_tree_size - 1)
    conjecture_holds = metric_value < 0.1
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "barcode_length_times_dpll_tree_size",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3**j + 5**k for i, j, k in product(range(5), range(5), range(5))]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")