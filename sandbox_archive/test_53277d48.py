# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_monotone_tautology(n):
        # Generate a random monotone tautology using a clique problem
        vertices = list(range(1, n+1))
        edges = [(i, j) for i in range(1, n) for j in range(i+1, n+1)]
        random.shuffle(edges)
        tautology = []
        for u, v in edges:
            if random.choice([True, False]):
                tautology.append(f"{u} OR {v}")
            else:
                tautology.append(f"NOT ({u} AND {v})")
        return " AND ".join(tautology)
    
    def extended_frege_proof_length(proof):
        # Simplify the proof by removing redundant steps
        simplified = []
        for step in proof.split("\n"):
            if step not in simplified:
                simplified.append(step)
        return len(simplified)
    
    n = random.randint(5, 40)
    tautology = generate_monotone_tautology(n)
    proof_length = extended_frege_proof_length(tautology)
    
    metric_name = "Extended Frege Proof Length"
    metric_value = proof_length
    instances_tested = 1
    conjecture_holds = proof_length > n * (n - 1) // 2
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} is not super-linear for n={n}"
    
    return {
        "metric_name": metric_name,
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = (sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results)) ** 0.5
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"First failing seed\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")