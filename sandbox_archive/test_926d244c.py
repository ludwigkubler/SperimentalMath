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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def free_algebra_rank(f):
        n = len(f)
        variables = set()
        for term in f:
            for var in term:
                if var.startswith('x'):
                    variables.add(var)
        num_vars = len(variables)
        return num_vars
    
    def communication_complexity(f):
        n = len(f)
        rank_F = free_algebra_rank(f)
        return n * math.log2(n) / rank_F
    
    def alpha(n):
        return 1.4426950408889634  # Approximation of α(n) for large n
    
    instances_tested = 0
    total_metric_value = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(100):  # Test with at least 30 different random seeds
        f = generate_boolean_function(random.randint(5, 40))
        rank_F = free_algebra_rank(f)
        cc_f = communication_complexity(f)
        
        if rank_F <= len(f):
            instances_tested += 1
            total_metric_value += cc_f
            
            if not (alpha(len(f)) * 0.9 <= cc_f <= alpha(len(f)) * 1.1):
                conjecture_holds = False
                counterexample = f"CC_XOR(f) out of bounds: {cc_f} for n={len(f)}"
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": total_metric_value / instances_tested if instances_tested > 0 else 0,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2**i + 7 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results if r["instances_tested"] > 0) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results if r["instances_tested"] > 0) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unreachable")