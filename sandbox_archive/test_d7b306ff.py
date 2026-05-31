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
    
    def generate_random_boolean_function(n):
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def compute_tropical_curve(f):
        q = 2
        n = len(f)
        T_f = [[0] * (n + 1) for _ in range(n + 1)]
        for i in range(n):
            for j in range(n):
                if f[i] == f[j]:
                    T_f[i][j] = 0
                else:
                    T_f[i][j] = math.inf
        return T_f
    
    def minimal_local_index(T_f):
        n = len(T_f) - 1
        mli = 0
        for i in range(n):
            for j in range(i + 1, n + 1):
                if T_f[i][j] < math.inf:
                    mli += 1
        return mli
    
    def communication_complexity(f):
        n = len(f)
        C_f = 0
        for i in range(2**n):
            binary_i = format(i, f'0{n}b')
            count_1s = binary_i.count('1')
            if f[i] == 1:
                C_f += count_1s
        return C_f
    
    n = random.randint(5, 40)
    f = generate_random_boolean_function(n)
    T_f = compute_tropical_curve(f)
    mli = minimal_local_index(T_f)
    C_f = communication_complexity(f)
    
    return {
        "metric_name": "mli_vs_C",
        "metric_value": mli / C_f,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": abs(mli - C_f) <= 3,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    if all(result["conjecture_holds"] for result in results):
        support_fraction = len([result for result in results if result["conjecture_holds"]]) / len(results)
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={sum(result['metric_value'] for result in results) / len(results)} std=0 support_fraction={support_fraction}")
        else:
            print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mli(C(f)) not within 3 of C(f)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported the conjecture")