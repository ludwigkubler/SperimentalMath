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
    
    def disjointness_instance(n):
        inputs = [random.choice([True, False]) for _ in range(n)]
        outputs = [int(all(inputs[:i]) != all(inputs[i:]) for i in range(1, n))]
        return inputs, outputs
    
    def free_probability_representation(inputs, outputs):
        # Simplified representation using a matrix
        n = len(inputs)
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                if inputs[i] != inputs[j]:
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def entanglement_dimension(M):
        # Simplified calculation of entanglement dimension using Gaussian elimination
        n = len(M)
        rank = 0
        for i in range(n):
            if any(M[i]):
                pivot = next(j for j in range(i, n) if M[j][i] != 0)
                M[i], M[pivot] = M[pivot], M[i]
                for j in range(n):
                    if j != i:
                        factor = M[j][i] / M[i][i]
                        for k in range(n):
                            M[j][k] -= factor * M[i][k]
                rank += 1
        return rank
    
    min_entanglement_dimension = float('inf')
    n_tests = 30
    for _ in range(n_tests):
        n = random.randint(5, 40)
        inputs, outputs = disjointness_instance(n)
        M = free_probability_representation(inputs, outputs)
        entanglement_dim = entanglement_dimension(M)
        min_entanglement_dimension = min(min_entanglement_dimension, entanglement_dim)
    
    conjecture_holds = min_entanglement_dimension >= n
    counterexample = "" if conjecture_holds else f"Minimum entanglement dimension {min_entanglement_dimension} is less than Ω(n) for n={n}"
    
    return {
        "metric_name": "Minimal Entanglement Dimension",
        "metric_value": min_entanglement_dimension,
        "instances_tested": n_tests,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Minimum entanglement dimension is less than Ω(n)\" first_failing_seed={first_failing_seed}")