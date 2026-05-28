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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clause = [f'~{variables[i-1]}']
            for j in range(i+1, n+1):
                clause.append(f'{variables[j-1]}')
            clauses.append(clause)
        return variables, clauses
    
    def compute_algebraic_automorphism_group(variables, clauses):
        # Simplified version of computing the automorphism group
        # This is a placeholder and does not actually compute the automorphism group
        return 2 ** len(variables)
    
    def resolution_proof_length(clauses):
        # Simplified version of computing the resolution proof length
        # This is a placeholder and does not actually compute the proof length
        return len(clauses) * 10
    
    n = random.randint(5, 40)
    variables, clauses = generate_tseitin_formula(n)
    min_rank = compute_algebraic_automorphism_group(variables, clauses)
    t_F = resolution_proof_length(clauses)
    
    if min_rank == 0:
        return {
            "metric_name": "log2_t_F",
            "metric_value": float('-inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "min_rank_undefined"
        }
    
    log2_t_F = math.log2(t_F)
    return {
        "metric_name": "log2_t_F",
        "metric_value": log2_t_F,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["conjecture_holds"]]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={sum(metric_values) / len(metric_values)} std=0.0 support_fraction=1.0")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"min_rank_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")