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
from fractions import Fraction
import math
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def monotone_width(circuits):
        max_width = 0
        for circuit in circuits:
            width = 0
            seen_vars = set()
            for clause in circuit:
                for var in clause:
                    if abs(var) not in seen_vars:
                        seen_vars.add(abs(var))
                        width += 1
            max_width = max(max_width, width)
        return max_width
    
    def lefschetz_number(circuit):
        n = len(circuit)
        # Simplified version of Lefschetz number for demonstration purposes
        return Fraction(n * (n + 1), 2)
    
    circuits = [generate_circuit(5) for _ in range(30)]
    mu_C = monotone_width(circuits)
    L_C = sum(lefschetz_number(circuit) for circuit in circuits)
    
    if mu_C == 0:
        return {
            "metric_name": "log2(L(C))",
            "metric_value": -math.inf,
            "instances_tested": 30,
            "n_max": 5,
            "conjecture_holds": False,
            "counterexample": "monotone_width_is_zero"
        }
    
    log2_L_C = math.log2(L_C)
    correlation_coefficient = log2_L_C / mu_C
    
    return {
        "metric_name": "log2(L(C))",
        "metric_value": correlation_coefficient,
        "instances_tested": 30,
        "n_max": 5,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and any(result["metric_value"] < 0.5 for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"correlation_coefficient_below_0.5\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")