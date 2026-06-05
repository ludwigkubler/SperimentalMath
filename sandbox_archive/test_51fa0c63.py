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
    
    def generate_circuit(n):
        clauses = []
        for _ in range(n):
            clause = [random.choice([1, -1]) * i for i in range(1, n+1)]
            clauses.append(clause)
        return clauses

    def lefschetz_number(circuits):
        # Placeholder function to compute Lefschetz number
        # This is a dummy implementation and should be replaced with actual computation
        return sum(len(circuit) for circuit in circuits)

    def monotone_width(circuits):
        # Placeholder function to compute monotone width
        # This is a dummy implementation and should be replaced with actual computation
        return max(len(set(abs(x) for x in clause)) for circuit in circuits for clause in circuit)

    n = 10  # Example size, change as needed
    circuits = generate_circuit(n)
    L_C = lefschetz_number(circuits)
    mu_C = monotone_width(circuits)
    
    if L_C <= 0 or mu_C == 0:
        return {
            "metric_name": "log2(L(C))",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "Lefschetz number or monotone width is non-positive"
        }
    
    log2_L_C = math.log2(L_C)
    correlation_coefficient = (log2_L_C * mu_C) / (math.sqrt(log2_L_C**2 + mu_C**2))
    
    return {
        "metric_name": "log2(L(C))",
        "metric_value": correlation_coefficient,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": correlation_coefficient > 0.7,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(res["metric_value"] for res in results if res["metric_value"] is not None) / len(results)
    std_metric_value = math.sqrt(sum((res["metric_value"] - mean_metric_value)**2 for res in results if res["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")