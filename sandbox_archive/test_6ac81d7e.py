# auto-injected by SEC sandbox
import math
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
import itertools

def generate_cnf(n, k):
    clauses = []
    for _ in range(k):
        clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
        if all(clause[i] != -clause[j] for i, j in itertools.combinations(range(len(clause)), 2)):
            clauses.append(clause)
    return clauses

def resolution_length(cnf):
    queue = cnf[:]
    while True:
        new_clause = None
        for clause1 in queue:
            for clause2 in queue:
                if len(set(clause1) & set(clause2)) == 1:
                    new_clause = [x for x in clause1 + clause2 if x not in set(clause1) & set(clause2)]
                    break
            if new_clause is not None:
                break
        if new_clause is None:
            return len(queue)
        if new_clause in queue:
            return len(queue)
        queue.append(new_clause)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    k = random.randint(n // 2, n)
    cnf = generate_cnf(n, k)
    
    rank = len(cnf)  # Simplified minimal rank for this example
    proof_length = resolution_length(cnf)
    
    metric_value = proof_length / (rank ** 2) if rank != 0 else float('inf')
    conjecture_holds = metric_value <= 2
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} exceeds quadratic bound for rank {rank}"
    
    return {
        "metric_name": "Proof Length / Rank^2",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["metric_value"] > 2 for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["metric_value"] > 2)
        print(f"RESULT: FALSIFIED counterexample=\"Proof length exceeds quadratic bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")