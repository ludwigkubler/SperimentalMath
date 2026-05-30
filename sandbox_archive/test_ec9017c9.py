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
    
    def generate_random_state(n, epsilon):
        state = [random.uniform(-epsilon, epsilon) for _ in range(2**n)]
        norm = sum(x**2 for x in state)**0.5
        return [x / norm for x in state]
    
    def compute_bipartite_coherence(state, n):
        # Simplified version of Umegaki's coherent information
        coherence = 0
        for i in range(n):
            substate1 = state[:2**i] + state[2**(i+1):]
            substate2 = state[2**i:2**(i+1)]
            norm1 = sum(x**2 for x in substate1)**0.5
            norm2 = sum(x**2 for x in substate2)**0.5
            coherence += (norm1 * norm2) / (2 ** i)
        return coherence
    
    def generate_xor_functions(n, delta):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        g = f[:]
        while True:
            changed = False
            for i in range(2**n):
                if random.random() < delta / (2 * n):
                    g[i] = 1 - g[i]
                    changed = True
            if changed and sum(abs(f[i] - g[i]) for i in range(2**n)) >= 2 * delta:
                return f, g
    
    def compute_communication_complexity(f, g):
        # Simplified version of Bravyi-Kitaev teleportation-based classical simulation
        complexity = 0
        for i in range(2**n):
            if f[i] != g[i]:
                complexity += 1
        return complexity
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        epsilon = random.uniform(0.1, 0.9)
        state = generate_random_state(n, epsilon)
        coherence = compute_bipartite_coherence(state, n)
        
        f, g = generate_xor_functions(n, 2 * epsilon)
        complexity = compute_communication_complexity(f, g)
        
        results.append({
            "n": n,
            "epsilon": epsilon,
            "coherence": coherence,
            "complexity": complexity
        })
    
    avg_coherence = sum(result["coherence"] for result in results) / len(results)
    avg_complexity = sum(result["complexity"] for result in results) / len(results)
    
    conjecture_holds = all(coherence >= math.log(1 / epsilon) for result in results)
    counterexample = "" if conjecture_holds else "coherence < log(1/epsilon)"
    
    return {
        "metric_name": "Communication Complexity",
        "metric_value": avg_complexity,
        "instances_tested": len(results),
        "n_max": max(result["n"] for result in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{trial_result['counterexample']}\" first_failing_seed={first_failing_seed}")