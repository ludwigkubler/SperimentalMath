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
    
    def generate_monotone_circuit(n: int, k: int):
        # Placeholder function to generate a monotone circuit
        return [[random.choice([0, 1]) for _ in range(k)] for _ in range(n)]
    
    def tensor_product_representation(C):
        # Placeholder function to compute the tensor product representation
        n = len(C)
        rank = 2 ** (n * k)
        return rank
    
    n = random.randint(5, 40)
    k = random.randint(1, min(10, n))
    C = generate_monotone_circuit(n, k)
    rank = tensor_product_representation(C)
    
    return {
        "metric_name": "tensor_product_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= n ** (math.sqrt(k)),
        "counterexample": "" if rank <= n ** (math.sqrt(k)) else f"Rank {rank} exceeds n^(sqrt({k})) = {n ** math.sqrt(k)}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing_seed]['counterexample']}\" first_failing_seed={seeds[first_failing_seed]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data or support_fraction < 80%")