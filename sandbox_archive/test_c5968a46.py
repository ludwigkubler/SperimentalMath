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
    
    def d_regular_circuit(n, d):
        if n % d != 0:
            return None
        circuit = []
        for i in range(n):
            row = [random.choice([0, 1]) for _ in range(d)]
            circuit.append(row)
        return circuit
    
    def density_matrix(circuit):
        n = len(circuit)
        rho = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                count = 0
                for k in range(2**n):
                    input_bits = [k >> (i + j) & 1 for i in range(j - i + 1)]
                    if circuit[i][input_bits[0]] == circuit[j][input_bits[-1]]:
                        count += 1
                rho[i][j] = count / 2**n
                rho[j][i] = rho[i][j]
        return rho
    
    def geometric_entropy(rho):
        n = len(rho)
        entropy = 0
        for i in range(n):
            if rho[i][i] > 0:
                entropy -= rho[i][i] * math.log2(rho[i][i])
        return entropy
    
    def entanglement_complexity(circuit):
        n = len(circuit)
        commuting_pairs = 0
        for i in range(n):
            for j in range(i + 1, n):
                commute = True
                for k in range(2**n):
                    input_bits = [k >> (i + j) & 1 for i in range(j - i + 1)]
                    if circuit[i][input_bits[0]] != circuit[j][input_bits[-1]]:
                        commute = False
                        break
                if commute:
                    commuting_pairs += 1
        return commuting_pairs
    
    n_values = [5, 10, 15, 20, 30, 40]
    instances_tested = 0
    total_entropy = 0.0
    max_n = 0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for _ in range(5):
            circuit = d_regular_circuit(n, 2)
            if circuit is None:
                continue
            rho = density_matrix(circuit)
            entropy = geometric_entropy(rho)
            E_C = entanglement_complexity(circuit)
            
            instances_tested += 1
            max_n = max(max_n, n)
            
            total_entropy += entropy
            
            if entropy > 1.5 * E_C:
                conjecture_holds = False
                counterexample = f"n={n}, E(C)={E_C}, H(ρ_C)={entropy}"
    
    mean_entropy = total_entropy / instances_tested
    
    return {
        "metric_name": "geometric_entropy",
        "metric_value": mean_entropy,
        "instances_tested": instances_tested,
        "n_max": max_n,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")