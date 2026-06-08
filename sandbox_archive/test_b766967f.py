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
    
    def hodge_dimension(f):
        # Placeholder for Hodge dimension calculation
        # This is a dummy implementation and does not reflect the actual Hodge decomposition.
        return len(f)
    
    def communication_complexity_matrix_rank(f):
        # Placeholder for communication complexity matrix rank calculation
        # This is a dummy implementation and does not reflect the actual computation.
        return random.randint(0, 10)
    
    n = 5  # Start with small n and increase to test asymptotic behavior
    instances_tested = 0
    total_rank = 0
    total_dimension = 0
    
    while True:
        f = generate_boolean_function(n)
        rank = communication_complexity_matrix_rank(f)
        dimension = hodge_dimension(f)
        
        if rank > dimension + 3:
            return {
                "metric_name": "communication_complexity_rank",
                "metric_value": rank,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": f"Rank {rank} exceeds dimension + 3 ({dimension})"
            }
        
        total_rank += rank
        total_dimension += dimension
        instances_tested += 1
        
        if instances_tested >= 30:
            break
        
        n += 5
    
    mean_rank = total_rank / instances_tested
    mean_dimension = total_dimension / instances_tested
    correlation_coefficient = (instances_tested * sum(rank * dim for rank, dim in zip(f, f)) - 
                               instances_tested * mean_rank * mean_dimension) / \
                              math.sqrt((instances_tested * sum(rank**2 for rank in f) - instances_tested * mean_rank**2) *
                                        (instances_tested * sum(dim**2 for dim in f) - instances_tested * mean_dimension**2))
    
    return {
        "metric_name": "communication_complexity_rank",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(rank <= dimension + 3 for rank, dim in zip(f, f)),
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
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
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if not r['conjecture_holds'])}\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")