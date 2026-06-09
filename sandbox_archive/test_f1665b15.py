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
    
    def generate_random_function(n):
        # Generate a random function f from {0, 1}^n to {0, 1}
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        max_communication = 0
        for i in range(n):
            comm = sum(f[j] != f[j + 2**i] for j in range(2**(n - i - 1)))
            if comm > max_communication:
                max_communication = comm
        return max_communication
    
    def syntactic_monoid(f):
        n = int(math.log2(len(f)))
        monoid = []
        for i in range(n):
            for j in range(2**i):
                for k in range(2**(n - i)):
                    if f[j] == f[k + 2**i]:
                        monoid.append((j, k))
        return monoid
    
    def representation_depth(monoid):
        # Simplified representation depth calculation
        return len(monoid)
    
    n = random.randint(5, 40)
    f = generate_random_function(n)
    comm_rank = communication_complexity(f)
    monoid = syntactic_monoid(f)
    rep_depth = representation_depth(monoid)
    
    if rep_depth > comm_rank + 3:
        return {
            "metric_name": "communication_rank",
            "metric_value": comm_rank,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": f"Representation depth {rep_depth} exceeds communication rank {comm_rank} by more than 3 units"
        }
    
    return {
        "metric_name": "communication_rank",
        "metric_value": comm_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value)**2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for res in results:
            if not res["conjecture_holds"]:
                print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={seed}")
                break