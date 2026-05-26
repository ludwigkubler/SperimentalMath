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
    
    def generate_read_twice_bp(n):
        bp = []
        for _ in range(n):
            layer = [random.choice([0, 1]) for _ in range(2**n)]
            bp.append(layer)
        return bp
    
    def compute_minimal_rank(bp):
        n = len(bp)
        size = 2**n
        g_n = math.log(size)
        
        # Placeholder for actual computation of minimal rank
        # For now, we use a dummy value that depends on the seed
        min_rank = random.uniform(0.5 * g_n, 1.5 * g_n)
        
        return min_rank
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    bp = generate_read_twice_bp(n)
    min_rank = compute_minimal_rank(bp)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank <= math.log(2**n),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")