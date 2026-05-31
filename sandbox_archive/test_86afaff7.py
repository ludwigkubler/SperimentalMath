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
    
    def generate_circuit(n):
        circuit = []
        for _ in range(2**(n-1)):
            gate = random.choice(['AND', 'OR'])
            inputs = [random.randint(0, 1) for _ in range(n)]
            circuit.append((gate, inputs))
        return circuit
    
    def monotone_complexity(circuit):
        n = len(circuit[0][1])
        complexity = 2**n
        for gate, inputs in circuit:
            if gate == 'AND':
                complexity *= 2
            elif gate == 'OR':
                complexity *= (2**(len(inputs) - 1))
        return complexity
    
    def coxeter_group_order(circuit):
        n = len(circuit[0][1])
        order = 2**n
        for _ in range(2**(n-1)):
            order *= 2
        return order
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        complexity = monotone_complexity(circuit)
        order = coxeter_group_order(circuit)
        results.append((n, complexity, order))
    
    if len(results) < 30:
        return {
            "metric_name": "Coxeter Group Order vs Monotone Complexity",
            "metric_value": None,
            "instances_tested": len(results),
            "n_max": max(n for n, _, _ in results),
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mean_complexity = sum(c for _, c, _ in results) / len(results)
    mean_order = sum(o for _, _, o in results) / len(results)
    correlation = 0
    n = len(results)
    for i in range(n):
        correlation += (results[i][1] - mean_complexity) * (results[i][2] - mean_order)
    correlation /= (n * math.sqrt(sum((c - mean_complexity)**2 for c, _, _ in results)) * math.sqrt(sum((o - mean_order)**2 for _, _, o in results)))
    
    return {
        "metric_name": "Coxeter Group Order vs Monotone Complexity",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(correlation) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **trial_result}}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_corr = sum(result["metric_value"] for result in results) / len(results)
        support_fraction = sum(1 for result in results if "conjecture_holds" in result and result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_corr} std=0.0 support_fraction={support_fraction}")
    elif any("counterexample" in result for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result)
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")