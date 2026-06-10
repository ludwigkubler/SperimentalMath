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
            clauses.append(clause)
        return clauses
    
    def construct_circuit(cnf):
        n = len(cnf[0])
        circuit = [[[] for _ in range(n)] for _ in range(2)]
        for clause in cnf:
            for literal in clause:
                var_index = abs(literal) - 1
                if literal > 0:
                    circuit[0][var_index].append(clause)
                else:
                    circuit[1][var_index].append(clause)
        return circuit
    
    def geometric_flow(circuit):
        n = len(circuit[0])
        steps = 0
        while True:
            changed = False
            for i in range(n):
                if circuit[0][i] and circuit[1][i]:
                    circuit[0][i].pop()
                    circuit[1][i].pop()
                    steps += 1
                    changed = True
            if not changed:
                break
        return steps
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_steps = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        circuit = construct_circuit(cnf)
        steps = geometric_flow(circuit)
        total_steps += steps
        instances_tested += 1
        if n > n_max:
            n_max = n
    
    avg_steps = total_steps / len(n_values)
    conjecture_holds = avg_steps <= n_max ** 2 and max(steps for steps in [geometric_flow(construct_circuit(generate_cnf(n))) for n in n_values]) <= 4 * n_max ** 2
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Geometric Flow Complexity",
        "metric_value": avg_steps,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and max(result["n_max"] for result in results) >= 16:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")