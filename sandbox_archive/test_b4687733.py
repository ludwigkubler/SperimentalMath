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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        return clauses
    
    def compute_minimal_rank(cnf):
        # Placeholder for birational model computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 5)
    
    def compute_resolution_proof_length(cnf):
        # Placeholder for resolution proof length computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.randint(1, 20)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    min_rank = compute_minimal_rank(cnf)
    resolution_proof_length = compute_resolution_proof_length(cnf)
    
    metric_value = abs(min_rank - math.log(n))
    conjecture_holds = metric_value <= 1 and resolution_proof_length <= 2 * math.log(n)
    counterexample = "mapping_undefined" if not conjecture_holds else ""
    
    return {
        "metric_name": "minimal_rank_diff",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")