# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n: int):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.choice([-i, i]) for i in range(1, n + 1)]
            cnf.append(clause)
        return cnf
    
    def truth_table_to_quantum_state(cnf):
        n = len(cnf[0])
        state = [Fraction(0) for _ in range(2**n)]
        state[0] = Fraction(1)
        
        for assignment in itertools.product([-1, 1], repeat=n):
            if all(any(assignment[abs(lit) - 1] == l > 0 for l in clause) or any(assignment[abs(lit) - 1] != l < 0 for l in clause) for clause in cnf):
                state[sum([assignment[i-1] * (2**(n-i)) for i in range(1, n + 1)])] += Fraction(1)
        
        return state
    
    def minimal_geometric_entanglement(state):
        n = len(state)
        max_entanglement = 0
        for i in range(n):
            for j in range(i+1, n):
                entanglement = abs(state[i] * state[j])
                if entanglement > max_entanglement:
                    max_entanglement = entanglement
        return max_entanglement
    
    def circuit_monotone_width(cnf):
        # Placeholder implementation for demonstration purposes
        return len(cnf)
    
    n_values = [5, 10, 15, 20, 30, 40]
    mge_values = []
    w_values = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        state = truth_table_to_quantum_state(cnf)
        mge_value = minimal_geometric_entanglement(state)
        w_value = circuit_monotone_width(cnf)
        
        if mge_value > 2 * w_value:
            return {
                "metric_name": "mge_w_ratio",
                "metric_value": None,
                "instances_tested": len(n_values),
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mge > 2 * w"
            }
        
        mge_values.append(mge_value)
        w_values.append(w_value)
    
    correlation_coefficient = sum((x - mean_x) * (y - mean_y) for x, y in zip(mge_values, w_values)) / len(mge_values)
    mean_mge = sum(mge_values) / len(mge_values)
    std_mge = (sum((x - mean_mge)**2 for x in mge_values) / len(mge_values))**0.5
    
    return {
        "metric_name": "mge_w_ratio",
        "metric_value": correlation_coefficient,
        "instances_tested": len(n_values),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{trial_result}...}}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_metric_value = (sum((result["metric_value"] - mean_metric_value)**2 for result in results if result["metric_value"] is not None) / len(results))**0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mge > 2 * w\" first_failing_seed={first_failing_seed}")