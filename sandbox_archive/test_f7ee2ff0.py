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
    
    def groupoid_automorphism_group(cnf):
        n = len(cnf)
        if n == 0:
            return 1
        
        # Generate all possible permutations of variables
        perms = list(itertools.permutations(range(1, n + 1)))
        
        # Check each permutation for automorphism property
        aut_group_size = 0
        for perm in perms:
            if all((lit > 0 and perm[lit - 1] > 0) or (lit < 0 and perm[-lit] < 0) for lit in cnf):
                aut_group_size += 1
        
        return aut_group_size
    
    def resolution_proof_width(cnf):
        # Placeholder function to simulate resolution proof width calculation
        # This is a dummy implementation, replace with actual logic
        return len(cnf)
    
    instances_tested = 0
    total_aut_group_size = 0
    total_w_phi = 0
    n_max = 0
    
    for _ in range(30):
        n = random.randint(5, 40)
        cnf = [random.choice([-i, i]) for _ in range(n) for _ in range(random.randint(1, 2))]
        aut_group_size = groupoid_automorphism_group(cnf)
        w_phi = resolution_proof_width(cnf)
        
        instances_tested += 1
        total_aut_group_size += aut_group_size
        total_w_phi += w_phi
        n_max = max(n_max, n)
    
    if instances_tested < 30:
        return {
            "metric_name": "aut_group_size_over_w_phi",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_aut_group_size = total_aut_group_size / instances_tested
    mean_w_phi = total_w_phi / instances_tested
    correlation_coefficient = (instances_tested * sum(aut_group_size * w_phi for aut_group_size, w_phi in zip(cnf, cnf)) - 
                               total_aut_group_size * total_w_phi) / math.sqrt((instances_tested * sum(aut_group_size**2 for aut_group_size in cnf) - total_aut_group_size**2) *
                                                                 (instances_tested * sum(w_phi**2 for w_phi in cnf) - total_w_phi**2))
    
    return {
        "metric_name": "aut_group_size_over_w_phi",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and mean_aut_group_size / mean_w_phi <= 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, **result}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / (len(results) - 1))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient<0.8' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")