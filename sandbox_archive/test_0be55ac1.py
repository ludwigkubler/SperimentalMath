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
    
    def generate_random_circuit(n):
        circuit = []
        for _ in range(2**n):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
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
    
    def minimal_quandle_action_order(clauses):
        n = len(clauses)
        order = 0
        while True:
            new_clauses = set()
            for clause in clauses:
                if any(x not in clause for x in range(n)):
                    continue
                new_clause = tuple(sorted(set(clause) - {x}))
                new_clauses.add(new_clause)
            if new_clauses == clauses:
                break
            clauses = new_clauses
            order += 1
        return order
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        complexity = 0
        for gate, inputs in circuit:
            complexity += len(inputs)
        return complexity
    
    def pearson_correlation(x, y):
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        cov_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y)) / len(x)
        std_x = math.sqrt(sum((xi - mean_x)**2 for xi in x) / len(x))
        std_y = math.sqrt(sum((yi - mean_y)**2 for yi in y) / len(y))
        return cov_xy / (std_x * std_y)
    
    n_values = [5, 10, 15, 20, 30, 40]
    all_log_min_order = []
    all_entanglement_complexity = []
    
    for n in n_values:
        for _ in range(30):
            circuit = generate_random_circuit(n)
            clauses = clause_set(circuit)
            min_order = minimal_quandle_action_order(clauses)
            entanglement_comp = entanglement_complexity(circuit)
            all_log_min_order.append(math.log(min_order))
            all_entanglement_complexity.append(entanglement_comp)
    
    correlation_coefficient = pearson_correlation(all_log_min_order, all_entanglement_complexity)
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(all_log_min_order),
        "n_max": max(n_values),
        "conjecture_holds": 0.5 <= correlation_coefficient < 0.8,
        "counterexample": "" if 0.5 <= correlation_coefficient < 0.8 else "Pearson correlation coefficient is outside the expected range"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='Pearson correlation coefficient is outside the expected range' first_failing_seed={first_failing_seed}")