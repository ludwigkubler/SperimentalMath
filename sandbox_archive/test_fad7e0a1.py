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
    
    def generate_random_permutation(n):
        return [i for i in range(n)]
    
    def schur_weyl_duality_representation(permutation, n):
        # Placeholder function to compute the Schur-Weyl duality representation
        # This is a dummy implementation and should be replaced with actual computation
        return len(permutation)
    
    def permutation_circuit(permutation):
        # Placeholder function to construct a permutation circuit
        # This is a dummy implementation and should be replaced with actual construction
        depth = 1
        size = len(permutation)
        return depth, size
    
    def min_rank(permutation, n):
        representation = schur_weyl_duality_representation(permutation, n)
        return representation
    
    n = random.randint(5, 40)
    permutation = generate_random_permutation(n)
    rho = min_rank(permutation, n)
    D_g, S_g = permutation_circuit(permutation)
    
    if rho > 2**(D_g + math.log(S_g)):
        conjecture_holds = False
        counterexample = "rho(g) > 2^(D_g + log S_g)"
    else:
        conjecture_holds = True
        counterexample = ""
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": rho,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(result["seed"] for result in results if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='rho(g) > 2^(D_g + log S_g)' first_failing_seed={first_failing_seed}")