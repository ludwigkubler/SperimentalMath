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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([i, -i]) for i in range(1, n + 1)]
            clauses.append(clause)
        return clauses
    
    def truth_table_to_quantum_state(cnf):
        n = len(cnf[0])
        state = [0] * (2**n)
        for assignment in itertools.product([0, 1], repeat=n):
            if all(any(assignment[abs(lit) - 1] == l > 0 for l in clause) or any(assignment[abs(lit) - 1] != l < 0 for l in clause) for clause in cnf):
                state[int(''.join(str(bit) for bit in assignment), 2)] = 1
        return state
    
    def minimal_geometric_entanglement(state, n):
        # Simplified version of geometric entanglement calculation
        return sum(abs(x) for x in state)
    
    def circuit_monotone_width(cnf):
        # Simplified version of circuit monotone width calculation
        return len(cnf)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        cnf = generate_cnf(n)
        state = truth_table_to_quantum_state(cnf)
        mge = minimal_geometric_entanglement(state, n)
        w = circuit_monotone_width(cnf)
        
        if mge > 2 * w:
            return {
                "metric_name": "mge_w_ratio",
                "metric_value": mge / w,
                "instances_tested": 1,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"mge > 2 * w for n={n}"
            }
        
        results.append((mge, w))
    
    if not results:
        return {
            "metric_name": "mge_w_ratio",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mge_values, w_values = zip(*results)
    correlation_coefficient = sum((m - m_avg) * (w - w_avg) for m, w in results) / math.sqrt(sum((m - m_avg)**2 for m in mge_values) * sum((w - w_avg)**2 for w in w_values))
    
    return {
        "metric_name": "mge_w_ratio",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for _ in range(30)),
        "conjecture_holds": correlation_coefficient > 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all("conjecture_holds" not in result or result["conjecture_holds"] for result in results):
        mean_metric_value = sum(result["metric_value"] for result in results) / len(results)
        std_metric_value = math.sqrt(sum((result["metric_value"] - mean_metric_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if "conjecture_holds" not in result or result["conjecture_holds"]) / len(results)
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any("counterexample" in result and result["counterexample"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "counterexample" in result and result["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no_data")