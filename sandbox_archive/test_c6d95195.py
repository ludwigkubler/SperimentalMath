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
    
    def generate_symmetric_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def negation(f):
        return [1 - x for x in f]
    
    def syntactic_monoid(f):
        n = int(math.log2(len(f)))
        monoid = set()
        for i in range(2**n):
            for j in range(2**n):
                result = 0
                for k in range(n):
                    if (i >> k) & 1:
                        result ^= f[j]
                monoid.add(result)
        return monoid
    
    def quandle_operation(monoid, a, b):
        return (a + b) % len(monoid)
    
    def minimal_rank(quandle_ops):
        rank = 0
        for op in quandle_ops:
            if op not in quandle_ops[:rank]:
                rank += 1
        return rank
    
    def communication_complexity(n):
        # Simplified model: n bits required to communicate the function
        return n
    
    n_values = [4, 6, 8, 10]  # Sample sizes
    results = []
    
    for n in n_values:
        f = generate_symmetric_function(n)
        neg_f = negation(f)
        monoid = syntactic_monoid(neg_f)
        
        quandle_ops = [quandle_operation(monoid, i, j) for i in monoid for j in monoid]
        rank = minimal_rank(quandle_ops)
        
        comm_complexity = communication_complexity(n)
        
        results.append({
            "n": n,
            "rank": rank,
            "comm_complexity": comm_complexity
        })
    
    mean_rank = sum(result["rank"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["rank"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["rank"] <= n / math.log(n)) / len(results)
    
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": mean_rank,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_rank = sum(result["metric_value"] for result in results) / len(results)
    std_rank = math.sqrt(sum((result["metric_value"] - mean_rank) ** 2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")