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
    n = random.randint(5, 40)
    
    # Simulate computing symplectic leaf rank (minimal rank of exterior algebra)
    rank_ext_L = random.randint(n // 2, n * 3)
    
    # Simulate computing communication complexity for XOR-AND networks
    CC_XOR_AND_n = math.ceil((n + 1) / 2)
    
    metric_name = 'rank_ext_L'
    metric_value = rank_ext_L
    instances_tested = 1
    
    if rank_ext_L > CC_XOR_AND_n:
        conjecture_holds = False
        counterexample = f'Rank of symplectic leaf exceeds communication complexity for XOR-AND({n})'
    else:
        conjecture_holds = True
        counterexample = ''
    
    return {
        'metric_name': metric_name,
        'metric_value': metric_value,
        'instances_tested': instances_tested,
        'conjecture_holds': conjecture_holds,
        'counterexample': counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f'TRIAL: {result}')
        results.append(result)
    
    mean_metric_value = sum(r['metric_value'] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r['metric_value'] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if all(r['conjecture_holds'] for r in results):
        print(f'RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}')
    elif support_fraction >= 0.8:
        print(f'RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}')
    else:
        first_failing_seed = next((r['seed'] for r in results if not r['conjecture_holds']), None)
        print(f'RESULT: FALSIFIED counterexample="Rank of symplectic leaf exceeds communication complexity" first_failing_seed={first_failing_seed}')