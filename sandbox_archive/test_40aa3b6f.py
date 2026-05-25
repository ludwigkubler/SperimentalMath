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
    
    def generate_monotone_circuit(n):
        circuit = [False] * n
        for i in range(1, n-1):
            if random.choice([True, False]):
                circuit[i] = True
        return circuit
    
    def is_monotone(circuit):
        n = len(circuit)
        for i in range(1, n-1):
            if circuit[i] and not (circuit[i-1] or circuit[i+1]):
                return False
        return True
    
    def construct_matroid_representation(circuit):
        matroid = []
        for i in range(len(circuit)):
            if circuit[i]:
                matroid.append([i])
        return matroid
    
    def compute_rank(matroid):
        rank = 0
        bases = [set(b) for b in matroid]
        while bases:
            base = bases.pop()
            rank += 1
            new_bases = []
            for nb in bases:
                if not nb.issubset(base):
                    new_bases.append(nb)
            bases = new_bases
        return rank
    
    n = random.randint(5, 40)
    circuit = generate_monotone_circuit(n)
    
    if not is_monotone(circuit):
        return {
            "metric_name": "Rank of Generalized Matroid",
            "metric_value": 0.0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Non-monotone circuit"
        }
    
    matroid = construct_matroid_representation(circuit)
    rank = compute_rank(matroid)
    
    return {
        "metric_name": "Rank of Generalized Matroid",
        "metric_value": rank / n**(1/4),
        "instances_tested": 1,
        "conjecture_holds": rank >= 0.5 * n**(1/4) and rank / n**(1/4) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-monotone circuit\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")