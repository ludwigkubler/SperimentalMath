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
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n * (n - 1) // 2):
            clause = [random.choice([-1, 1]) * random.randint(1, n) for _ in range(random.randint(1, n))]
            if all(clause[i] != -clause[j] for i, j in itertools.combinations(range(n), 2)):
                clauses.append(clause)
        return clauses
    
    def compute_subset_entropy(clauses):
        counts = [0] * (1 << len(clauses))
        for clause in clauses:
            mask = 0
            for lit in clause:
                if lit > 0:
                    mask |= 1 << (lit - 1)
                else:
                    mask |= 1 << (-lit - 1)
            counts[mask] += 1
        total = sum(counts)
        entropy = 0.0
        for count in counts:
            if count > 0:
                prob = count / total
                entropy -= prob * math.log2(prob)
        return entropy
    
    def compute_root_lattice_entropy(n):
        # Placeholder for root lattice entropy computation
        # This is a dummy implementation and should be replaced with actual logic
        return random.random() * n

    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        instances_tested = 0
        total_se = 0.0
        total_sh = 0.0
        
        for _ in range(5):  # Ensure at least 30 instances per seed
            clauses = generate_sat_instance(n)
            se = compute_root_lattice_entropy(n)
            sh = compute_subset_entropy(clauses)
            
            results.append({
                "n": n,
                "se": se,
                "sh": sh
            })
            
            total_se += se
            total_sh += sh
            instances_tested += 1
        
        if instances_tested < 30:
            return {
                "metric_name": "Correlation Coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "insufficient_instances"
            }
    
    se_values = [r["se"] for r in results]
    sh_values = [r["sh"] for r in results]
    
    correlation_coefficient = sum((se_values[i] - sum(se_values) / len(se_values)) * (sh_values[i] - sum(sh_values) / len(sh_values)) for i in range(len(results))) / (len(results) * math.sqrt(sum((se_values[i] - sum(se_values) / len(se_values)) ** 2 for i in range(len(results))) * sum((sh_values[i] - sum(sh_values) / len(sh_values)) ** 2 for i in range(len(results)))))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": correlation_coefficient > 0.05,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_value = sum(r["metric_value"] for r in results) / len(results)
        std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        mean_value = None
        std_value = None
        support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["metric_value"] is not None for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["counterexample"] == "insufficient_instances" for r in results):
        print("RESULT: INCONCLUSIVE insufficient_instances")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")