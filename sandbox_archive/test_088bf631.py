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
    
    def generate_branching_program(n):
        if n == 1:
            return [0]
        else:
            left = generate_branching_program(n // 2)
            right = generate_branching_program(n - len(left))
            return [left, right]
    
    def compute_hodge_rank(program):
        if not program:
            return 0
        elif isinstance(program[0], int):
            return 1
        else:
            left_rank = compute_hodge_rank(program[0])
            right_rank = compute_hodge_rank(program[1])
            return max(left_rank, right_rank) + 1
    
    def is_trivial_program(program):
        if not program:
            return True
        elif isinstance(program[0], int):
            return False
        else:
            left_is_trivial = is_trivial_program(program[0])
            right_is_trivial = is_trivial_program(program[1])
            return left_is_trivial and right_is_trivial
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        program = generate_branching_program(n)
        rank = compute_hodge_rank(program)
        ranks.append(rank)
    
    if is_trivial_program(program):
        lower_bound = 2 ** (n - 1)
        if any(rank < lower_bound for rank in ranks):
            return {
                "metric_name": "Hodge Rank",
                "metric_value": sum(ranks) / len(ranks),
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": "trivial_program_rank_too_low"
            }
    
    upper_bound = 10 * n ** 2
    if any(rank > upper_bound for rank in ranks):
        return {
            "metric_name": "Hodge Rank",
            "metric_value": sum(ranks) / len(ranks),
            "instances_tested": len(n_values),
            "conjecture_holds": False,
            "counterexample": f"rank_exceeds_upper_bound_{upper_bound}"
        }
    
    return {
        "metric_name": "Hodge Rank",
        "metric_value": sum(ranks) / len(ranks),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    total_ranks = [r['metric_value'] for r in results if r['conjecture_holds']]
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(total_ranks) / len(total_ranks)} std={math.sqrt(sum((x - (sum(total_ranks) / len(total_ranks))) ** 2 for x in total_ranks) / len(total_ranks))} support_fraction={support_fraction}")
    elif any(not r['conjecture_holds'] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank_exceeds_upper_bound\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")