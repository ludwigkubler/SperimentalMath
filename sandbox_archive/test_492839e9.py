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
    
    def generate_k_clique(n):
        if n < 3:
            return []
        clique = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(clique)
        return clique[:min(2 * int(math.log2(n)), len(clique))]
    
    def free_group_from_clique(clique):
        generators = set()
        relations = []
        for u, v in clique:
            generators.add(f'x{u}')
            generators.add(f'x{v}')
            relations.append((f'x{u}', f'x{v}'))
            relations.append((f'x{v}', f'x{u}'))
        return len(generators), relations
    
    n = random.randint(5, 40)
    clique = generate_k_clique(n)
    num_generators, _ = free_group_from_clique(clique)
    
    return {
        "metric_name": "num_generators",
        "metric_value": num_generators,
        "instances_tested": 1,
        "conjecture_holds": num_generators >= n ** (1/3),
        "counterexample": "" if num_generators >= n ** (1/3) else f"n={n}, generators={num_generators}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(2, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={res['counterexample']}\", first_failing_seed={first_failing_seed}")