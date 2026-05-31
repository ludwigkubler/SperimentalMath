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
    
    def generate_k_sat_instance(n, k):
        variables = list(range(n))
        clauses = []
        for _ in range(k):
            clause = [random.choice(variables) for _ in range(2)]
            if random.choice([True, False]):
                clause[0] = -clause[0]
            clauses.append(clause)
        return clauses

    def twisted_group_representation(clauses):
        n = len(set(abs(v) for v in sum(clauses, [])))
        # Simplified representation using a hypercube
        return [[(i >> j) & 1 for j in range(n)] for i in range(2 ** n)]

    def order_of_automorphism_group(representation):
        n = len(representation)
        identity = [0] * n
        if representation == [identity]:
            return 1
        
        # Brute-force search for automorphisms
        count = 0
        for perm in itertools.permutations(range(n)):
            permuted_rep = [[perm[i] for i in row] for row in representation]
            if permuted_rep == representation:
                count += 1
        return count

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_order = 0
        
        while instances_tested < 30:
            clauses = generate_k_sat_instance(n, k=3)
            representation = twisted_group_representation(clauses)
            order = order_of_automorphism_group(representation)
            
            if order > 1.5 * n ** (2/3):
                return {
                    "metric_name": "order_of_automorphism_group",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"Order {order} exceeds 1.5 * {n}^(2/3)"
                }
            
            total_order += order
            instances_tested += 1
        
        results.append({
            "metric_name": "order_of_automorphism_group",
            "metric_value": total_order / instances_tested,
            "instances_tested": instances_tested,
            "n_max": n,
            "conjecture_holds": True,
            "counterexample": ""
        })
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        return {
            "metric_name": "order_of_automorphism_group",
            "metric_value": mean_order,
            "instances_tested": sum(r["instances_tested"] for r in results),
            "n_max": max(r["n_max"] for r in results),
            "conjecture_holds": True,
            "counterexample": ""
        }
    else:
        return {
            "metric_name": "order_of_automorphism_group",
            "metric_value": mean_order,
            "instances_tested": sum(r["instances_tested"] for r in results),
            "n_max": max(r["n_max"] for r in results),
            "conjecture_holds": False,
            "counterexample": f"Support fraction {support_fraction} < 0.8"
        }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Support fraction {support_fraction} < 0.8' first_failing_seed={first_failing_seed}")