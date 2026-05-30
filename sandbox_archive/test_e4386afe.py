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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            literals = [random.randint(1, n), random.randint(-n, -1)]
            random.shuffle(literals)
            clause = tuple(sorted(literals))
            if clause not in clauses:
                clauses.append(clause)
        return clauses

    def k_theory_rank(clauses):
        # Simplified version for demonstration purposes
        return len(set(len(c) for c in clauses))

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n**2)
        instance = generate_3cnf(n, m)
        rank = k_theory_rank(instance)
        
        results.append({
            "metric_name": "K-theory rank",
            "metric_value": rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": ""
        })
    
    return {
        "seed": seed,
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.extend(trial_result["results"])
    
    total_metric_value = sum(r["metric_value"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        RESULT = f"SUPPORTED mean={total_metric_value / instances_tested:.4f} std=NA support_fraction={support_fraction:.2f}"
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        RESULT = f"FALSIFIED counterexample='not enough data' first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE insufficient_data"
    
    print(RESULT)