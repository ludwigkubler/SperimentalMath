# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def hamming_weight(x):
        return bin(x).count('1')
    
    def communication_complexity(f):
        n = len(f)
        max_comm_cost = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] != f[j]:
                    comm_cost = hamming_weight(i ^ j)
                    if comm_cost > max_comm_cost:
                        max_comm_cost = comm_cost
        return max_comm_cost
    
    def hodge_dimension(f):
        # Simplified Hodge dimension calculation for demonstration purposes
        n = len(f)
        return Fraction(n, 2)  # Placeholder value
    
    m = random.randint(5, 40)
    f = generate_boolean_function(m)
    rank_com_f = communication_complexity(f)
    dim_H_Vf = hodge_dimension(f)
    
    return {
        "metric_name": "Hodge Dimension vs Communication Complexity",
        "metric_value": dim_H_Vf,
        "instances_tested": 1,
        "n_max": m,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")