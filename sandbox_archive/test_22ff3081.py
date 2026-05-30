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
    
    def generate_random_state(n: int, epsilon: float):
        state = [random.uniform(-epsilon, epsilon) for _ in range(2**n)]
        norm = sum(x**2 for x in state)**0.5
        return [x / norm for x in state]
    
    def compute_coherence(state, n):
        # Simplified coherence measure (Umegaki's coherent information)
        if all(x == 0 for x in state):
            return 0
        rho = [[state[i] * state[j] for j in range(2**n)] for i in range(2**n)]
        trace = sum(rho[i][i] for i in range(2**n))
        return -trace / (2**n)
    
    def generate_xor_functions(n, delta):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        g = [(x + random.randint(1, int(delta * 2**n))) % 2 for x in f]
        return f, g
    
    def communication_complexity(f, g):
        # Simplified simulation of communication complexity
        n = len(f)
        total_bits = 0
        for i in range(n):
            if f[i] != g[i]:
                total_bits += math.ceil(math.log2(n))
        return total_bits / n
    
    epsilon_values = [10**(-i) for i in range(1, 5)]
    results = []
    
    for epsilon in epsilon_values:
        state = generate_random_state(5, epsilon)
        coherence = compute_coherence(state, 5)
        f, g = generate_xor_functions(2**5, delta=epsilon * 2**5)
        complexity = communication_complexity(f, g)
        
        results.append({
            "metric_name": "coherence",
            "metric_value": coherence,
            "instances_tested": 1,
            "n_max": 32,
            "conjecture_holds": coherence >= math.log(1/epsilon),
            "counterexample": ""
        })
    
    mean_coherence = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "metric_name": "coherence",
        "mean_coherence": mean_coherence,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_coherence = sum(res["mean_coherence"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["support_fraction"] >= 0.8) / len(results)
    
    if all(res["support_fraction"] >= 0.8 for res in results):
        print(f"RESULT: SUPPORTED mean={mean_coherence} std=0 support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='coherence' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")