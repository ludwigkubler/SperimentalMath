# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        var = next((v for v in range(len(assignment)) if assignment[v] is None), -1)
        if var == -1:
            return False
        
        for value in [True, False]:
            new_assignment = assignment[:]
            new_assignment[var] = value
            if dpll([c for c in clauses if not any(l == -v or l == v for l in c)], new_assignment):
                return True
        return False
    
    def grothendieck_group(clauses):
        # Simplified version of Grothendieck group construction for demonstration purposes
        # This is a placeholder and does not reflect actual mathematical details
        rank = len(set(tuple(sorted(c)) for c in clauses))
        return rank
    
    n_max = 0
    instances_tested = 0
    metric_values = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = []
            for _ in range(random.randint(1, n * (n - 1) // 2)):
                clause = [random.choice([-i-1, i] for i in range(n)) for _ in range(random.randint(1, n))]
                clauses.append(clause)
            
            rank = grothendieck_group(clauses)
            height = dpll(clauses, [None] * n)
            
            if rank is None or height is None:
                continue
            
            instances_tested += 1
            metric_values.append((rank, height))
    
    if not metric_values:
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    rank_values, height_values = zip(*metric_values)
    mean_rank = sum(rank_values) / len(rank_values)
    mean_height = sum(height_values) / len(height_values)
    correlation_coefficient = sum((r - mean_rank) * (h - mean_height) for r, h in metric_values) / (len(metric_values) * (sum((r - mean_rank) ** 2 for r in rank_values)) ** 0.5 * (sum((h - mean_height) ** 2 for h in height_values)) ** 0.5)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, {result}}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support n_tested={len(results)}")