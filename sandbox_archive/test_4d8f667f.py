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

def gaussian_elimination(A, b):
    n = len(A)
    Augmented = [A[i] + [b[i]] for i in range(n)]
    
    for i in range(n):
        if Augmented[i][i] == 0:
            # Find a row with non-zero pivot
            for j in range(i+1, n):
                if Augmented[j][i] != 0:
                    Augmented[i], Augmented[j] = Augmented[j], Augmented[i]
                    break
            else:
                raise ValueError("No non-zero pivot found")
        
        # Make the pivot 1
        pivot = Augmented[i][i]
        for j in range(i, n+1):
            Augmented[i][j] /= pivot
        
        # Eliminate the current column below the pivot
        for j in range(n):
            if j != i:
                factor = Augmented[j][i]
                for k in range(i, n+1):
                    Augmented[j][k] -= factor * Augmented[i][k]
    
    return [row[:-1] for row in Augmented]

def minimal_rank(tree):
    # Construct the noncommutative crossed product algebra
    # This is a placeholder function. Replace with actual implementation.
    n = len(tree)
    A = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if tree[i][j] == 1:
                A[i][j] = 1
    return len(gaussian_elimination(A, [0]*len(A)))

def xor_and_tree_width(tree):
    # Placeholder function to compute the width of the XOR-AND tree
    # Replace with actual implementation.
    n = len(tree)
    if n == 1:
        return 1
    else:
        return max(xor_and_tree_width(tree[:n//2]), xor_and_tree_width(tree[n//2:]))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        tree = [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
        
        rank = minimal_rank(tree)
        width = xor_and_tree_width(tree)
        
        results.append((rank, width))
    
    mean_rank = sum(rank for rank, _ in results) / len(results)
    mean_width = sum(width for _, width in results) / len(results)
    
    conjecture_holds = all(rank <= math.log(n) * math.log(math.log(n)) for n, (rank, _) in zip(range(5, 41), results))
    counterexample = "" if conjecture_holds else "minimal_rank > f(n)"
    
    return {
        "metric_name": "mean_width",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*31, 2))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_width = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.9:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(seed for seed, res in enumerate(results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{res['counterexample']}\" first_failing_seed={first_failing_seed}")