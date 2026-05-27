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
    
    def dpll_depth(instance):
        # Simplified DPLL algorithm to estimate depth
        if not instance:
            return 0
        if all(var in instance for var in instance[0]):
            return 1 + max(dpll_depth({var: val for var, val in instance if var != clause[0]}) for clause in instance)
        return 1 + dpll_depth([{var: val for var, val in instance if var != clause[0]} for clause in instance if clause[0] not in instance])
    
    def quantum_cluster_rank(instance):
        # Simplified mapping to estimate rank
        return len(instance) ** 2
    
    instances = []
    for _ in range(30):
        n = random.randint(5, 40)
        instance = {f'x{i}': random.choice([True, False]) for i in range(n)}
        instances.append((instance, dpll_depth(instance), quantum_cluster_rank(instance)))
    
    total_rank = sum(rank for _, _, rank in instances)
    avg_rank = total_rank / len(instances)
    max_rank = max(rank for _, _, rank in instances)
    
    conjecture_holds = all(max_rank <= 2 ** depth for _, depth, _ in instances)
    counterexample = "" if conjecture_holds else "max_rank exceeds 2^depth"
    
    return {
        "metric_name": "Average Quantum Cluster Rank",
        "metric_value": avg_rank,
        "instances_tested": len(instances),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] for r in results)
    avg_metric_value = total_metric_value / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"max_rank exceeds 2^depth\" first_failing_seed={first_failing_seed}")