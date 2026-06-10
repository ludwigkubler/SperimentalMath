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
        return [random.randint(0, 1) for _ in range(2**n)]
    
    def communication_complexity_rank_variance(f):
        n = len(f)
        circuit_ranks = []
        for i in range(n):
            for j in range(i+1, n):
                rank = sum(f[i] ^ f[j])
                circuit_ranks.append(rank)
        return Fraction(sum(circuit_ranks), len(circuit_ranks))
    
    def minimal_p_adic_derivative_rank(f):
        # Placeholder implementation
        return 0
    
    instances_tested = 30
    n_max = 40
    mdr_values = []
    delta_values = []
    
    for _ in range(instances_tested):
        n = random.randint(5, 40)
        f = generate_boolean_function(n)
        delta = communication_complexity_rank_variance(f)
        mdr = minimal_p_adic_derivative_rank(f)
        
        if mdr > 1.2 * delta:
            return {
                "metric_name": "mdr",
                "metric_value": mdr,
                "instances_tested": instances_tested,
                "n_max": n_max,
                "conjecture_holds": False,
                "counterexample": f"mdr(f) > 1.2 * Δ(f): {mdr} > {1.2 * delta}"
            }
        
        mdr_values.append(mdr)
        delta_values.append(delta)
    
    correlation_coefficient = sum((x - sum(x for x in mdr_values)/len(mdr_values)) * (y - sum(y for y in delta_values)/len(delta_values)) for x, y in zip(mdr_values, delta_values)) / (len(mdr_values) * math.sqrt(sum((x - sum(x for x in mdr_values)/len(mdr_values))**2 for x in mdr_values)) * math.sqrt(sum((y - sum(y for y in delta_values)/len(delta_values))**2 for y in delta_values)))
    
    return {
        "metric_name": "mdr",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": correlation_coefficient >= 0.8 and all(mdr <= 1.2 * delta for mdr, delta in zip(mdr_values, delta_values)),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(r["mdr"] > 1.5 * r["delta"] for r in results) or support_fraction < 0.6:
        first_failing_seed = next(seed for seed, result in enumerate(results, start=1) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mdr(f) > 1.5 * Δ(f)\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")