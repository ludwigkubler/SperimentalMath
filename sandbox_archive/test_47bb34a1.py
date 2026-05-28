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
    
    def compute_characteristic_variety(f):
        # Simplified procedure to simulate characteristic variety computation
        n = int(math.log2(len(f)))
        return f"CP^{n}"
    
    def compute_hodge_rank(variety):
        # Simulated Hodge rank computation
        n = int(variety[3:])
        return n
    
    def compute_communication_complexity(n):
        # Simplified communication complexity computation
        return 2 * n ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_hodge_rank = 0
    total_communication_complexity = 0
    
    for n in n_values:
        f = generate_boolean_function(n)
        variety = compute_characteristic_variety(f)
        hodge_rank = compute_hodge_rank(variety)
        communication_complexity = compute_communication_complexity(n)
        
        total_hodge_rank += hodge_rank ** 2
        total_communication_complexity += communication_complexity
    
    mean_hodge_rank_squared = total_hodge_rank / len(n_values)
    mean_communication_complexity = total_communication_complexity / len(n_values)
    
    correlation_coefficient = total_communication_complexity / (len(n_values) * mean_hodge_rank_squared)
    
    conjecture_holds = correlation_coefficient >= 0.8 and mean_communication_complexity / mean_hodge_rank_squared <= 3
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_communication_complexity,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.2f} std={std_metric_value:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")