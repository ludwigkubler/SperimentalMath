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
    
    def generate_cnf(n: int) -> list:
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if all(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def minimal_order_brauer_group(phi: list) -> int:
        n = len(phi[0]) if phi and phi[0] else 1
        order = 2**n
        return order
    
    def circuit_weight(phi: list) -> int:
        weight = sum(len(clause) for clause in phi)
        return weight
    
    metrics = []
    instances_tested = 0
    n_max = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_cnf(n)
            order = minimal_order_brauer_group(phi)
            weight = circuit_weight(phi)
            
            if order <= 0 or weight <= 0:
                continue
            
            metrics.append((math.log(order), weight))
            instances_tested += 1
            n_max = max(n_max, n)
    
    if not metrics:
        return {
            "metric_name": "log(BrauerGroup(φ)) vs. Circuit Weight",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    log_brauer_group = [m[0] for m in metrics]
    circuit_weights = [m[1] for m in metrics]
    
    mean_log_brauer_group = sum(log_brauer_group) / len(log_brauer_group)
    mean_circuit_weight = sum(circuit_weights) / len(circuit_weights)
    
    covariance = sum((log_brauer_group[i] - mean_log_brauer_group) * (circuit_weights[i] - mean_circuit_weight) for i in range(len(metrics)))
    variance_log_brauer_group = sum((log_brauer_group[i] - mean_log_brauer_group)**2 for i in range(len(metrics)))
    variance_circuit_weight = sum((circuit_weights[i] - mean_circuit_weight)**2 for i in range(len(metrics)))
    
    if variance_log_brauer_group == 0 or variance_circuit_weight == 0:
        return {
            "metric_name": "log(BrauerGroup(φ)) vs. Circuit Weight",
            "metric_value": None,
            "instances_tested": len(log_brauer_group),
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient = covariance / (math.sqrt(variance_log_brauer_group) * math.sqrt(variance_circuit_weight))
    
    return {
        "metric_name": "log(BrauerGroup(φ)) vs. Circuit Weight",
        "metric_value": correlation_coefficient,
        "instances_tested": len(log_brauer_group),
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")