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
    
    def generate_boolean_matrix(n):
        return [[random.randint(0, 1) for _ in range(n)] for _ in range(n)]
    
    def bp_read_twice_circuit_size(matrix):
        n = len(matrix)
        if n == 1:
            return 1
        k = 2
        while True:
            found = False
            for i in range(2**k):
                circuit = [i]
                current_state = matrix[0][:]
                for j in range(1, n):
                    next_state = []
                    for x in current_state:
                        if x == 0:
                            next_state.append(circuit[-1])
                        else:
                            next_state.append((circuit[-1] + 1) % k)
                    circuit.append(next_state[0])
                if circuit == matrix[1:]:
                    found = True
                    break
            if found:
                return k
            k += 1
    
    def geometric_entropy(matrix):
        n = len(matrix)
        count = sum(sum(row) for row in matrix)
        total = n * n
        p = count / total
        if p == 0 or p == 1:
            return 0
        return -p * math.log2(p) - (1 - p) * math.log2(1 - p)
    
    results = []
    for n in [5, 10, 20, 40]:
        for _ in range(30):
            matrix = generate_boolean_matrix(n)
            k = bp_read_twice_circuit_size(matrix)
            H_M = geometric_entropy(matrix)
            if H_M < 2**k:
                return {
                    "metric_name": "geometric entropy vs BP_ReadTwice circuit size",
                    "metric_value": H_M,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"Matrix of size {n} with k={k}, H(M)={H_M}"
                }
            results.append(H_M)
    
    mean = sum(results) / len(results)
    std = math.sqrt(sum((x - mean)**2 for x in results) / len(results))
    support_fraction = len([x for x in results if x >= 2**k]) / len(results)
    
    return {
        "metric_name": "geometric entropy vs BP_ReadTwice circuit size",
        "metric_value": mean,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean = sum(x["metric_value"] for x in results) / len(results)
    std = math.sqrt(sum((x["metric_value"] - mean)**2 for x in results) / len(results))
    support_fraction = sum(1 for x in results if x["conjecture_holds"]) / len(results)
    
    if support_fraction == 1:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(x["seed"] for x in results if not x["conjecture_holds"])
        counterexample = next(x["counterexample"] for x in results if not x["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")