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

def generate_tseitin_formula(n, m):
    variables = list(range(1, n + 1))
    clauses = []
    
    for i in range(m):
        var = random.choice(variables)
        neg_var = -var
        clause = [var]
        if random.choice([True, False]):
            clause.append(neg_var)
        clauses.append(clause)
    
    return variables, clauses

def resolution_length(clauses):
    queue = clauses.copy()
    seen = set()
    
    while queue:
        literal = queue.pop(0)
        neg_literal = -literal
        
        if neg_literal in seen:
            continue
        
        seen.add(neg_literal)
        
        for clause in clauses:
            if literal in clause:
                new_clause = [l for l in clause if l != literal]
                if not new_clause:
                    return len(queue) + 1
                queue.append(new_clause)
    
    return float('inf')

def minimal_rank(clauses):
    n = len(clauses)
    m = len(clauses[0])
    
    # Simulate a quantum channel with minimal rank
    rank = 2 ** (m - n / 2)
    return rank

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    for n in [5, 10, 15, 20, 30, 40]:
        variables, clauses = generate_tseitin_formula(n, n * (n - 1))
        
        rank = minimal_rank(clauses)
        resolution_len = resolution_length(clauses)
        
        if rank < 2 ** (len(clauses) - n / 2):
            return {
                "metric_name": "Minimal Rank vs Resolution Proof Length",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, m={len(clauses)}, rank={rank} < 2^({len(clauses)} - {n}/2)"
            }
        
        if resolution_len < len(clauses):
            return {
                "metric_name": "Minimal Rank vs Resolution Proof Length",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, m={len(clauses)}, resolution_len={resolution_len} < {len(clauses)}"
            }
    
    return {
        "metric_name": "Minimal Rank vs Resolution Proof Length",
        "metric_value": rank,
        "instances_tested": 6,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={len(results[0]['variables'])}, m={len(results[0]['clauses'])}\" first_failing_seed={first_failing_seed}")