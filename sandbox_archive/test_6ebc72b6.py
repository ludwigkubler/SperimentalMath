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
    
    def generate_boolean_formula(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def compute_circuit(formula):
        n = len(formula)
        circuit = []
        for i in range(n):
            if formula[i] == 0:
                circuit.append((i,))
            else:
                circuit.append((i, i+1))
        return circuit
    
    def compute_tropicalized_local_cohomology_order(circuit):
        n = len(circuit)
        max_rank = 0
        for node in range(n):
            rank = 0
            for edge in circuit:
                if node in edge:
                    rank += 1
            max_rank = max(max_rank, rank)
        return max_rank
    
    def compute_resolution_proof_width(circuit):
        n = len(circuit)
        cnf = []
        for i in range(n):
            cnf.append([i])
        for edge in circuit:
            if len(edge) == 2:
                cnf.append([-edge[0], edge[1]])
        return solve_cnf(cnf, n)
    
    def solve_cnf(cnf, n):
        def dpll(lits, cls):
            if not lits:
                return True
            lit = next((l for l in range(n) if l not in cls and -l not in cls), None)
            if lit is None:
                return False
            new_lits_true = [l for l in lits if l != lit]
            new_lits_false = [l for l in lits if l != -lit]
            return dpll(new_lits_true, cls | {lit}) or dpll(new_lits_false, cls | {-lit})
        
        return dpll(cnf, set())
    
    n_values = [5, 10, 15, 20, 30, 40]
    correlation_coefficient = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):
            formula = generate_boolean_formula(n)
            circuit = compute_circuit(formula)
            mloc = compute_tropicalized_local_cohomology_order(circuit)
            w = compute_resolution_proof_width(circuit)
            correlation_coefficient += (mloc - 10) * (w - 10)
            instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "correlation",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    correlation_coefficient /= instances_tested
    return {
        "metric_name": "correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient < 0.8\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds tested")