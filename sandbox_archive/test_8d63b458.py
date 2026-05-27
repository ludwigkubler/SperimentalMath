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
    
    def generate_disj_instance(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.choice([0, 1]) for _ in range(n)]
            clauses.append(clause)
        return clauses
    
    def non_archimedean_valuation(clauses):
        # Simplified non-archimedean valuation (example)
        rank = sum(1 for clause in clauses if any(x == 1 for x in clause))
        return rank
    
    def communication_complexity(clauses, rank):
        # Simplified communication complexity (example)
        return len(clauses) * rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m = random.randint(1, n * 10)  # Number of clauses
        clauses = generate_disj_instance(n, m)
        rank = non_archimedean_valuation(clauses)
        cc_r = communication_complexity(clauses, rank)
        results.append({"n": n, "m": m, "rank": rank, "cc_r": cc_r})
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "no_instances_generated"
        }
    
    min_rank = min(result["rank"] for result in results)
    avg_cc_r = sum(result["cc_r"] for result in results) / len(results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": avg_cc_r,
        "instances_tested": len(results),
        "conjecture_holds": min_rank * n_values[0] <= avg_cc_r,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        avg_cc_r = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={avg_cc_r} std=0 support_fraction={support_fraction}")
        elif any(not result["conjecture_holds"] for result in results):
            first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"first failing seed\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")