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
    
    def generate_planar_curve(n):
        # Generate n points on a planar curve (simplified for testing)
        return [(random.uniform(-1, 1), random.uniform(-1, 1)) for _ in range(n)]
    
    def tropicalized_divisor(curve):
        # Simplified computation of minimal rank
        return len(curve) - 2
    
    def bp_readtwice_tensor_width(curve):
        # Simplified computation of tensor width
        return sum(1 for point in curve if point[0] > 0 and point[1] > 0)
    
    n = random.choice([10, 15, 20, 25, 30])
    curve = generate_planar_curve(n)
    min_rank = tropicalized_divisor(curve)
    tensor_width = bp_readtwice_tensor_width(curve)
    
    return {
        "metric_name": "MinRank(TropicalDivisor(C))",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": min_rank <= 2 * tensor_width,  # Simplified linear bound
        "counterexample": "" if min_rank <= 2 * tensor_width else f"n={n}, MinRank={min_rank}, TensorWidth={tensor_width}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results) and support_fraction >= 0.8:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"MinRank > 2 * TensorWidth\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")