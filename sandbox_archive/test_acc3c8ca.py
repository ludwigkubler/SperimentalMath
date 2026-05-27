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
            return '0'
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return f'({left},{right})'

    def alexander_module(circuit):
        if circuit == '0':
            return [1]
        elif circuit == '1':
            return [-1, 1]
        else:
            left, right = circuit.split(', ')
            A_left = alexander_module(left)
            A_right = alexander_module(right)
            n = len(A_left) + len(A_right) - 2
            A = [0] * (n + 1)
            for i in range(len(A_left)):
                for j in range(len(A_right)):
                    A[i + j] += A_left[i] * A_right[j]
            return A

    n = random.randint(5, 40)
    circuit = generate_circuit(n)
    A = alexander_module(circuit)
    min_rank = max(abs(x) for x in A if x != 0)

    f_n = math.log2(n + 1)
    metric_value = abs(min_rank - f_n)
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": metric_value,
        "instances_tested": 1,
        "conjecture_holds": metric_value <= 3,
        "counterexample": "" if metric_value <= 3 else f"n={n}, min_rank={min_rank}, f(n)={f_n}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or list(range(2, 160, 5))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value:.4f} std={std_metric_value:.4f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results) and support_fraction >= 0.8:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={first_failing_seed}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f}")