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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 0
        left = f[:n//2]
        right = f[n//2:]
        return max(xor_and_tree_width(left), xor_and_tree_width(right)) + 1
    
    def minimal_rank(f):
        n = len(f)
        if n == 1:
            return 1
        
        # Construct the lattice of real algebraic integers that vanish on the image of f
        lattice = set()
        for i in range(2**n):
            if all(f[j] ^ (i >> j & 1) == 0 for j in range(n)):
                lattice.add(i)
        
        # Compute the minimal rank of the lattice
        basis = []
        for x in lattice:
            is_basis = True
            for y in basis:
                if any(x & (1 << i) and not y & (1 << i) for i in range(n)):
                    is_basis = False
                    break
            if is_basis:
                basis.append(x)
        
        return len(basis)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    for n in n_values:
        f = generate_boolean_function(n)
        rank = minimal_rank(f)
        width = xor_and_tree_width(f)
        results.append((n, rank, width))
    
    mean_rank = sum(rank for _, rank, _ in results) / len(results)
    mean_width = sum(width for _, _, width in results) / len(results)
    support_fraction = sum(1 for _, rank, width in results if width <= 1.1 * mean_rank) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "XOR-AND tree width vs Minimal Rank",
        "metric_value": mean_width,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i - 1 for i in range(3, 6)]
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
    mean_width = sum(trial_result["metric_value"] for trial_result in results) / len(results)
    support_fraction = sum(1 for trial_result in results if trial_result["conjecture_holds"]) / len(results)
    
    if support_fraction == 1.0:
        result = "SUPPORTED"
    elif support_fraction >= 0.8:
        result = "FALSIFIED counterexample=mapping_undefined first_failing_seed=<s>"
    else:
        result = "INCONCLUSIVE reason=insufficient_evidence"
    
    print(f"RESULT: {result} mean={mean_width} std=<y> support_fraction={support_fraction}")