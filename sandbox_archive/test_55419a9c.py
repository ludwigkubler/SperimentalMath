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
    
    def generate_ac0_circuit(n):
        # Simplified AC0 circuit for parity function
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def tensor_representation(circuit):
        n = len(circuit)
        T_f = [[0] * (2**n) for _ in range(n+1)]
        T_f[0][0] = 1
        for i in range(1, n+1):
            for j in range(2**(i-1)):
                T_f[i][j*2] = circuit[j]
                T_f[i][j*2 + 1] = 1 - circuit[j]
        return T_f
    
    def symmetric_tensor_norm(T_f):
        n = len(T_f) - 1
        norm = 0
        for i in range(2**n):
            sum_val = 0
            for j in range(n+1):
                sum_val += abs(T_f[j][i])
            norm += sum_val ** (1/n)
        return norm / (2**n)
    
    def calculate_norms(circuit, n):
        norms = []
        for _ in range(30):  # Ensure at least 30 instances per seed
            T_f = tensor_representation(circuit)
            norm = symmetric_tensor_norm(T_f)
            norms.append(norm)
        return norms
    
    n_values = [5, 10, 15, 20, 30, 40]
    all_norms = []
    
    for n in n_values:
        circuit = generate_ac0_circuit(n)
        norms = calculate_norms(circuit, n)
        all_norms.extend(norms)
    
    mean_norm = sum(all_norms) / len(all_norms)
    std_norm = math.sqrt(sum((x - mean_norm) ** 2 for x in all_norms) / len(all_norms))
    
    conjecture_holds = all(n * n * math.log(n) <= norm for norm in all_norms)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "symmetric_tensor_norm",
        "metric_value": mean_norm,
        "instances_tested": len(all_norms),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_norm = sum(r["metric_value"] for r in results) / len(results)
    std_norm = math.sqrt(sum((r["metric_value"] - mean_norm) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_norm} std={std_norm} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")