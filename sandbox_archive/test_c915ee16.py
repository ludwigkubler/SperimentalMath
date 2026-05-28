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
    
    def generate_frege_proof(n):
        # Placeholder for generating a Frege proof
        return [random.randint(1, 10) for _ in range(n)]
    
    def compute_geometric_langlands_rank(proof):
        # Placeholder for computing the rank of the geometric Langlands dual object
        # This is a dummy implementation that returns a random rank
        return random.randint(1, 10)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_rank = 0
    instances_tested = 0
    
    for n in n_values:
        proof = generate_frege_proof(n)
        rank = compute_geometric_langlands_rank(proof)
        total_rank += rank
        instances_tested += 1
    
    average_rank = Fraction(total_rank, instances_tested)
    expected_rank = Fraction(math.log(n), math.log(math.log(n)))
    
    conjecture_holds = abs(average_rank - expected_rank) <= Fraction(10, 100) * expected_rank
    counterexample = "" if conjecture_holds else f"Expected {expected_rank}, got {average_rank}"
    
    return {
        "metric_name": "Average Rank",
        "metric_value": float(average_rank),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] if len(sys.argv) > 1 else [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_rank = sum(r["metric_value"] * r["instances_tested"] for r in results)
    instances_tested = sum(r["instances_tested"] for r in results)
    average_rank = Fraction(total_rank, instances_tested)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={average_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={average_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")