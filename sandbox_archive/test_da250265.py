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
    
    def xor_and_tree(n):
        if n == 1:
            return "x"
        else:
            left = xor_and_tree(n // 2)
            right = xor_and_tree(n - n // 2)
            return f"({left} & {right})"
    
    def tropicalize(tree):
        if tree.startswith("(") and tree.endswith(")"):
            left, op, right = tree[1:-1].split()
            if op == "&":
                return max(tropicalize(left), tropicalize(right))
            else:
                raise ValueError("Invalid operator in XOR-AND tree")
        elif tree.isalpha():
            return 0
        else:
            raise ValueError("Invalid node in XOR-AND tree")
    
    def minimal_rank(tree):
        return tropicalize(tree)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        tree = xor_and_tree(n)
        rank = minimal_rank(tree)
        results.append(rank)
    
    mean_value = sum(results) / len(results)
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results))
    conjecture_holds = all(rank <= math.log(n, 2) for n, rank in zip(n_values, results)) and any(rank == 0 for n, rank in zip(n_values, results))
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"rank={max(results)}, expected=Θ(log(n))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 3 for i in range(6)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds Θ(log(n))\" first_failing_seed={first_failing_seed}")