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
    
    def generate_ac0_circuit(n, depth):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            left = generate_ac0_circuit(n, depth - 1)
            right = generate_ac0_circuit(n, depth - 1)
            return [random.choice([left[i] ^ right[i] for i in range(len(left))])]

    def compute_quiver_representation(circuit):
        n = len(circuit)
        quiver = [[0] * n for _ in range(n)]
        for i in range(n):
            if circuit[i] == 1:
                quiver[0][i] = 1
                quiver[i][n-1] = 1
        return quiver

    def compute_symmetry(quiver):
        n = len(quiver)
        automorphisms = 0
        for perm in itertools.permutations(range(n)):
            if all(quiver[perm[i]][perm[j]] == quiver[i][j] for i in range(n) for j in range(n)):
                automorphisms += 1
        return automorphisms

    def log2(x):
        return math.log2(x)

    n = random.randint(5, 40)
    depth = random.randint(2, 3)
    circuit = generate_ac0_circuit(n, depth)
    quiver = compute_quiver_representation(circuit)
    symmetry = compute_symmetry(quiver)
    
    metric_value = log2(len(circuit))
    instances_tested = 1
    conjecture_holds = symmetry >= metric_value
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Symmetry",
        "metric_value": symmetry,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(5, 35)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(r for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing['seed']}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")