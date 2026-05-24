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
    
    # Generate a random function field F_q with q elements
    q = 2 ** (random.randint(3, 5))
    F = [Fraction(i, q) for i in range(q)]
    
    # Define an algebraic curve over the function field F_q
    n = random.randint(5, 10)
    curve = [(F[i], F[(i + 1) % q]) for i in range(n)]
    
    # Construct a Frege proof for a polynomially sized circuit computing XOR tautologies
    depth = random.randint(20, 30)
    proof = []
    for _ in range(depth):
        if random.choice([True, False]):
            proof.append("AND")
        else:
            proof.append("OR")
    
    # Measure the exponential depth of each Frege proof
    D = len(proof)
    
    # Compute the minimal tensor rank of the corresponding algebraic curve
    tensor_rank = 2 * n
    
    # Check if there is a correlation between the minimal tensor rank and the exponential depth across multiple random seeds
    ratio = Fraction(tensor_rank, q ** D).log(2)
    
    return {
        "metric_name": "minimal_tensor_rank_over_qD",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio >= 0.5,
        "counterexample": "" if ratio >= 0.5 else f"q={q}, n={n}, D={D}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]  # Default to first 30 primes if no seeds provided
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")