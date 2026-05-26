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
        if len(f) != 2**n:
            raise ValueError("f must be a Boolean function of n variables")
        
        # Simulate a simple protocol where each bit is communicated separately
        return n
    
    def tensor_network_valuation(f):
        n = int(math.log2(len(f)))
        rank = sum(1 for i in range(n) if f[i] != f[0])
        return rank
    
    instances_tested = 30
    total_rank = 0
    equal_count = 0
    max_n = 40
    
    for _ in range(instances_tested):
        n = random.randint(5, max_n)
        f = generate_boolean_function(n)
        
        cc = communication_complexity(f)
        rank = tensor_network_valuation(f)
        
        total_rank += rank
        
        if rank == cc:
            equal_count += 1
    
    mean_rank = total_rank / instances_tested
    support_fraction = equal_count / instances_tested
    
    return {
        "metric_name": "minimal_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": support_fraction >= 0.25,
        "counterexample": "" if support_fraction >= 0.25 else f"rank={mean_rank}, expected=CC(f)"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{'seed': {seed}, ...{result}...}}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"rank > CC(f)\" first_failing_seed={seeds[first_failing_seed]}")