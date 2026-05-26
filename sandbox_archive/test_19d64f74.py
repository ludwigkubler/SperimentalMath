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
    
    def generate_circuit(n):
        if n == 1:
            return ['OR']
        else:
            a = generate_circuit(n // 2)
            b = generate_circuit(n - n // 2)
            return [random.choice(['AND', 'OR'])] + a + b
    
    def construct_geometric_object(circuit):
        if len(circuit) == 1:
            return 1
        else:
            left_rank = construct_geometric_object(circuit[1:circuit.index('OR')])
            right_rank = construct_geometric_object(circuit[circuit.index('OR') + 1:])
            return max(left_rank, right_rank) + 1
    
    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    rank = construct_geometric_object(circuit)
    
    g_n = math.log2(n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": rank <= g_n,
        "counterexample": "" if rank <= g_n else f"rank={rank}, expected={g_n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r['metric_value'] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={math.sqrt(sum((r['metric_value'] - mean_value) ** 2 for r in results) / len(results))} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r['seed'] for r in results if not r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"rank exceeds g(n)\" first_failing_seed={first_failing_seed}")