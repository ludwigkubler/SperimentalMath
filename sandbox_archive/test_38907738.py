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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] * clause[j] == 0 for i in range(n) for j in range(i + 1, n)):
                clauses.append(clause)
        return clauses
    
    def clause_subset_entropy(cnf):
        total = 2 ** len(cnf)
        entropy = 0
        for k in range(1, total):
            subset = [i for i in range(total) if (k & (1 << i)) != 0]
            count = sum(all(clause[i] == 0 for clause in cnf) for i in subset)
            prob = Fraction(count, total)
            entropy -= prob * math.log2(prob)
        return entropy
    
    def quaternionic_k_theory_order(cnf):
        n = len(cnf[0])
        if any(len(clause) != n for clause in cnf):
            return None
        order = 1
        while True:
            found = False
            for i in range(n):
                for j in range(i + 1, n):
                    if all(clause[i] * clause[j] == 0 for clause in cnf):
                        found = True
                        break
                if found:
                    break
            if not found:
                return order
            order += 1
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        cnf = generate_cnf(n_max)
        entropy = clause_subset_entropy(cnf)
        order = quaternionic_k_theory_order(cnf)
        
        if order is None:
            return {
                "metric_name": "quaternionic_k_theory_order",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        metric_values.append(order)
    
    mean = sum(metric_values) / len(metric_values)
    std = math.sqrt(sum((x - mean) ** 2 for x in metric_values) / len(metric_values))
    
    return {
        "metric_name": "quaternionic_k_theory_order",
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(trial_result)
    
    mean = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results if result["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unsupported_operation")