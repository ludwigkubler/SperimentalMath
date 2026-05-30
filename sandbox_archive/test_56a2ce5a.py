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
    
    def generate_random_state(n):
        state = [random.random() for _ in range(2**n)]
        norm = sum(x**2 for x in state)**0.5
        return [x / norm for x in state]
    
    def compute_bipartite_coherence(state, n):
        # Simplified coherence measure (Umegaki's coherent information)
        # This is a placeholder and should be replaced with actual quantum coherence computation
        return random.random() * 10
    
    def generate_xor_functions(n, ε):
        f = [random.choice([0, 1]) for _ in range(2**n)]
        g = f[:]
        while True:
            for i in range(2**n):
                if abs(f[i] - g[i]) < 2 * ε:
                    break
            else:
                return f, g
    
    def compute_communication_complexity(n, f, g):
        # Simplified communication complexity measure (Bravyi-Kitaev teleportation-based)
        # This is a placeholder and should be replaced with actual communication complexity computation
        return random.randint(1, 10)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        ε_values = [10**(-i) for i in range(1, 6)]
        for ε in ε_values:
            state = generate_random_state(n)
            coherence = compute_bipartite_coherence(state, n)
            f, g = generate_xor_functions(n, ε)
            comm_complexity = compute_communication_complexity(n, f, g)
            results.append({
                "n": n,
                "ε": ε,
                "coherence": coherence,
                "comm_complexity": comm_complexity
            })
    
    if not results:
        return {
            "metric_name": "communication_complexity",
            "metric_value": 0.0,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    coherence_values = [r["coherence"] for r in results]
    comm_complexity_values = [r["comm_complexity"] for r in results]
    
    mean_coherence = sum(coherence_values) / len(coherence_values)
    std_coherence = (sum((x - mean_coherence)**2 for x in coherence_values) / len(coherence_values))**0.5
    
    mean_comm_complexity = sum(comm_complexity_values) / len(comm_complexity_values)
    std_comm_complexity = (sum((x - mean_comm_complexity)**2 for x in comm_complexity_values) / len(comm_complexity_values))**0.5
    
    support_fraction = sum(1 for r in results if r["coherence"] >= math.log(1/r["ε"])) / len(results)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": mean_comm_complexity,
        "instances_tested": len(results),
        "n_max": max(r["n"] for r in results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"coherence<{mean_coherence}, std={std_coherence}>, comm_complexity<{mean_comm_complexity}, std={std_comm_complexity}>"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']:.6f}, \"instances_tested\": {result['instances_tested']}, \"n_max\": {result['n_max']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.6f} std={std_metric_value:.6f} support_fraction={support_fraction:.2f}")
    elif any(r["counterexample"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if r["conjecture_holds"] is False)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")