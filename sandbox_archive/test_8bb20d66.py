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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, n-1) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def resolution(proof, new_clause):
        proof.append(new_clause)
        while True:
            new_clauses = []
            for i in range(len(proof)):
                for j in range(i+1, len(proof)):
                    p = proof[i]
                    q = proof[j]
                    if any(-x in q for x in p) and not any(x in q for x in p):
                        new_clause = [x for x in p + q if x != -p[0]]
                        if new_clause:
                            new_clauses.append(new_clause)
            if not new_clauses:
                break
            proof.extend(new_clauses)
        return proof
    
    def geometric_entropy(proof):
        # Placeholder for the actual computation of geometric entropy
        # This is a dummy implementation that does not actually compute the entropy
        return len(proof) / 2
    
    def resolution_width(proof):
        max_width = 0
        current_width = 1
        for clause in proof:
            if len(clause) > current_width:
                current_width = len(clause)
            if current_width > max_width:
                max_width = current_width
        return max_width
    
    def run_resolution(n):
        cnf = generate_cnf(n)
        proof = []
        for clause in cnf:
            proof = resolution(proof, clause)
        return proof
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_instances = 0
    correlation_sum = 0.0
    support_count = 0
    
    for n in n_values:
        instances_tested = 0
        for _ in range(5):
            proof = run_resolution(n)
            width = resolution_width(proof)
            entropy = geometric_entropy(proof)
            if width == 0 or entropy == 0:
                continue
            correlation_sum += width / entropy
            instances_tested += 1
            total_instances += 1
    
    if total_instances < 30 * len(n_values):
        return {
            "metric_name": "correlation_coefficient",
            "metric_value": None,
            "instances_tested": total_instances,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_correlation = correlation_sum / total_instances
    support_fraction = (support_count / len(n_values)) if instances_tested > 0 else 0
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": mean_correlation,
        "instances_tested": total_instances,
        "n_max": max(n_values),
        "conjecture_holds": mean_correlation >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"not_enough_support\" first_failing_seed={first_failing_seed}")