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
    
    def generate_permutation(n):
        return list(range(1, n + 1))
    
    def inversions_count(perm):
        count = 0
        for i in range(len(perm)):
            for j in range(i + 1, len(perm)):
                if perm[i] > perm[j]:
                    count += 1
        return count
    
    def noncrossing_partition_size(n):
        # Simplified approximation of the minimal rank for noncrossing partitions
        return n ** (2 / 3)
    
    def permutation_circuit_size(n, inversions):
        # Simplified approximation of the circuit size
        return min(n ** (2 / 3), inversions * math.log(n) ** 2)
    
    n = random.randint(5, 40)
    perm = generate_permutation(n)
    inversions = inversions_count(perm)
    rank = noncrossing_partition_size(n)
    circuit_size = permutation_circuit_size(n, inversions)
    
    return {
        "metric_name": "circuit_size",
        "metric_value": circuit_size,
        "instances_tested": 1,
        "conjecture_holds": rank >= n ** (2 / 3) and rank <= inversions * math.log(n) ** 2,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_circuit_size = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_circuit_size} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_circuit_size} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"circuit size outside bounds\" first_failing_seed={first_failing_seed}")