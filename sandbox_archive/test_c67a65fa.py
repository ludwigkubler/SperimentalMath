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
    
    def generate_boolean_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), 2))
            circuit.append((gate, inputs))
        return circuit
    
    def clause_set(circuit):
        clauses = set()
        for gate, inputs in circuit:
            if gate == 'AND':
                clauses.add(tuple(sorted(inputs)))
            elif gate == 'OR':
                clauses.add(tuple(sorted(inputs)))
        return clauses
    
    def minimal_order(clauses):
        n = len(clauses)
        order = 0
        while True:
            new_clauses = set()
            for clause in clauses:
                if len(clause) > 1:
                    new_clauses.update({tuple(sorted([x, y])) for x, y in itertools.combinations(clause, 2)})
            if new_clauses == clauses:
                break
            clauses = new_clauses
            order += 1
        return order
    
    def entanglement_complexity(circuit):
        # Placeholder function; actual implementation needed
        return len(circuit)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_boolean_circuit(n)
        clauses = clause_set(circuit)
        min_order = minimal_order(clauses)
        entanglement_complexity_val = entanglement_complexity(circuit)
        
        if min_order == 0 or entanglement_complexity_val == 0:
            continue
        
        results.append((math.log(min_order), entanglement_complexity_val))
    
    if not results:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "No valid instances found"
        }
    
    n = len(results)
    x_sum, y_sum, xy_sum, xx_sum, yy_sum = 0, 0, 0, 0, 0
    
    for x, y in results:
        x_sum += x
        y_sum += y
        xy_sum += x * y
        xx_sum += x ** 2
        yy_sum += y ** 2
    
    mean_x = x_sum / n
    mean_y = y_sum / n
    numerator = n * xy_sum - x_sum * y_sum
    denominator = math.sqrt((n * xx_sum - x_sum ** 2) * (n * yy_sum - y_sum ** 2))
    
    if denominator == 0:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": n,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "Denominator is zero"
        }
    
    pearson_correlation = numerator / denominator
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_correlation,
        "instances_tested": n,
        "n_max": max(n_values),
        "conjecture_holds": pearson_correlation >= 0.8 and all(pearson_correlation >= 0.5 for _, _ in results),
        "counterexample": "" if pearson_correlation >= 0.8 else f"Pearson correlation < 0.5: {pearson_correlation}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if not all(result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        mean_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results if result["metric_value"] is not None) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")