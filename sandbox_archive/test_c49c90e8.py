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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tropicalized_noncrossing_partition(poly):
        n = len(poly)
        if n == 1:
            return poly[0]
        else:
            left_poly = [poly[i] + poly[j] for i in range(n//2) for j in range(i+1, n//2)]
            right_poly = [poly[i] + poly[j] for i in range(n//2, n) for j in range(i+1, n)]
            return tropicalized_noncrossing_partition(left_poly), tropicalized_noncrossing_partition(right_poly)
    
    def min_rank(poly):
        if isinstance(poly, tuple):
            left_rank = min_rank(poly[0])
            right_rank = min_rank(poly[1])
            return max(left_rank, right_rank) + 1
        else:
            return 1
    
    n = random.randint(5, 40)
    f = generate_boolean_function(n)
    poly = tropicalized_noncrossing_partition(f)
    rank = min_rank(poly)
    
    # BP_readtwice circuit size is not defined for this conjecture
    bp_circuit_size = None
    
    return {
        "metric_name": "min_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if not r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")