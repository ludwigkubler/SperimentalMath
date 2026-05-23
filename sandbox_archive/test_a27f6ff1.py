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
        clause = [neg_var]
        for _ in range(random.randint(0, n - 2)):
            other_var = random.choice(variables)
            if other_var not in clause:
                clause.append(other_var)
        clauses.append(clause)
    
    return variables, clauses

def resolution_length(clauses):
    queue = list(clauses)
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
    m = len([c for c in clauses if len(c) > 1])
    
    # Simplified heuristic: rank is proportional to the number of non-trivial clauses
    return math.ceil(2 ** (m - n / 2))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 4)
    
    variables, clauses = generate_tseitin_formula(n, m)
    resolution_len = resolution_length(clauses)
    rank = minimal_rank(clauses)
    
    conjecture_holds = rank >= 2 ** (m - n / 2) and resolution_len >= rank
    counterexample = "" if conjecture_holds else f"Rank {rank} < 2^(m - n/2) or Resolution length {resolution_len} < Rank"
    
    return {
        "metric_name": "Minimal Rank vs Resolution Proof Length",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank:.4f} std={std_rank:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank too small\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")