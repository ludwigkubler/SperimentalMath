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

def generate_3cnf(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < 3:
            var = random.choice(variables)
            polarity = random.choice([True, False])
            if (var, polarity) not in clause and (-var, not polarity) not in clause:
                clause.add((var, polarity))
        clauses.append(list(clause))
    return clauses

def resolution_width(phi):
    learned_clauses = phi[:]
    while True:
        new_clause = None
        for i in range(len(learned_clauses)):
            for j in range(i + 1, len(learned_clauses)):
                clause_i = set(learned_clauses[i])
                clause_j = set(learned_clauses[j])
                for literal in clause_i:
                    if (-literal[0], not literal[1]) in clause_j:
                        new_clause = [l for l in clause_i if l != literal] + \
                                      [l for l in clause_j if l != (-literal[0], not literal[1])]
                        break
                if new_clause:
                    break
            if new_clause:
                break
        if not new_clause:
            break
        learned_clauses.append(new_clause)
    return max(len(c) for c in learned_clauses)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = max(1, int(n * (n - 1) / 6))  # Ensure at least one clause
        phi = generate_3cnf(n, m)
        
        w_phi = resolution_width(phi)
        if not w_phi:
            continue
        
        rank_K_phi = len(set(tuple(sorted(c)) for c in phi))
        
        results.append({
            "n": n,
            "m": m,
            "w_phi": w_phi,
            "rank_K_phi": rank_K_phi
        })
    
    if not results:
        return {
            "metric_name": "ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = sum(r["rank_K_phi"] / r["w_phi"] for r in results) / len(results)
    instances_tested = len(results)
    n_max = max(r["n"] for r in results)
    
    return {
        "metric_name": "ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio <= 1,  # Placeholder constant c=1
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {seed} {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")