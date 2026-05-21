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
    
    def generate_bp(n):
        bp = [[random.choice([0, 1]) for _ in range(n)] for _ in range(n)]
        return bp
    
    def matrix_multiply(A, B):
        m, p = len(A), len(B[0])
        n = len(B)
        result = [[Fraction(0) for _ in range(p)] for _ in range(m)]
        for i in range(m):
            for j in range(p):
                for k in range(n):
                    result[i][j] += A[i][k] * B[k][j]
        return result
    
    def free_probability_tensor_entanglement(bp, ip_2):
        n = len(bp)
        T_i = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        T_j = [[Fraction(0) for _ in range(n)] for _ in range(n)]
        
        # Calculate T_i and T_j
        for i in range(n):
            for j in range(n):
                if bp[i][j] == 1:
                    T_i[i][j] = Fraction(1)
                    T_j[j][i] = Fraction(1)
        
        entanglement = 0
        for i in range(n):
            for j in range(i, n):
                product = matrix_multiply(T_i[i], T_j[j])
                for k in range(n):
                    for l in range(n):
                        if abs(product[k][l]) > entanglement:
                            entanglement = abs(product[k][l])
        return entanglement
    
    def check_bp():
        n = random.randint(5, 40)
        bp = generate_bp(n)
        entanglement = free_probability_tensor_entanglement(bp, None)
        if entanglement > Fraction(math.log(n), 1):
            return {"metric_name": "entanglement", "metric_value": float(entanglement), "instances_tested": 1, "conjecture_holds": False, "counterexample": "BP instance with high entanglement"}
        else:
            return {"metric_name": "entanglement", "metric_value": float(entanglement), "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    def check_ip_2():
        n = random.randint(5, 40)
        ip_2 = generate_bp(n)
        entanglement = free_probability_tensor_entanglement(None, ip_2)
        if entanglement < Fraction(n, 1):
            return {"metric_name": "entanglement", "metric_value": float(entanglement), "instances_tested": 1, "conjecture_holds": False, "counterexample": "IP_2 instance with low entanglement"}
        else:
            return {"metric_name": "entanglement", "metric_value": float(entanglement), "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}
    
    trial_result = check_bp()
    if not trial_result["conjecture_holds"]:
        return trial_result
    
    trial_result.update(check_ip_2())
    return trial_result

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    entanglement_values = [r["metric_value"] for r in results if "entanglement" in r]
    conjecture_holds = all(r["conjecture_holds"] for r in results if "conjecture_holds" in r)
    
    mean_entanglement = sum(entanglement_values) / len(entanglement_values)
    std_dev = math.sqrt(sum((x - mean_entanglement) ** 2 for x in entanglement_values) / len(entanglement_values))
    support_fraction = len([r for r in results if "conjecture_holds" in r and r["conjecture_holds"]]) / len(results)
    
    if conjecture_holds:
        print(f"RESULT: SUPPORTED mean={mean_entanglement} std={std_dev} support_fraction={support_fraction}")
    elif any("counterexample" in r for r in results):
        counterexample = next(r["counterexample"] for r in results if "counterexample" in r)
        first_failing_seed = next(r["seed"] for r in results if "conjecture_holds" not in r or not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")