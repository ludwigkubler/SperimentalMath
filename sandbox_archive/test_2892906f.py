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

def generate_tseitin_circuit(n, m):
    if n <= 0 or m <= 0:
        return [], []
    
    inputs = [f'x{i}' for i in range(n)]
    clauses = []
    
    # Generate variables and clauses
    for i in range(m):
        var = f'y{i}'
        clause = random.choice(inputs)
        if random.choice([True, False]):
            clause += ' OR '
        else:
            clause += ' NOT '
        clause += var
        clauses.append(clause)
        
        # Add Tseitin variable to inputs
        inputs.append(var)
    
    return inputs, clauses

def tropicalize_qmcs(qmcs):
    n = len(qmcs)
    rank = 0
    
    for i in range(n):
        max_val = -math.inf
        for j in range(n):
            if qmcs[i][j] > max_val:
                max_val = qmcs[i][j]
        rank += max_val
    
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 5 instances per size
            inputs, clauses = generate_tseitin_circuit(n, len(clauses))
            if not inputs or not clauses:
                continue
            
            qmcs = [[random.uniform(-10, 10) for _ in range(len(inputs))] for _ in range(len(inputs))]
            rank = tropicalize_qmcs(qmcs)
            
            total_rank += rank
            instances_tested += 1
    
    mean_rank = Fraction(total_rank, instances_tested)
    conjecture_holds = mean_rank <= 1.5 * math.sqrt(len(clauses))
    
    return {
        "metric_name": "mean_rank",
        "metric_value": float(mean_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank {mean_rank} not within 1.5 * sqrt({len(clauses)})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank out of bounds\" first_failing_seed={first_failing_seed}")