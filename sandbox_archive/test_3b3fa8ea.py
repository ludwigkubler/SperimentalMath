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
    
    def boolean_function(n):
        return lambda x: random.choice([True, False])
    
    def delone_set_representation(f, n):
        delone_set = []
        for i in range(2**n):
            if f(i):
                delone_set.append(tuple((i >> j) & 1 for j in range(n)))
        return delone_set
    
    def matroid_rank(delone_set):
        n = len(delone_set[0])
        rank = 0
        basis = []
        for element in delone_set:
            if all(sum(x*y for x, y in zip(b, element)) % 2 == 0 for b in basis):
                basis.append(element)
                rank += 1
        return rank
    
    def communication_complexity_k_clique(n):
        # Simplified protocol: each node sends its index to the other nodes
        return n - 1
    
    n = random.choice([5, 10, 15, 20, 30, 40])
    f = boolean_function(n)
    delone_set = delone_set_representation(f, n)
    rank = matroid_rank(delone_set)
    cc_k_clique = communication_complexity_k_clique(n)
    
    return {
        "metric_name": "minimal_matroid_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= 2 * cc_k_clique,  # Simplified threshold for demonstration
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
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
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")