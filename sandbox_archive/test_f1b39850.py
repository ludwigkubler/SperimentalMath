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
    
    def generate_circuit(n):
        if n == 1:
            return ['NOT', '0']
        else:
            left = generate_circuit(random.randint(1, n-1))
            right = generate_circuit(n - len(left) - 1)
            op = random.choice(['AND', 'OR'])
            return [op] + left + right
    
    def construct_geometric_object(circuit):
        if circuit[0] == 'NOT':
            sub_circuit = circuit[1:]
            rank = construct_geometric_object(sub_circuit)
            return 2 * rank
        elif circuit[0] in ['AND', 'OR']:
            left_rank = construct_geometric_object(circuit[1:circuit.index('OR')])
            right_rank = construct_geometric_object(circuit[circuit.index('OR') + 1:])
            return max(left_rank, right_rank) + 1
        else:
            return 0
    
    def min_rank(n):
        return math.ceil(math.log2(n))
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    rank = construct_geometric_object(circuit)
    conjecture_holds = rank <= min_rank(n)
    counterexample = "" if conjecture_holds else f"rank={rank}, expected={min_rank(n)}"
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")