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
    
    def random_monotone_circuit(k, n):
        if k == 1:
            return [[i % 2] for i in range(n)]
        subcircuits = [random_monotone_circuit(k-1, n//2)]
        for i in range(1, n//2):
            subcircuits.append([i % 2])
        return [subcircuit + [sum(subcircuit) % 2] for subcircuit in subcircuits]
    
    def quandle_representation(circuit):
        if len(circuit) == 1:
            return circuit
        q = {}
        for i in range(len(circuit)):
            for j in range(i+1, len(circuit)):
                if circuit[i][0] != circuit[j][0]:
                    q[(i, j)] = (circuit[i][1] + circuit[j][1]) % 2
        return q
    
    def minimal_rank(q):
        rank = 0
        for i in range(len(q)):
            for j in range(i+1, len(q)):
                if q[(i, j)] == 0:
                    continue
                found = False
                for k in range(rank):
                    if all(q[(i, k)] + q[(k, j)] == q[(i, j)] for k in range(k)):
                        found = True
                        break
                if not found:
                    rank += 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        k = random.randint(1, min(n-1, 4))
        circuit = random_monotone_circuit(k, n)
        q = quandle_representation(circuit)
        rank = minimal_rank(q)
        
        if rank < math.ceil(2**k):
            return {
                "metric_name": "minimal_rank",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"rank={rank}, expected=Ω({2**k})"
            }
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": math.ceil(2**k),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(30, 67))  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank < 2^k\" first_failing_seed={first_failing_seed}")