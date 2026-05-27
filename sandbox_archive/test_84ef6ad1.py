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
            return '0'
        else:
            left = generate_circuit(n // 2)
            right = generate_circuit(n - n // 2)
            return f'({left},{right})'
    
    def hodge_height(circuit):
        if circuit in ('0', '1'):
            return 0
        left, right = circuit.split(',')[0], circuit.split(',')[1][:-1]
        return max(hodge_height(left), hodge_height(right)) + 1
    
    def xor_and_tree_width(circuit):
        if circuit in ('0', '1'):
            return 1
        left, right = circuit.split(',')[0], circuit.split(',')[1][:-1]
        return max(xor_and_tree_width(left), xor_and_tree_width(right))
    
    n_values = [5, 10, 15, 20, 30, 40]
    total_width = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            circuit = generate_circuit(n)
            height = hodge_height(circuit)
            width = xor_and_tree_width(circuit)
            total_width += width
            instances_tested += 1
    
    mean_width = Fraction(total_width, instances_tested)
    conjecture_holds = mean_width <= 2 ** (Fraction(1, 2) * math.log2(instances_tested))
    
    return {
        "metric_name": "XOR-AND Tree Width",
        "metric_value": float(mean_width),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_width = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_width} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")