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
    
    def truth_table_to_quantum_state(cnf):
        n = len(cnf[0])
        state = [0] * (2 ** n)
        
        for assignment in itertools.product([True, False], repeat=n):
            if all(any(assignment[abs(lit) - 1] == l > 0 for l in clause) or any(assignment[abs(lit) - 1] != l < 0 for l in clause) for clause in cnf):
                state[tuple(assignment)] += 1
        
        return state
    
    def calculate_minimal_geometric_entanglement(state):
        n = int(math.log2(len(state)))
        total_probability = sum(state)
        
        entanglement = 0
        for i in range(n):
            prob_i = sum(state[j] for j in range(2 ** (i + 1)) if j & (1 << i))
            entanglement += -prob_i * math.log2(prob_i / total_probability)
        
        return entanglement
    
    def calculate_circuit_monotone_width(cnf):
        n = len(cnf[0])
        width = float('inf')
        
        for assignment in itertools.product([True, False], repeat=n):
            if all(any(assignment[abs(lit) - 1] == l > 0 for l in clause) or any(assignment[abs(lit) - 1] != l < 0 for l in clause) for clause in cnf):
                width = min(width, sum(1 for lit in assignment if lit))
        
        return width
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_mge = 0.0
    total_w = 0.0
    
    for n in n_values:
        for _ in range(5):
            cnf = [[random.choice([-1, 1]) * (i + 1) for i in range(n)] for _ in range(random.randint(2, n))]
            state = truth_table_to_quantum_state(cnf)
            mge = calculate_minimal_geometric_entanglement(state)
            w = calculate_circuit_monotone_width(cnf)
            
            if mge > 2 * w:
                return {
                    "metric_name": "mge_w_correlation",
                    "metric_value": None,
                    "instances_tested": instances_tested,
                    "n_max": n,
                    "conjecture_holds": False,
                    "counterexample": f"mge > 2w for n={n}"
                }
            
            total_mge += mge
            total_w += w
            instances_tested += 1
    
    mean_mge = total_mge / instances_tested
    mean_w = total_w / instances_tested
    correlation_coefficient = (instances_tested * sum(mge * w for mge, w in zip([mge for _, mge in run_trial(seed).items()], [w for _, w in run_trial(seed).items()])) - instances_tested * mean_mge * mean_w) / math.sqrt((instances_tested * sum(mge**2 for mge in [mge for _, mge in run_trial(seed).items()]) - instances_tested * mean_mge**2) * (instances_tested * sum(w**2 for w in [w for _, w in run_trial(seed).items()]) - instances_tested * mean_w**2))
    
    return {
        "metric_name": "mge_w_correlation",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mge > 2w\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")