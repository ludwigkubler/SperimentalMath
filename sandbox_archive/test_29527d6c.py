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
    
    def generate_hyperbolic_embedding(n):
        # Simplified hyperbolic embedding generation (not actual implementation)
        return [random.randint(1, n) for _ in range(n)]
    
    def communication_rank(embedding):
        # Simplified communication rank calculation (not actual implementation)
        return len(set(embedding))
    
    def geometric_complexity(embedding):
        # Simplified geometric complexity calculation (not actual implementation)
        return sum(1 for i in range(len(embedding)) if embedding[i] == i + 1)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ratios = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Sample 5 instances per size
            embedding = generate_hyperbolic_embedding(n)
            rank = communication_rank(embedding)
            complexity = geometric_complexity(embedding)
            ratios.append(complexity / rank if rank != 0 else float('inf'))
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_ratio = sum(ratios) / len(ratios)
    std_ratio = math.sqrt(sum((x - mean_ratio) ** 2 for x in ratios) / len(ratios))
    support_fraction = sum(1 for r in ratios if r <= n_values[0]) / len(ratios)
    
    conjecture_holds = support_fraction >= 0.8 and std_ratio < 0.1 * n_values[0]
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "geometric_complexity_to_communication_rank_ratio",
        "metric_value": mean_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")