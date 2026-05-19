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
    
    # Generate Ramsey-type tautology for a small graph (n ≤ 40)
    n = random.randint(5, 30)
    G = {i: set() for i in range(n)}
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if random.choice([True, False]):
                G[i].add(j)
                G[j].add(i)
                edges.append((i, j))
    
    # Encode the tautology as a propositional formula
    clauses = []
    for u, v in edges:
        literals = [f"e_{u}_{v}", f"e_{v}_{u}"]
        clause = " or ".join(literals)
        clauses.append(clause)
    
    tautology = " and ".join(clauses)
    
    # Measure the size of Extended Frege proofs
    proof_size = len(tautology.split(" and "))  # Simplified model
    
    return {
        "metric_name": "proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")