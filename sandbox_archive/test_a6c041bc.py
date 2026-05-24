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
    
    # Generate a random Boolean circuit of size s and depth d
    n = 20  # Number of variables
    s = random.randint(5, 30)  # Size of the circuit
    d = random.randint(5, 10)  # Depth of the circuit
    
    # Create a random AND-OR tree with given depth and size
    def generate_tree(depth, size):
        if depth == 1:
            return [random.choice([0, 1])]
        else:
            children = []
            for _ in range(size):
                child_depth = random.randint(1, depth - 1)
                child_size = random.randint(1, size)
                children.append(generate_tree(child_depth, child_size))
            return ['AND'] + children
    
    tree = generate_tree(d, s)
    
    # Convert the AND-OR tree to a tropicalized affine scheme
    def convert_to_scheme(tree):
        if isinstance(tree, int):
            return [tree]
        elif tree[0] == 'AND':
            return [1] * len(tree[1:])
        else:
            raise ValueError("Invalid tree structure")
    
    A = convert_to_scheme(tree)
    
    # Calculate the rank of the tropicalized affine scheme
    def rank(A):
        m, n = len(A), len(A[0])
        for i in range(m):
            if sum(A[i]) == 0:
                return 0
        return min(m, n)
    
    r_A = rank(A)
    
    # Store the results
    result = {
        "metric_name": "Rank of Tropicalized Affine Scheme",
        "metric_value": r_A,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": ""
    }
    
    # Check if the conjecture holds for this seed
    if s >= 5 and d >= 5:
        if r_A <= math.sqrt(s):
            result["conjecture_holds"] = True
    
    return result

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]]
    if not seeds:
        seeds = [2**i - 1 for i in range(5, 30)]  # First 25 primes
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_r_A = sum(r["metric_value"] for r in results) / len(results)
    std_r_A = math.sqrt(sum((r["metric_value"] - mean_r_A)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_r_A} std={std_r_A} support_fraction={support_fraction}")
    elif support_fraction >= 0.95:
        print(f"RESULT: SUPPORTED mean={mean_r_A} std={std_r_A} support_fraction={support_fraction}")
    else:
        for r in results:
            if not r["conjecture_holds"]:
                counterexample = f"Seed {r['seed']}: Rank {r['metric_value']} does not satisfy the conjecture"
                print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={r['seed']}")
                break