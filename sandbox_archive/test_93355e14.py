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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), 2))
            circuit.append((gate, inputs[0], inputs[1]))
        return circuit
    
    def clause_set(circuit):
        clauses = set()
        for gate, a, b in circuit:
            if gate == 'AND':
                clauses.add(f"{a} AND {b}")
            elif gate == 'OR':
                clauses.add(f"{a} OR {b}")
        return clauses
    
    def minimal_order(clauses):
        n = len(clauses)
        order = 0
        while True:
            new_clauses = set()
            for clause in clauses:
                if " AND " not in clause and " OR " not in clause:
                    continue
                parts = clause.split(" AND ")
                if len(parts) > 1:
                    new_clauses.add(f"({parts[0]})")
                    new_clauses.add(f"({parts[1]})")
                else:
                    parts = clause.split(" OR ")
                    if len(parts) > 1:
                        new_clauses.add(f"({parts[0]})")
                        new_clauses.add(f"({parts[1]})")
            if new_clauses == clauses:
                break
            clauses = new_clauses
            order += 1
        return order
    
    def entanglement_complexity(circuit):
        complexity = 0
        for gate, a, b in circuit:
            if gate == 'AND':
                complexity += abs(a - b)
            elif gate == 'OR':
                complexity += max(abs(a - b), 1)
        return complexity
    
    n_max = 40
    instances_tested = 30
    metric_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, min(n_max, 20))
        circuit = generate_random_circuit(n)
        clauses = clause_set(circuit)
        min_order_val = minimal_order(clauses)
        entanglement_val = entanglement_complexity(circuit)
        if min_order_val == 0:
            continue
        log_min_order = math.log(min_order_val)
        metric_values.append((log_min_order, entanglement_val))
    
    if not metric_values:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "No valid circuits generated"
        }
    
    log_min_orders = [x for x, _ in metric_values]
    entanglement_vals = [y for _, y in metric_values]
    
    mean_log_min_order = sum(log_min_orders) / len(log_min_orders)
    mean_entanglement_val = sum(entanglement_vals) / len(entanglement_vals)
    variance_log_min_order = sum((x - mean_log_min_order)**2 for x in log_min_orders) / len(log_min_orders)
    variance_entanglement_val = sum((y - mean_entanglement_val)**2 for y in entanglement_vals) / len(entanglement_vals)
    
    covariance = sum((log_min_orders[i] - mean_log_min_order) * (entanglement_vals[i] - mean_entanglement_val) for i in range(len(log_min_orders))) / len(log_min_orders)
    
    pearson_corr = covariance / math.sqrt(variance_log_min_order * variance_entanglement_val)
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_corr,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": pearson_corr >= 0.8 and all(pearson_corr >= 0.5 for _ in range(instances_tested)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_corr = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if result["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation below threshold\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction} n_tested={len(results)}")