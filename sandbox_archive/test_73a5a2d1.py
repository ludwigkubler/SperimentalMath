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
    
    def generate_protocol(n):
        # Generate a random n-communication protocol with known communication complexity rank r(P) ≤ 40
        return [random.randint(1, 40) for _ in range(n)]
    
    def construct_vector_bundle(protocol):
        # Construct the associated vector bundle E and compute its minimal index
        n = len(protocol)
        E = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i, n):
                E[i][j] = protocol[j]
                E[j][i] = protocol[i]
        return E
    
    def min_index(E):
        # Compute the minimal index of the vector bundle E
        n = len(E)
        count = 0
        for i in range(n):
            if all(E[i][j] == 0 for j in range(i + 1, n)):
                count += 1
        return count
    
    def communication_complexity_rank(protocol):
        # Compute the communication complexity rank r(P) of the protocol
        return sum(protocol)
    
    n = random.randint(5, 40)
    protocol = generate_protocol(n)
    E = construct_vector_bundle(protocol)
    index_E = min_index(E)
    r_P = communication_complexity_rank(protocol)
    
    metric_name = 'minimal_index'
    metric_value = index_E
    instances_tested = 1
    n_max = n
    conjecture_holds = (1.5 <= index_E / r_P <= 2)
    counterexample = f'Protocol with n={n}, index(E)={index_E}, r(P)={r_P}' if not conjecture_holds else ''
    
    return {
        'metric_name': metric_name,
        'metric_value': metric_value,
        'instances_tested': instances_tested,
        'n_max': n_max,
        'conjecture_holds': conjecture_holds,
        'counterexample': counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 997) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {result}')
        results.append(result)
    
    mean_value = sum(result['metric_value'] for result in results) / len(results)
    std_value = math.sqrt(sum((result['metric_value'] - mean_value) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result['conjecture_holds']) / len(results)
    
    if all(result['conjecture_holds'] for result in results):
        print(f'RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}')
    elif any(not result['conjecture_holds'] for result in results):
        first_failing_seed = next((result["seed"] for result in results if not result["conjecture_holds"]), None)
        print(f'RESULT: FALSIFIED counterexample="{results[first_failing_seed]["counterexample"]}" first_failing_seed={first_failing_seed}')
    else:
        print('RESULT: INCONCLUSIVE reason=unknown')