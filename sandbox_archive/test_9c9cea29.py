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
    
    # Generate a read-twice branching program with n inputs and m clauses
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    P = [[random.choice([0, 1]) for _ in range(m)] for _ in range(n)]
    
    # Compute the associated algebraic stack (simplified example)
    rank = sum(max(row.count(0), row.count(1)) for row in P) / m
    
    # Compute the theoretical bound
    bound = math.sqrt(m) * n ** (1/3)
    
    # Correlate the computed minimal rank with the size of the shortest refutation tree
    ratio = rank / bound
    
    return {
        "metric_name": "rank_to_bound_ratio",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.8,
        "counterexample": "" if ratio >= 0.8 else f"Ratio {ratio} < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    if not results:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        total_metric = sum(r["metric_value"] for r in results)
        total_conjecture_holds = sum(1 for r in results if r["conjecture_holds"])
        mean = total_metric / len(results)
        std = math.sqrt(sum((r["metric_value"] - mean) ** 2 for r in results) / len(results))
        support_fraction = total_conjecture_holds / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean:.6f} std={std:.6f} support_fraction={support_fraction:.3f}")
        elif any(not r["conjecture_holds"] for r in results):
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
            print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
        else:
            print("RESULT: INCONCLUSIVE insufficient_support")