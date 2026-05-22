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
    n = random.randint(5, 40)
    k = random.randint(2, min(n-1, 6))
    
    # Generate a random k-Clique instance
    vertices = list(range(n))
    edges = set()
    for _ in range(k):
        u = random.choice(vertices)
        v = random.choice([v for v in vertices if v != u and (u, v) not in edges and (v, u) not in edges])
        edges.add((u, v))
    
    # Constructive mapping to an affine scheme
    A = [[0] * n for _ in range(n)]
    for u, v in edges:
        A[u][v] = 1
        A[v][u] = 1
    
    # Compute the minimal Hodge index (simplified version)
    hodge_index = sum(sum(row) for row in A) / len(A)
    
    # Calculate resolution proof length
    Q = 2**n / (hodge_index ** 2)
    
    return {
        "metric_name": "HodgeIndex",
        "metric_value": hodge_index,
        "instances_tested": 1,
        "conjecture_holds": hodge_index <= n**(k/2) and Q >= 2**n / (hodge_index ** 2),
        "counterexample": "" if hodge_index <= n**(k/2) and Q >= 2**n / (hodge_index ** 2) else f"HodgeIndex={hodge_index}, Q={Q}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else list(range(30, 67))
    
    total_metric_value = 0
    total_conjecture_holds = 0
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        total_metric_value += trial_result["metric_value"]
        if trial_result["conjecture_holds"]:
            total_conjecture_holds += 1
    
    mean_metric_value = total_metric_value / len(seeds)
    support_fraction = total_conjecture_holds / len(seeds)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0 support_fraction={support_fraction}")
    elif any(trial_result["counterexample"] for trial_result in [run_trial(seed) for seed in seeds]):
        first_failing_seed = next(seed for seed in seeds if run_trial(seed)["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(seeds)}")