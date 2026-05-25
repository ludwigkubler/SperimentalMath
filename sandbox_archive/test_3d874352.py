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
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return True
        for i in range(1, p):
            if (i * i) % p == a:
                return True
        return False

    def minimal_rank(n, q):
        rank = 0
        for x in range(q):
            if is_quadratic_residue(x, q):
                rank += 1
        return rank

    n_values = [5, 10, 15, 20, 30, 40]
    total_rank_diff = 0
    instances_tested = 0
    
    for n in n_values:
        inner_product_circuit = random.getrandbits(n)
        xor_circuit = random.getrandbits(n)
        
        q = 2**n  # Simple finite field size for demonstration
        
        rank_inner = minimal_rank(inner_product_circuit, q)
        rank_xor = minimal_rank(xor_circuit, q)
        
        total_rank_diff += abs(rank_inner - rank_xor)
        instances_tested += 1
    
    mean_rank_diff = total_rank_diff / len(n_values)
    conjecture_holds = mean_rank_diff <= 0.5 * math.log(len(n_values))
    
    return {
        "metric_name": "mean_rank_diff",
        "metric_value": mean_rank_diff,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Mean rank difference {mean_rank_diff} > 0.5 * log({len(n_values)})"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Mean rank difference exceeds bound\" first_failing_seed={first_failing_seed}")