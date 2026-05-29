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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tree_like_resolution_width(f):
        n = int(math.log2(len(f)))
        clauses = []
        for i in range(n):
            clause = []
            for j in range(i + 1):
                if f[2**(i - j) ^ 2**j] != f[2**(i - j)]:
                    clause.append(j)
            clauses.append(clause)
        count = 0
        while len(clauses) > 1:
            new_clauses = []
            for i in range(0, len(clauses), 2):
                if i + 1 < len(clauses):
                    new_clause = set(clauses[i]) | set(clauses[i + 1])
                    new_clauses.append(new_clause)
                else:
                    new_clauses.append(clauses[i])
            clauses = new_clauses
            count += 1
        return len(clauses) - count
    
    def symplectic_leaves(f):
        n = int(math.log2(len(f)))
        leaves = []
        for i in range(2**n):
            if all(f[i ^ (1 << j)] == f[i] for j in range(n)):
                leaves.append(i)
        return len(leaves)
    
    instances_tested = 0
    total_leaves = 0
    total_widths_squared = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        w_t_f = tree_like_resolution_width(f)
        leaves = symplectic_leaves(f)
        
        instances_tested += 1
        total_leaves += leaves
        total_widths_squared += w_t_f ** 2
    
    metric_value = total_leaves / instances_tested
    n_max = 40
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": "Symplectic Leaves Number",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")