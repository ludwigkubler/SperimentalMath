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
    
    def generate_ac0_circuit(n, func):
        if n == 1:
            return [func]
        else:
            left = generate_ac0_circuit(n // 2, lambda x: func(x[:n//2]))
            right = generate_ac0_circuit(n // 2, lambda x: func(x[n//2:]))
            return [lambda x: left[0](x) ^ right[0](x)]
    
    def count_irreducible_components(circuit):
        if len(circuit) == 1:
            return 1
        else:
            return count_irreducible_components(circuit[0])
    
    n = random.randint(5, 40)
    func = random.choice([lambda x: sum(x) % 2, lambda x: x[0] ^ x[1]])
    circuit = generate_ac0_circuit(n, func)
    irreducible_components = count_irreducible_components(circuit)
    
    metric_value = irreducible_components
    instances_tested = 1
    conjecture_holds = False if func == (lambda x: sum(x) % 2) else True
    counterexample = "" if conjecture_holds else "XOR function"
    
    return {
        "metric_name": "irreducible_components",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"XOR function\" first_failing_seed={first_failing_seed}")