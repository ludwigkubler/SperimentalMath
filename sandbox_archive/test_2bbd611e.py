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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set(random.sample(range(1, n+1), 3))
            if len(clause & {i for i in range(1, n+1) if -i in clause}) == 0:
                clauses.append(clause)
        return clauses
    
    def circuit_depth(cnf):
        # Simplified heuristic for circuit depth
        return max(len(clause) for clause in cnf)
    
    def geometric_langlands_duality_invariant(cnf):
        # Placeholder function, replace with actual computation
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    total_instances = 0
    
    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n, random.randint(1, n*2))
            d_phi = geometric_langlands_duality_invariant(cnf)
            d_circuit = circuit_depth(cnf)
            results.append({"n": n, "d_phi": d_phi, "d_circuit": d_circuit})
            total_instances += 1
    
    if len(results) < 30:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(result["n"] for result in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    correlation = sum((result["d_phi"] - mean_d_phi) * (result["d_circuit"] - mean_d_circuit) for result in results)
    correlation /= len(results)
    mean_d_phi = sum(result["d_phi"] for result in results) / len(results)
    mean_d_circuit = sum(result["d_circuit"] for result in results) / len(results)
    
    conjecture_holds = all(abs(result["d_phi"]) >= 2**len([lit for lit in cnf if -lit in cnf]) for result in results)
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "not_provided"
        mean_value = None
        std_value = None
        support_fraction = sum(result["conjecture_holds"] for result in results) / len(results)
    
    print(f"RESULT: {'SUPPORTED' if all(result['conjecture_holds'] for result in results) else 'FALSIFIED'} mean={mean_value} std={std_value} support_fraction={support_fraction}")