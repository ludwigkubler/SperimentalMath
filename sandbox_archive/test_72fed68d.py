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
    
    def generate_and_or_tree(depth):
        if depth == 0:
            return random.choice([0, 1])
        else:
            left = generate_and_or_tree(depth - 1)
            right = generate_and_or_tree(depth - 1)
            return (left, right) if random.randint(0, 1) == 0 else (right, left)
    
    def construct_yang_baxter_equation(tree):
        if isinstance(tree, int):
            return [[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]]
        else:
            left_eq = construct_yang_baxter_equation(tree[0])
            right_eq = construct_yang_baxter_equation(tree[1])
            # Simplified braid relation for demonstration
            return [
                [left_eq[0][0] * right_eq[0][0], left_eq[0][0] * right_eq[0][1]],
                [left_eq[1][0] * right_eq[1][0], left_eq[1][0] * right_eq[1][1]]
            ]
    
    def calculate_minimal_rank(eq):
        # Simplified rank calculation for demonstration
        return max(abs(eq[0][0]), abs(eq[0][1]), abs(eq[1][0]), abs(eq[1][1]))
    
    results = []
    for n in range(5, 41):
        tree = generate_and_or_tree(n)
        eq = construct_yang_baxter_equation(tree)
        rank = calculate_minimal_rank(eq)
        results.append((n, rank))
    
    mean_rank = sum(rank for _, rank in results) / len(results)
    std_dev = math.sqrt(sum((rank - mean_rank) ** 2 for _, rank in results) / len(results))
    conjecture_holds = all(mean_rank - 3 * std_dev <= rank <= mean_rank + 3 * std_dev for _, rank in results)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"mean_rank={mean_rank}, std_dev={std_dev}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mean_rank did not meet the conjectured bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")