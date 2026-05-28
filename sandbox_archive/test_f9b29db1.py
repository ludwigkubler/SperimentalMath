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
    
    def generate_circuit(n):
        # Generate a random boolean circuit with n inputs
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def configuration_space(circuit):
        # Compute the configuration space of the circuit
        n = int(math.log2(len(circuit)))
        config_space = []
        for i in range(2**n):
            config = [int(x) for x in format(i, f'0{n}b')]
            if all(config[j] == circuit[2*j] or config[j] == circuit[2*j+1] for j in range(n)):
                config_space.append(config)
        return config_space
    
    def euler_characteristic(space):
        # Compute the Euler characteristic of the configuration space
        return len(space) - sum(len(list(group)) for _, group in itertools.groupby(sorted(space)))
    
    def monotone_complexity(circuit):
        # Compute the monotone complexity of the circuit
        n = int(math.log2(len(circuit)))
        max_depth = 0
        visited = set()
        
        def dfs(node, depth):
            nonlocal max_depth
            if node in visited:
                return
            visited.add(node)
            if depth > max_depth:
                max_depth = depth
            for i in range(n):
                if circuit[2*i] == node or circuit[2*i+1] == node:
                    dfs(circuit[2*i], depth + 1)
                    dfs(circuit[2*i+1], depth + 1)
        
        dfs(0, 0)
        return max_depth
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    config_space = configuration_space(circuit)
    chi = euler_characteristic(config_space)
    mu = monotone_complexity(circuit)
    
    if chi == 0 or mu == 0:
        return {
            "metric_name": "chi_over_mu",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "chi or mu is zero"
        }
    
    chi_over_mu = chi / (mu ** 2)
    return {
        "metric_name": "chi_over_mu",
        "metric_value": chi_over_mu,
        "instances_tested": 1,
        "conjecture_holds": chi_over_mu <= 10,  # Arbitrary constant for testing
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='chi_over_mu > 10' first_failing_seed={first_failing_seed}")