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
        for _ in range(2 * n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def construct_quandle(clauses):
        quandle = {}
        for x in range(1, n + 1):
            quandle[x] = {x}
        for clause in clauses:
            a, b = abs(clause[0]), abs(clause[1])
            if clause[0] > 0 and clause[1] > 0:
                quandle[a].update(quandle[b])
                quandle[b].update(quandle[a])
            elif clause[0] > 0 and clause[1] < 0:
                quandle[a].discard(b)
                quandle[b].discard(a)
            elif clause[0] < 0 and clause[1] > 0:
                quandle[-a].discard(-b)
                quandle[-b].discard(-a)
            else:
                quandle[-a].update(quandle[-b])
                quandle[-b].update(quandle[-a])
        return quandle
    
    def calculate_order(quandle):
        order = 0
        for x in quandle:
            if len(quandle[x]) > order:
                order = len(quandle[x])
        return order
    
    def calculate_clause_complexity(clauses):
        return len(clauses)
    
    n_values = [5, 10, 15, 20, 30, 40]
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):
            clauses = generate_sat_instance(n)
            quandle = construct_quandle(clauses)
            order = calculate_order(quandle)
            complexity = calculate_clause_complexity(clauses)
            
            metrics.append({
                "n": n,
                "order": order,
                "complexity": complexity
            })
            instances_tested += 1
            if n > n_max:
                n_max = n
    
    correlation_sum = 0
    for i in range(instances_tested):
        for j in range(i + 1, instances_tested):
            r1 = metrics[i]["order"]
            c1 = metrics[i]["complexity"]
            r2 = metrics[j]["order"]
            c2 = metrics[j]["complexity"]
            correlation_sum += (r1 - r2) * (c1 - c2)
    
    mean_order = sum(metric["order"] for metric in metrics) / instances_tested
    std_dev = math.sqrt(sum((metric["order"] - mean_order) ** 2 for metric in metrics) / instances_tested)
    correlation_coefficient = correlation_sum / (instances_tested * std_dev * std_dev)
    
    conjecture_holds = correlation_coefficient >= 0.7 and all(metric["order"] <= n**(3/2) for metric in metrics)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
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
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_dev:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")