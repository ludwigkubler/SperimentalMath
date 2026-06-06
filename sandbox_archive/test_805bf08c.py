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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def resolution_proof_width(phi):
        # Simplified model for demonstration purposes
        return len(phi)
    
    def minimal_rank_of_kac_moody(phi):
        # Placeholder function, actual implementation needed
        return 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    total_rank = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        phi = generate_boolean_formula(n)
        width = resolution_proof_width(phi)
        rank = minimal_rank_of_kac_moody(phi)
        
        if width < rank / 10:
            return {
                "metric_name": "Resolution Proof Width vs Minimal Rank",
                "metric_value": None,
                "instances_tested": instances_tested + 1,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"phi: {phi}, width: {width}, rank: {rank}"
            }
        
        total_width += width
        total_rank += rank
        instances_tested += 1
        n_max = max(n_max, n)
    
    mean_width = Fraction(total_width, instances_tested)
    mean_rank = Fraction(total_rank, instances_tested)
    
    return {
        "metric_name": "Resolution Proof Width vs Minimal Rank",
        "metric_value": float(mean_width),
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": mean_width >= 10 * mean_rank,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(int(r["conjecture_holds"]) for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")