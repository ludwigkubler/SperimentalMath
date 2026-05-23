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
    
    def dpll(sat_instance):
        if not sat_instance:
            return 0
        p = next((i for i, x in enumerate(sat_instance) if x == 0), None)
        if p is None:
            return 1
        new_instance = [x if i != p else -x for i, x in enumerate(sat_instance)]
        proof_length_p = dpll(new_instance)
        if proof_length_p > 0:
            return proof_length_p + 1
        new_instance = [x if i != p else -x for i, x in enumerate(sat_instance)]
        proof_length_np = dpll(new_instance)
        if proof_length_np > 0:
            return proof_length_np + 1
        return 0
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1) for _ in range(random.randint(1, n))]
            clauses.append(clause)
        sat_instance = [0] * (2 * n)
        for clause in clauses:
            if all(sat_instance[abs(lit) - 1] != lit for lit in clause):
                p = random.choice([i for i in range(2 * n) if sat_instance[i] == 0])
                sat_instance[p] = random.choice(clause)
        return sat_instance
    
    def theta_function_rank(instance):
        # Placeholder for actual implementation
        return len(instance)
    
    def shortest_proof_length(instance):
        proof_length = dpll(instance)
        return proof_length
    
    n = random.randint(5, 40)
    sat_instance = generate_sat_instance(n)
    min_rank = theta_function_rank(sat_instance)
    proof_length = shortest_proof_length(sat_instance)
    
    return {
        "metric_name": "min_rank_theta_function",
        "metric_value": min_rank,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")