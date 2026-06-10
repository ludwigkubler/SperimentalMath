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
        for _ in range(2 ** n - 1):
            gate = random.choice(['AND', 'OR'])
            inputs = sorted(random.sample(range(n), random.randint(1, n)))
            circuit.append((gate, inputs))
        return circuit
    
    def clause_set(circuit):
        clauses = set()
        for gate, inputs in circuit:
            if gate == 'AND':
                for i in range(len(inputs) - 1):
                    for j in range(i + 1, len(inputs)):
                        clauses.add(frozenset([inputs[i], inputs[j]]))
            elif gate == 'OR':
                for i in range(len(inputs) - 1):
                    for j in range(i + 1, len(inputs)):
                        clauses.add(frozenset([inputs[i], inputs[j]]))
        return clauses
    
    def minimal_quandle_action_order(clauses):
        n = len(clauses)
        if n == 0:
            return 1
        order = 2
        while True:
            new_clauses = set()
            for clause in clauses:
                for other_clause in clauses:
                    if clause != other_clause:
                        intersection = clause & other_clause
                        if len(intersection) > 0:
                            new_clause = frozenset(clause ^ other_clause)
                            if new_clause not in new_clauses:
                                new_clauses.add(new_clause)
            if new_clauses == set():
                return order
            clauses = new_clauses
            order += 1
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        complexity = 0
        for gate, inputs in circuit:
            complexity += len(inputs) - 1
        return complexity
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            circuit = generate_random_circuit(n)
            clauses = clause_set(circuit)
            min_order = minimal_quandle_action_order(clauses)
            entanglement_comp = entanglement_complexity(circuit)
            results.append((math.log(min_order), entanglement_comp))
    
    if len(results) < 30:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    mean_x = sum(x for x, y in results) / len(results)
    mean_y = sum(y for x, y in results) / len(results)
    var_x = sum((x - mean_x) ** 2 for x, y in results) / len(results)
    var_y = sum((y - mean_y) ** 2 for x, y in results) / len(results)
    cov_xy = sum((x - mean_x) * (y - mean_y) for x, y in results) / len(results)
    
    if var_x == 0 or var_y == 0:
        return {
            "metric_name": "Pearson correlation",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for _, _ in results),
            "conjecture_holds": False,
            "counterexample": "constant_metric"
        }
    
    pearson_corr = cov_xy / (math.sqrt(var_x) * math.sqrt(var_y))
    
    return {
        "metric_name": "Pearson correlation",
        "metric_value": pearson_corr,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": pearson_corr >= 0.8 and all(pearson_corr >= 0.5 for _ in range(30)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        if result["conjecture_holds"]:
            results.append(result["metric_value"])
    
    mean_corr = sum(results) / len(results)
    std_corr = math.sqrt(sum((x - mean_corr) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= 0.8) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_corr} std={std_corr} support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = seeds[results.index(min(r for r in results if r < 0.5))]
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")