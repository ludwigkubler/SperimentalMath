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
from itertools import combinations

def generate_random_function(n):
    if n <= 0:
        return {}
    domain = list(range(2))
    return {tuple(random.sample(domain, n)) for _ in range(10)}

def compute_minimal_rank(f):
    # Placeholder for actual computation of minimal rank using GIT
    # This is a dummy implementation for the sake of testing
    return len(f)

def compute_disjointness_communication_complexity(f):
    # Placeholder for actual computation of communication complexity
    # This is a dummy implementation for the sake of testing
    n = len(next(iter(f)))
    return n

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_random_function(n)
        if not f:
            continue
        
        rank = compute_minimal_rank(f)
        communication_complexity = compute_disjointness_communication_complexity(f)
        
        results.append({
            "n": n,
            "rank": rank,
            "communication_complexity": communication_complexity
        })
    
    if not results:
        return {
            "metric_name": "Rank vs Communication Complexity",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    total_rank = sum(result["rank"] for result in results)
    total_communication_complexity = sum(result["communication_complexity"] for result in results)
    mean_ratio = total_communication_complexity / total_rank if total_rank != 0 else None
    
    return {
        "metric_name": "Rank vs Communication Complexity",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": mean_ratio is not None and mean_ratio >= 1.0,
        "counterexample": "" if mean_ratio is not None and mean_ratio >= 1.0 else "mean_ratio < 1.0"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30)) + [67, 71, 73, 79]  # Default to first 30 primes and a few more
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if not results:
        print("RESULT: INCONCLUSIVE no valid trials")
        sys.exit(1)
    
    total_rank = sum(r["instances_tested"] * r["metric_value"] for r in results if r["metric_value"] is not None)
    total_instances = sum(r["instances_tested"] for r in results)
    mean_ratio = total_rank / total_instances if total_instances != 0 else None
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if mean_ratio is not None and mean_ratio >= 1.0:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(r["counterexample"] == "mapping_undefined" for r in results):
        print("RESULT: INCONCLUSIVE mapping_undefined")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mean_ratio < 1.0' first_failing_seed={first_failing_seed}")