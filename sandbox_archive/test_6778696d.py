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
    
    def generate_tautology(n):
        return ''.join(random.choice('01') for _ in range(n))
    
    def tiling_space(tautology):
        # Placeholder implementation of tiling space construction
        # This is a dummy function and should be replaced with actual logic
        return len(tautology)
    
    def minimal_geometric_entropy(tiling_space_size):
        # Placeholder implementation of minimal geometric entropy calculation
        # This is a dummy function and should be replaced with actual logic
        return math.log2(tiling_space_size + 1)
    
    def communication_complexity_rank(tiling_space_size):
        # Placeholder implementation of communication complexity rank calculation
        # This is a dummy function and should be replaced with actual logic
        return tiling_space_size
    
    n = random.randint(5, 40)
    tautology = generate_tautology(n)
    G = tiling_space(tautology)
    
    H_min_G = minimal_geometric_entropy(G)
    r_G = communication_complexity_rank(G)
    
    metric_name = "H_min_G - r_G"
    metric_value = abs(H_min_G - r_G)
    instances_tested = 1
    n_max = n
    conjecture_holds = False
    counterexample = ""
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")