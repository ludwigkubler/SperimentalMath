# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
from itertools import product

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def dpll(circuit):
        if not circuit:
            return True
        for literal in circuit[0]:
            if literal > 0 and literal in assignment:
                continue
            assignment.add(literal)
            if dpll(circuit[1:]):
                return True
            assignment.remove(literal)
            if -literal in assignment:
                continue
            assignment.add(-literal)
            if dpll(circuit[1:]):
                return True
            assignment.remove(-literal)
        return False
    
    def monotone_complexity(circuit):
        assignment = set()
        return sum(1 for clause in circuit if any(lit > 0 and lit in assignment or -lit not in assignment for lit in clause))
    
    def quasi_crystal_order(circuit):
        n = len(circuit)
        if n == 0:
            return 0
        lattice_points = set()
        for i, clause in enumerate(circuit):
            for literal in clause:
                lattice_points.add((i, literal))
        order = 0
        for point in lattice_points:
            neighbors = [(point[0] + dx, point[1]) for dx in [-1, 1]]
            if all(neighbor in lattice_points for neighbor in neighbors):
                order += 1
        return order
    
    def generate_circuit(n):
        circuit = []
        for _ in range(random.randint(2, n)):
            clause = [random.choice([-1, 1]) * (i + 1) for i in random.sample(range(n), random.randint(1, n))]
            circuit.append(clause)
        return circuit
    
    instances_tested = 0
    total_order = 0
    total_complexity = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            circuit = generate_circuit(n)
            instances_tested += 1
            complexity = monotone_complexity(circuit)
            order = quasi_crystal_order(circuit)
            total_order += order
            total_complexity += complexity
    
    if instances_tested == 0:
        return {
            "metric_name": "quasi_crystal_order",
            "metric_value": 0,
            "instances_tested": 0,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "empty_circuit"
        }
    
    mean_order = total_order / instances_tested
    mean_complexity = total_complexity / instances_tested
    
    if instances_tested < 30:
        return {
            "metric_name": "quasi_crystal_order",
            "metric_value": 0,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    correlation_coefficient = (mean_order * mean_complexity - total_order * total_complexity / instances_tested**2) / \
                              math.sqrt((total_order**2 / instances_tested - mean_order**2) * 
                                          (total_complexity**2 / instances_tested - mean_complexity**2))
    
    return {
        "metric_name": "quasi_crystal_order",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(correlation_coefficient) >= 0.8 and abs(mean_order - mean_complexity) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"n={r['instances_tested']}, order={total_order}, complexity={total_complexity}"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={seed}")
                break
        else:
            print("RESULT: INCONCLUSIVE insufficient_data")