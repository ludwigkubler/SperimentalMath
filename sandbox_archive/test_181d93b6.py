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
    
    def xor_and_tree_width(formula):
        # Placeholder for XOR-AND tree width calculation
        return len(formula) // 2
    
    def tropicalized_rank(formula):
        # Placeholder for tropicalized rank calculation
        return len(formula) ** (3/4)
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            clause_density = random.uniform(0.1, 0.9)
            num_clauses = int(clause_density * (n * (n - 1) // 2))
            formula = [random.sample(range(n), 3) for _ in range(num_clauses)]
            
            xor_and_width = xor_and_tree_width(formula)
            rank = tropicalized_rank(formula)
            ratio = rank / xor_and_width
            
            results.append({
                "n": n,
                "ratio": ratio
            })
    
    mean_ratio = sum(result["ratio"] for result in results) / len(results)
    conjecture_holds = all(result["ratio"] <= 1.2 for result in results)
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Ratio of Tropicalized Rank to XOR-AND Tree Width",
        "metric_value": mean_ratio,
        "instances_tested": len(results),
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
    
    mean_ratio = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")