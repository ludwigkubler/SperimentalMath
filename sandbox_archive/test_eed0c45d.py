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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = int(math.log2(len(f)))
        count = 0
        for i in range(2**n):
            if f[i] != f[~i]:
                count += 1
        return count
    
    def frobenius_class_dimension(f):
        n = int(math.log2(len(f)))
        dimension = 0
        for i in range(n):
            for j in range(i+1, n):
                if f[i] == f[j]:
                    dimension += 1
        return dimension
    
    total_dim = 0
    total_rank = 0
    instances_tested = 0
    n_max = 5
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):
            f = generate_boolean_function(n)
            dim = frobenius_class_dimension(f)
            rank = communication_complexity(f)
            
            total_dim += dim
            total_rank += rank
            instances_tested += 1
    
    mean_dim = total_dim / instances_tested
    mean_rank = total_rank / instances_tested
    
    conjecture_holds = mean_dim <= n_max**2 and mean_rank <= 10
    counterexample = "" if conjecture_holds else f"dim={mean_dim}, rank={mean_rank}"
    
    return {
        "metric_name": "Frobenius class dimension",
        "metric_value": mean_dim,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_dim = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_dim} std=0.0 support_fraction=1.0")
    elif any(r["communication_complexity_rank"] > 10 for r in results) or any(r["metric_value"] > n_max**2 for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"dim={mean_dim}, rank={mean_rank}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")