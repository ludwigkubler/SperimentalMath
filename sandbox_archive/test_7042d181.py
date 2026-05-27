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
    
    def generate_random_boolean_function(n, m):
        return [random.randint(0, 1) for _ in range(m)]
    
    def xor_and_tree_width(f):
        n = len(f)
        if n == 1:
            return 1
        mid = n // 2
        left = f[:mid]
        right = f[mid:]
        return 1 + max(xor_and_tree_width(left), xor_and_tree_width(right))
    
    def count_quadratic_residues(modulus):
        residues = set()
        for i in range(1, modulus):
            if (i * i) % modulus not in residues:
                residues.add((i * i) % modulus)
        return len(residues)
    
    n = 40
    m = n
    f = generate_random_boolean_function(n, m)
    t_f = xor_and_tree_width(f)
    
    if t_f == 1:
        p = 2
    else:
        p = next_prime(t_f + 1)
    
    residues_count = count_quadratic_residues(p)
    
    return {
        "metric_name": "XOR-AND tree width",
        "metric_value": t_f,
        "instances_tested": 1,
        "conjecture_holds": t_f <= math.sqrt(p),
        "counterexample": "" if t_f <= math.sqrt(p) else f"t(f) = {t_f} > √{p}"
    }

def next_prime(n):
    def is_prime(num):
        if num < 2:
            return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0:
                return False
        return True
    
    while not is_prime(n):
        n += 1
    return n

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.4f} std={std_value:.4f} support_fraction={support_fraction:.2f}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) > 0.2:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"t(f) > √p\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction:.2f} < 0.8")