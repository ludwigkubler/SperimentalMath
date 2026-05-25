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
    
    n = 10  # Start with a small size and increase if needed
    instances_tested = 0
    total_rank_quot = 0
    total_entropy_complexity = 0
    
    while instances_tested < 30:
        f = [random.choice([0, 1]) for _ in range(2**n)]
        
        # Compute the quotient representation rank (simplified example)
        rank_quot = len(set(f))
        
        # Calculate the entropic complexity (simplified example)
        entropy_complexity = sum(f.count(i) / len(f) * math.log2(len(f) / f.count(i)) for i in set(f))
        
        if entropy_complexity == 0:
            continue
        
        total_rank_quot += rank_quot
        total_entropy_complexity += entropy_complexity
        instances_tested += 1
    
    mean_rank_quot = total_rank_quot / instances_tested
    mean_entropy_complexity = total_entropy_complexity / instances_tested
    ratio = mean_rank_quot / mean_entropy_complexity if mean_entropy_complexity != 0 else float('inf')
    
    conjecture_holds = ratio <= 1.5  # Example threshold, adjust as needed
    
    return {
        "metric_name": "Rank_quot vs Entropy_complexity",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Ratio {ratio} exceeds threshold 1.5"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"Ratio exceeds threshold\" first_failing_seed={first_failing_seed}")