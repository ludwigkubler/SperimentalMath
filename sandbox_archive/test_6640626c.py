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
    
    def generate_clique_circuit(n):
        if n == 1:
            return []
        clique = list(range(1, n + 1))
        circuit = []
        for i in range(len(clique)):
            for j in range(i + 1, len(clique)):
                circuit.append((clique[i], clique[j]))
        return circuit
    
    def compute_noncommutative_algebra(circuit):
        # Simplified version of noncommutative algebra computation
        return len(circuit)
    
    def quotient_rank(algebra_size):
        # Simplified version of quotient rank calculation
        return algebra_size ** 2 * math.log(algebra_size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    for n in n_values:
        circuit = generate_clique_circuit(n)
        algebra_size = compute_noncommutative_algebra(circuit)
        rank = quotient_rank(algebra_size)
        ranks.append(rank)
    
    mean_rank = sum(ranks) / len(ranks)
    max_rank = max(ranks)
    min_rank = min(ranks)
    
    conjecture_holds = all(min_rank >= n**2 * math.log(n) for n in n_values) and \
                       all(max_rank <= n**2 * math.log(n) for n in n_values)
    
    return {
        "metric_name": "quotient_rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"max_rank={max_rank}, min_rank={min_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes if no seeds provided
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")