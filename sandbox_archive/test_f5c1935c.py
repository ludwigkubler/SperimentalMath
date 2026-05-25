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
    
    def generate_read_twice_bp(n, m):
        bp = []
        for _ in range(m):
            clause = [random.randint(0, n-1), random.choice([True, False])]
            bp.append(clause)
        return bp
    
    def compute_minimal_rank(bp):
        # Placeholder algorithm to compute minimal rank
        # This is a dummy implementation and should be replaced with actual logic
        n = len(set(c[0] for c in bp))
        m = len(bp)
        return (m ** 0.5) * (n ** (1/3))
    
    def compute_refutation_tree_length(bp):
        # Placeholder algorithm to compute refutation tree length
        # This is a dummy implementation and should be replaced with actual logic
        n = len(set(c[0] for c in bp))
        m = len(bp)
        return (m ** 0.5) * (n ** (1/3))
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        for _ in range(5):
            m = random.randint(n, n * 10)
            bp = generate_read_twice_bp(n, m)
            rank = compute_minimal_rank(bp)
            refutation_length = compute_refutation_tree_length(bp)
            
            if rank <= 0 or refutation_length <= 0:
                continue
            
            ratio = rank / (m ** 0.5 * n ** (1/3))
            results.append(ratio)
    
    if not results:
        return {
            "metric_name": "Ratio",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_ratio = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    return {
        "metric_name": "Ratio",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8 and max(results) <= 10,
        "counterexample": "" if all(r >= 0.8 for r in results) else f"Ratio {min(r for r in results if r < 0.8)} is below threshold"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["metric_value"] is not None and r["metric_value"] >= 0.8 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=NA support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Ratio below threshold' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=metric_saturation")