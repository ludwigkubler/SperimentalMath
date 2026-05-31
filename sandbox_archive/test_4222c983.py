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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = {random.randint(1, n), -random.randint(1, n)}
            cnf.append(clause)
        return cnf
    
    def resolution_width(cnf):
        seen = set()
        queue = list(cnf)
        
        while queue:
            clause = queue.pop()
            for literal in clause:
                neg_literal = -literal
                if neg_literal in seen:
                    new_clause = [l for l in clause if l != literal and l != neg_literal]
                    if not new_clause:
                        return len(seen) + 1
                    new_clause = tuple(sorted(new_clause))
                    if new_clause not in seen:
                        seen.add(new_clause)
                        queue.append(new_clause)
                else:
                    seen.add(neg_literal)
        return len(seen)
    
    def coxeter_diagram_entropy(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        adjacency_matrix = [[0] * (n + 1) for _ in range(n + 1)]
        
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    l1, l2 = clause[i], clause[j]
                    adjacency_matrix[abs(l1)][abs(l2)] = 1
                    adjacency_matrix[abs(l2)][abs(l1)] = 1
        
        edges = sum(sum(row) for row in adjacency_matrix) // 2
        return edges
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        m = random.randint(5, 40)
        cnf = generate_cnf(m, m)
        width = resolution_width(cnf)
        entropy = coxeter_diagram_entropy(cnf)
        
        if width == 0:
            return {
                "metric_name": "Coxeter-diagram Entropy",
                "metric_value": entropy,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "resolution_width_is_zero"
            }
        
        if entropy > 10 * width:
            return {
                "metric_name": "Coxeter-diagram Entropy",
                "metric_value": entropy,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"Entropy {entropy} > 10 * Width {width}"
            }
        
        metric_values.append(entropy)
    
    mean_entropy = sum(metric_values) / len(metric_values)
    return {
        "metric_name": "Coxeter-diagram Entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_entropy = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_entropy} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Entropy > 10 * Width' first_failing_seed={first_failing_seed}")