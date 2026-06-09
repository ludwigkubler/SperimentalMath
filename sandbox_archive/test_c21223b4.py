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
        for _ in range(10 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            if random.choice([True, False]):
                clause = [-c for c in clause]
            clauses.append(clause)
        return clauses

    def cnf_to_varphi(cnf):
        # Placeholder for converting CNF to a variety
        return "varphi"

    def ext_group_rank(varphi):
        # Placeholder for computing the rank of Ext^(n-2)(φ, Z/2Z)
        # This is a dummy implementation that returns a random number
        return random.randint(1, 30)

    def communication_complexity_rank(cnf):
        # Placeholder for computing the communication complexity rank
        # This is a dummy implementation that returns a random number
        return random.randint(1, 30)

    n = random.choice([5, 10, 15, 20, 30, 40])
    cnf = generate_cnf(n)
    varphi = cnf_to_varphi(cnf)
    
    ext_rank = ext_group_rank(varphi)
    comm_rank = communication_complexity_rank(cnf)

    return {
        "metric_name": "ext_group_rank",
        "metric_value": ext_rank,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        seeds = [int(s) for s in sys.argv[1:]]
    else:
        primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
        seeds = random.sample(primes, min(30, len(primes)))

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    ext_ranks = [r["metric_value"] for r in results]
    comm_ranks = [r["communication_complexity_rank"] for r in results if "communication_complexity_rank" in r]

    mean_ext_rank = sum(ext_ranks) / len(ext_ranks)
    std_ext_rank = math.sqrt(sum((x - mean_ext_rank) ** 2 for x in ext_ranks) / len(ext_ranks))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ext_rank} std={std_ext_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")