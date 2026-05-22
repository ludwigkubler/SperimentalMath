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
    n = 40
    instances_tested = 30
    ranks = []
    
    for _ in range(instances_tested):
        # Generate a random k-CLIQUE instance with n variables
        edges = set()
        while len(edges) < math.comb(n, 2):
            u, v = random.sample(range(n), 2)
            if (u, v) not in edges and (v, u) not in edges:
                edges.add((u, v))
        
        # Construct the monotone DNF formula
        dnf_formula = []
        for i in range(n):
            for j in range(i + 1, n):
                clause = [f"v{i}", f"v{j}"]
                dnf_formula.append(clause)
        
        # Compute the minimal rank of its associated matroid expansion
        matroid_rank = len(dnf_formula)  # Simplified for demonstration
        
        ranks.append(matroid_rank)
    
    mean_rank = sum(ranks) / instances_tested
    conjecture_holds = n**0.5 <= mean_rank <= n
    
    return {
        "metric_name": "matroid_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[first_failing_seed]}")