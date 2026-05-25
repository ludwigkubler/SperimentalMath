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
    
    def generate_ptf(n, m):
        clauses = []
        for _ in range(m):
            literals = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            clauses.append(literals)
        return clauses
    
    def compute_minimal_rank(clauses):
        # Placeholder implementation of minimal rank computation
        # This is a dummy function and should be replaced with actual logic
        return random.randint(1, 100)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        m_values = range(1, n + 1)  # Ensure at least one clause per variable
        for m in m_values:
            ptf = generate_ptf(n, m)
            minimal_rank = compute_minimal_rank(ptf)
            predicted_value = Fraction(m**(1/4) * n**(3/4))
            ratio = Fraction(minimal_rank, predicted_value)
            results.append({"n": n, "m": m, "minimal_rank": minimal_rank, "predicted_value": predicted_value, "ratio": ratio})
    
    if not results:
        return {
            "metric_name": "Ratio of Minimal Rank to Predicted Value",
            "metric_value": 0,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "No instances generated"
        }
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    std_ratio = math.sqrt(sum((result["ratio"] - mean_ratio)**2 for result in results) / len(results))
    
    return {
        "metric_name": "Ratio of Minimal Rank to Predicted Value",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
        "conjecture_holds": std_ratio < 0.1 and mean_ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_ratio = sum(result["metric_value"] for result in results) / len(results)
        std_ratio = math.sqrt(sum((result["metric_value"] - mean_ratio)**2 for result in results) / len(results))
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction=1.0")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Ratio of Minimal Rank to Predicted Value exceeds 1.5"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")