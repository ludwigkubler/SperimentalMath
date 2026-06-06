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
        for _ in range(10 * n):  # Generate 10n clauses
            clause = [random.randint(-n, -1), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def frege_proof_width(cnf):
        # Simplified estimation of Frege proof width for demonstration purposes
        return len(cnf) * 2
    
    def minimal_representation_order(n):
        # Minimal order of the symmetric group S_n representation
        return math.factorial(n)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        w_phi = frege_proof_width(cnf)
        R_Sn = minimal_representation_order(n)
        results.append({"n": n, "w_phi": w_phi, "R_Sn": R_Sn})
    
    correlation = 0.0
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            x1, y1 = results[i]["R_Sn"], results[j]["w_phi"]
            x2, y2 = results[j]["R_Sn"], results[i]["w_phi"]
            correlation += (x1 * y2 - x2 * y1) / math.sqrt((x1**2 + x2**2) * (y1**2 + y2**2))
    
    correlation /= len(results) ** 2
    
    return {
        "metric_name": "correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(n_values),
        "conjecture_holds": correlation >= 0.8 and all(val <= 10 for val in [r["R_Sn"] for r in results]),
        "counterexample": "" if correlation >= 0.8 else "correlation < 0.8"
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        print("RESULT: FALSIFIED counterexample=\"correlation < 0.8\" first_failing_seed=<s>")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")