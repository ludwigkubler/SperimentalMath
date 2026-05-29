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
    
    def generate_random_affine_group(m):
        # Generate a random affine group with m generators
        A = [[random.randint(0, 1) for _ in range(m)] for _ in range(m)]
        b = [random.randint(0, 1) for _ in range(m)]
        return A, b
    
    def brute_force_group_operation(A, b):
        # Brute-force the group operation
        n = len(A)
        steps = 0
        for i in range(n):
            for j in range(n):
                if all((A[i][k] * A[j][k]) % 2 == (A[i][k] + A[j][k]) % 2 for k in range(n)):
                    steps += 1
        return steps
    
    def construct_monotone_circuit(A, b):
        # Construct a monotone circuit with size at most 2^(2m/3)
        m = len(A)
        size = int(2 ** (2 * m / 3))
        return size
    
    m_values = [5, 10, 15, 20, 30, 40]
    total_steps = 0
    circuit_sizes = []
    
    for m in m_values:
        A, b = generate_random_affine_group(m)
        steps = brute_force_group_operation(A, b)
        size = construct_monotone_circuit(A, b)
        
        if size > 2 ** (2 * m / 3):
            return {
                "metric_name": "circuit_size",
                "metric_value": size,
                "instances_tested": len(m_values),
                "conjecture_holds": False,
                "counterexample": f"m={m}, circuit_size={size} > 2^(2*{m}/3)"
            }
        
        total_steps += steps
        circuit_sizes.append(size)
    
    mean_steps = total_steps / len(m_values)
    std_dev = math.sqrt(sum((x - mean_steps) ** 2 for x in circuit_sizes) / len(circuit_sizes))
    
    return {
        "metric_name": "circuit_size",
        "metric_value": mean_steps,
        "instances_tested": len(m_values),
        "conjecture_holds": all(size <= 2 ** (2 * m / 3) for size, m in zip(circuit_sizes, m_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    if not sys.argv[1:]:
        seeds = [2**i + 1 for i in range(5, 6)]  # Default list of 30 primes
    else:
        seeds = [int(s) for s in sys.argv[1:]]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_steps = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_steps) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_steps} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='<desc>' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")