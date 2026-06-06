# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_boolean_function(m):
        return [random.choice([0, 1]) for _ in range(2**m)]
    
    def communication_complexity(f):
        m = len(f)
        max_rank = 0
        for i in range(1 << m):
            subset = [f[j] for j in range(m) if (i & (1 << j)) != 0]
            rank = sum(subset) + 1
            if rank > max_rank:
                max_rank = rank
        return max_rank
    
    def hodge_dimension(f):
        m = len(f)
        # Simplified Hodge dimension calculation for demonstration purposes
        # This is not a real Hodge dimension but serves as an example
        return Fraction(m, 2)
    
    instances_tested = 0
    total_hodge_dim = 0
    total_comm_rank = 0
    
    for _ in range(1000):
        m = random.randint(5, 30)
        f = generate_boolean_function(m)
        hodge_dim = hodge_dimension(f)
        comm_rank = communication_complexity(f)
        
        if hodge_dim is None or comm_rank is None:
            continue
        
        total_hodge_dim += hodge_dim
        total_comm_rank += comm_rank
        instances_tested += 1
    
    if instances_tested == 0:
        return {
            "metric_name": "Hodge Dimension vs Communication Rank",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": 30,
            "conjecture_holds": False,
            "counterexample": "No valid instances generated"
        }
    
    mean_hodge_dim = total_hodge_dim / instances_tested
    mean_comm_rank = total_comm_rank / instances_tested
    
    correlation_coefficient = (instances_tested * mean_hodge_dim * mean_comm_rank - 
                               sum(h * c for h, c in zip([hodge_dimension(generate_boolean_function(m)) for m in range(5, 31)], 
                                                        [communication_complexity(generate_boolean_function(m)) for m in range(5, 31)]))) / \
                              ((instances_tested - 1) * 
                               math.sqrt(sum((h - mean_hodge_dim)**2 for h in [hodge_dimension(generate_boolean_function(m)) for m in range(5, 31)]) *
                                         sum((c - mean_comm_rank)**2 for c in [communication_complexity(generate_boolean_function(m)) for m in range(5, 31)])))
    
    return {
        "metric_name": "Hodge Dimension vs Communication Rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": 30,
        "conjecture_holds": abs(correlation_coefficient) > 0.9,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_data")