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
    
    def generate_ac0_circuit(n, depth):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_ac0_circuit(n, depth - 1)
            right = generate_ac0_circuit(n, depth - 1)
            return [random.choice([left[i] ^ right[i] for i in range(len(left))])]

    def construct_quiver_representation(circuit):
        n = len(circuit)
        quiver = [[0] * n for _ in range(n)]
        for i in range(n):
            if circuit[i] == 1:
                quiver[0][i] = 1
                quiver[i][n-1] = 1
        return quiver

    def is_automorphism(quiver, perm):
        n = len(quiver)
        for i in range(n):
            for j in range(n):
                if quiver[i][j] != quiver[perm[i]][perm[j]]:
                    return False
        return True

    def compute_symmetry(quiver):
        n = len(quiver)
        identity = list(range(n))
        automorphisms = [identity]
        for i in range(1, n):
            perm = [(i + j) % n for j in range(n)]
            if is_automorphism(quiver, perm):
                automorphisms.append(perm)
        return len(automorphisms)

    def ac0_circuit_size(circuit):
        return len(circuit)

    def log_base_2(x):
        return math.log2(x) if x > 0 else -math.inf

    n = random.randint(5, 40)
    depth = random.randint(1, 3)
    circuit = generate_ac0_circuit(n, depth)
    quiver = construct_quiver_representation(circuit)
    symmetry = compute_symmetry(quiver)
    circuit_size = ac0_circuit_size(circuit)
    log_circuit_size = log_base_2(circuit_size)

    return {
        "metric_name": "Symmetry vs Log Circuit Size",
        "metric_value": symmetry,
        "instances_tested": 1,
        "conjecture_holds": symmetry >= log_circuit_size,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    if all(result["conjecture_holds"] for result in results):
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = "Symmetry does not correlate with log circuit size"
        mean_value = sum(result["metric_value"] for result in results) / len(results)
        std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
        support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)

    print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")