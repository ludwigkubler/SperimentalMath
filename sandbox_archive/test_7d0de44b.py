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
    
    def agm(values):
        if not values:
            return 0
        product = 1
        sum_values = 0
        for v in values:
            product *= v
            sum_values += v
        n = len(values)
        return (product ** (1/n)) * (sum_values / n)
    
    def depth_of_resolution_proof(clause_sizes):
        if not clause_sizes:
            return 0
        max_size = max(clause_sizes)
        return math.ceil(math.log2(max_size))
    
    n = random.choice([30, 35, 40])
    m = random.randint(1, 2*n)
    clauses = [random.randint(1, n) for _ in range(m)]
    clause_sizes = [len(clause) for clause in clauses]
    
    k = random.uniform(0.5, 1)
    agm_value = agm([size ** k for size in clause_sizes])
    depth = depth_of_resolution_proof(clause_sizes)
    
    return {
        "metric_name": "Depth of Resolution Proof",
        "metric_value": depth,
        "instances_tested": 1,
        "conjecture_holds": depth <= agm_value * 2 and depth >= agm_value / 2,
        "counterexample": "" if depth <= agm_value * 2 and depth >= agm_value / 2 else f"Depth {depth} exceeds bounds for AGM({agm_value})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    total_depth = 0
    total_instances = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
        total_depth += trial_result["metric_value"]
        total_instances += trial_result["instances_tested"]
    
    mean_depth = total_depth / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_depth) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_depth} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth exceeds bounds for AGM\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")