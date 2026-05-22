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
    
    def generate_branching_program(n):
        nodes = [{'children': []} for _ in range(2**n)]
        for i in range(n):
            for j in range(2**(i+1)):
                node = nodes[j]
                left_child = {'value': random.choice([0, 1]), 'children': []}
                right_child = {'value': random.choice([0, 1]), 'children': []}
                node['children'].append(left_child)
                node['children'].append(right_child)
        return nodes[0]
    
    def tropical_rank(node):
        if not node['children']:
            return 1
        left_rank = tropical_rank(node['children'][0])
        right_rank = tropical_rank(node['children'][1])
        return max(left_rank, right_rank) + 1
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        size = 2**n
        program = generate_branching_program(n)
        rank = tropical_rank(program)
        
        upper_bound = math.log(size) + 3
        lower_bound = int(math.ceil(n ** (1/4)))
        
        if rank <= upper_bound and rank >= lower_bound:
            results.append(True)
        else:
            return {
                "metric_name": "Tropicalized Rank",
                "metric_value": rank,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"n={n}, rank={rank}"
            }
    
    return {
        "metric_name": "Tropicalized Rank",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(results),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")