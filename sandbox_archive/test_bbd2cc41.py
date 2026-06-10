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
    
    def generate_group(n):
        if n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        else:
            elements = list(range(n))
            for i in range(1, n):
                elements.append(i * (n - 1) % n)
            return elements
    
    def generate_representation(group, dim):
        if dim == 1:
            return [[1]]
        elif dim == 2:
            return [[1, 0], [0, 1]]
        else:
            rep = []
            for _ in range(dim):
                row = [random.randint(0, 1) for _ in range(dim)]
                if sum(row) != 0:
                    rep.append(row)
            return rep
    
    def compute_automorphism_group(rep, group):
        n = len(group)
        dim = len(rep)
        aut_group = []
        for perm in itertools.permutations(range(n)):
            permuted_rep = [[rep[i][perm[j]] for j in range(dim)] for i in range(dim)]
            if permuted_rep == rep:
                aut_group.append(perm)
        return aut_group
    
    def communication_complexity(rep):
        n = len(rep)
        dim = len(rep[0])
        max_comm = 0
        for i in range(n):
            for j in range(i + 1, n):
                comm = sum(abs(rep[i][k] - rep[j][k]) for k in range(dim))
                if comm > max_comm:
                    max_comm = comm
        return max_comm
    
    def order_of_group(group):
        return len(group)
    
    n_max = 0
    instances_tested = 0
    total_comm_complexity = 0
    aut_group_orders = []
    
    for _ in range(30):
        n = random.randint(5, 40)
        dim = random.randint(1, 40)
        group = generate_group(n)
        rep = generate_representation(group, dim)
        
        if len(rep) != dim or any(len(row) != dim for row in rep):
            continue
        
        aut_group = compute_automorphism_group(rep, group)
        comm_complexity = communication_complexity(rep)
        aut_group_order = order_of_group(aut_group)
        
        n_max = max(n_max, n)
        instances_tested += 1
        total_comm_complexity += comm_complexity
        aut_group_orders.append(aut_group_order)
    
    if instances_tested < 30:
        return {
            "metric_name": "communication_complexity",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_comm = total_comm_complexity / instances_tested
    std_comm = math.sqrt(sum((comm - mean_comm) ** 2 for comm in aut_group_orders) / instances_tested)
    support_fraction = sum(1 for order in aut_group_orders if order <= n_max ** 2) / len(aut_group_orders)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "support_fraction < 0.8"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_comm = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len([r for r in results if r["metric_value"] is not None])
    std_comm = math.sqrt(sum((r["metric_value"] - mean_comm) ** 2 for r in results if r["metric_value"] is not None)) / len([r for r in results if r["metric_value"] is not None])
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_comm} std={std_comm} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")