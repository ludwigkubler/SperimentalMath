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
    
    def generate_boolean_formula(n):
        return ''.join(random.choice('01') for _ in range(2**n))
    
    def compute_simplicial_complex(phi):
        n = phi.count('1')
        simplicial_complex = []
        for i in range(1, 2**n):
            if all(phi[j] == '1' for j in range(n) if (i >> j) & 1):
                simplicial_complex.append([j for j in range(n) if (i >> j) & 1])
        return simplicial_complex
    
    def compute_local_coherence(simplicial_complex):
        n = len(simplicial_complex)
        M = [[0] * n for _ in range(n)]
        for face in simplicial_complex:
            for i in range(len(face)):
                for j in range(i + 1, len(face)):
                    M[face[i]][face[j]] += 1
                    M[face[j]][face[i]] += 1
        return sum(sum(row) for row in M) / (2 * n * (n - 1))
    
    def compute_frege_proof_depth(phi):
        stack = []
        depth = 0
        max_depth = 0
        for char in phi:
            if char == '0':
                stack.pop()
                depth -= 1
            else:
                stack.append(char)
                depth += 1
                max_depth = max(max_depth, depth)
        return max_depth
    
    n_values = [5, 10, 15, 20, 30, 40]
    local_coherence_sum = 0
    proof_depth_sum = 0
    instances_tested = 0
    n_max = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            phi = generate_boolean_formula(n)
            simplicial_complex = compute_simplicial_complex(phi)
            local_coherence = compute_local_coherence(simplicial_complex)
            proof_depth = compute_frege_proof_depth(phi)
            
            local_coherence_sum += local_coherence
            proof_depth_sum += proof_depth
            instances_tested += 1
            n_max = max(n_max, n)
    
    mean_local_coherence = local_coherence_sum / instances_tested
    mean_proof_depth = proof_depth_sum / instances_tested
    
    correlation_coefficient = (instances_tested * sum(local_coherence * proof_depth for local_coherence, proof_depth in zip(local_coherence_values, proof_depth_values)) -
                               sum(local_coherence_values) * sum(proof_depth_values)) / \
                              math.sqrt((instances_tested * sum(local_coherence**2 for local_coherence in local_coherence_values) - sum(local_coherence_values)**2) *
                                        (instances_tested * sum(proof_depth**2 for proof_depth in proof_depth_values) - sum(proof_depth_values)**2))
    
    conjecture_holds = correlation_coefficient > 0.7
    counterexample = "" if conjecture_holds else "correlation_coefficient < 0.7"
    
    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] and r["metric_value"] < 0.5 for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"] and r["metric_value"] < 0.5)
        print(f"RESULT: FALSIFIED counterexample='correlation_coefficient < 0.7' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")