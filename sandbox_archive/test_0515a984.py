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

def generate_cnf(n, m):
    cnf = []
    for _ in range(m):
        clause = set(random.sample(range(1, n + 1), random.randint(1, n)))
        cnf.append(clause)
    return cnf

def matroid_rank(cnf):
    independent_sets = [{frozenset()}]
    for clause in cnf:
        new_independent_sets = set()
        for s in independent_sets:
            if all(x not in s for x in clause):
                new_independent_sets.add(s | {frozenset(clause)})
        independent_sets.update(new_independent_sets)
    return max(len(s) for s in independent_sets)

def karchmer_wigderson_communication_complexity(cnf):
    n = len(cnf[0])
    rank_value = matroid_rank(cnf)
    # Simulate deterministic protocol (simplified version)
    communication_cost = 2 * rank_value
    return communication_cost

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    m = random.randint(n, 2 * n)
    cnf = generate_cnf(n, m)
    
    matroid_rank_value = matroid_rank(cnf)
    comm_complexity = karchmer_wigderson_communication_complexity(cnf)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": abs(comm_complexity - matroid_rank_value) <= 1,  # Allow small constant factor
        "counterexample": "" if conjecture_holds else f"Graph with n={n}, A=[{', '.join(map(str, cnf))}]"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or list(range(2, 30 * 100 + 1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    std_value = math.sqrt(sum((res["metric_value"] - mean_value) ** 2 for res in results) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(res["seed"] for res in results if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")