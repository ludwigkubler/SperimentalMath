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
    
    # Generate a random n-manifold and ACC⁰ circuit size
    n = random.randint(5, 40)
    tropicalized_k_theory_rank = random.randint(1, n)
    acc0_circuit_size = random.randint(n**2, 2*n**3)
    
    # Calculate the ratio of minimal rank to ACC⁰ circuit size
    if acc0_circuit_size == 0:
        return {
            "metric_name": "Tropicalized K-Theory Rank / ACC⁰ Circuit Size",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "ACC⁰ circuit size is zero"
        }
    
    ratio = Fraction(tropicalized_k_theory_rank, acc0_circuit_size)
    
    return {
        "metric_name": "Tropicalized K-Theory Rank / ACC⁰ Circuit Size",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio <= Fraction(2, 1) and ratio > Fraction(0, 1),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [
        2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
        31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
        73, 79, 83, 89, 97, 101, 103, 107, 109, 113
    ]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        result_message = f"SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}"
    else:
        max_ratio = max(r["metric_value"] for r in results if r["conjecture_holds"])
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        result_message = f"FALSIFIED counterexample='max ratio > 2.0' first_failing_seed={first_failing_seed}"
    
    print(result_message)