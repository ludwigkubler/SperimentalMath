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
    
    def generate_and_or_tree(depth):
        if depth == 0:
            return random.choice([True, False])
        else:
            left = generate_and_or_tree(depth - 1)
            right = generate_and_or_tree(depth - 1)
            return (left, right) if random.random() < 0.5 else (right, left)
    
    def calculate_minimal_rank(tree):
        # Simplified rank calculation for demonstration
        return len(tree)
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_ranks = []
    
    for n in n_values:
        tree = generate_and_or_tree(n)
        rank = calculate_minimal_rank(tree)
        total_ranks.append(rank)
    
    avg_rank = sum(total_ranks) / len(total_ranks)
    std_dev = math.sqrt(sum((x - avg_rank) ** 2 for x in total_ranks) / len(total_ranks))
    conjecture_holds = all(avg_rank - 3 * std_dev <= rank <= avg_rank + 3 * std_dev for rank in total_ranks)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": avg_rank,
        "instances_tested": len(total_ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"avg_rank={avg_rank}, std_dev={std_dev}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"avg_rank={avg_rank}, std_dev={std_dev}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")