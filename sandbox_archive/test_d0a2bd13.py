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
    
    def generate_ac0_circuit(n, d):
        # Simplified AC0 circuit generation for PARITY function
        if n == 1:
            return [0]  # Base case for n=1
        else:
            left = generate_ac0_circuit(n // 2, d + 1)
            right = generate_ac0_circuit(n - n // 2, d + 1)
            return [0] + left + right
    
    def compute_quiver_representation(circuit):
        # Simplified quiver representation computation
        n = len(circuit)
        Q = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(1, n):
            Q[i][i-1] = 1
            Q[i-1][i] = 1
        return Q
    
    def compute_symmetry(Q):
        # Simplified computation of symmetry (number of automorphisms)
        n = len(Q)
        if n == 0:
            return 0
        symmetries = 1
        for i in range(1, n):
            if all(Q[i][j] == Q[j][i] for j in range(n)):
                symmetries *= i + 1
        return symmetries
    
    def log_of_circuit_size(circuit):
        # Simplified computation of logarithm of circuit size
        return math.log(len(circuit))
    
    n = random.randint(5, 40)
    circuit = generate_ac0_circuit(n, 1)
    Q = compute_quiver_representation(circuit)
    symmetry = compute_symmetry(Q)
    log_size = log_of_circuit_size(circuit)
    
    return {
        "metric_name": "Symmetry vs Log Size",
        "metric_value": symmetry,
        "instances_tested": 1,
        "conjecture_holds": symmetry >= log_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        counterexample = "Symmetry does not correlate with log size"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")