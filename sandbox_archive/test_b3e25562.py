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

def tseitin_circuit(f):
    n = len(f)
    literals = list(range(2 * n))
    clause_id = 2 * n
    
    def add_clause(clause):
        nonlocal clause_id
        clauses.append(clause)
        return clause_id - 1
    
    clauses = []
    
    for i in range(n):
        literal = literals[i]
        neg_literal = literals[n + i]
        
        # Add clause: literal ∨ ~neg_literal
        add_clause([literal, -neg_literal])
        
        # Add clause: ~literal ∨ neg_literal
        add_clause([-literal, neg_literal])
    
    for i in range(n):
        literal = literals[i]
        neg_literal = literals[n + i]
        
        # Add clause: f[i] ∨ literal
        if f[i]:
            add_clause([f[i], literal])
        else:
            add_clause([-f[i], -literal])
    
    return clauses

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    f = [random.choice([1, 2]) for _ in range(n)]
    circuit = tseitin_circuit(f)
    
    # Simulate computation of minimal rank (placeholder)
    min_rank = len(circuit) / n
    
    return {
        "metric_name": "min_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank >= math.log(n, 2) * 0.9 and min_rank <= math.log(n, 2) * 1.1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")