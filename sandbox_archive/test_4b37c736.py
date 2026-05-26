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
    
    def generate_read_twice_branching_program(n):
        if n == 1:
            return ['constant']
        else:
            left = generate_read_twice_branching_program(n // 2)
            right = generate_read_twice_branching_program(n - n // 2)
            return [f'if {i} then {left[i]} else {right[i]}' for i in range(n)]
    
    def compute_hodge_theoretic_motive_size(program):
        if program == 'constant':
            return 1
        elif isinstance(program, list):
            return sum(compute_hodge_theoretic_motive_size(subprogram) for subprogram in program)
        else:
            raise ValueError("Invalid program structure")
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            program = generate_read_twice_branching_program(n)
            rank = compute_hodge_theoretic_motive_size(program)
            ranks.append(rank)
    
    if not ranks:
        return {
            "metric_name": "Hodge motive rank",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "empty_rank_list"
        }
    
    mean_rank = sum(ranks) / len(ranks)
    std_dev = math.sqrt(sum((x - mean_rank) ** 2 for x in ranks) / len(ranks))
    
    return {
        "metric_name": "Hodge motive rank",
        "metric_value": mean_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": all(rank <= n**3 for n, rank in zip(n_values, ranks)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_rank = sum(r['metric_value'] for r in results if r['metric_value'] is not None) / len(results)
    std_dev = math.sqrt(sum((r['metric_value'] - mean_rank) ** 2 for r in results if r['metric_value'] is not None) / len(results))
    
    support_fraction = sum(r['conjecture_holds'] for r in results) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")