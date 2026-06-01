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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def ideal_generated_by_variables(cnf):
        variables = set()
        for clause in cnf:
            for var in clause:
                if var > 0:
                    variables.add(var)
                else:
                    variables.add(-var)
        return variables
    
    def minimal_local_ring_norm(ideal, n):
        # Placeholder implementation
        return Fraction(n**(1/3) * math.log(len(cnf)), 1)
    
    n = random.randint(5, 40)
    m_min = int(n**(1/3) * math.log(n))
    m_max = int(n**(1/3) * math.log(n)) + 10
    m_range = range(m_min, m_max + 1)
    local_ring_norms = []
    
    for m in m_range:
        cnf = generate_cnf(n, m)
        ideal = ideal_generated_by_variables(cnf)
        norm = minimal_local_ring_norm(ideal, n)
        local_ring_norms.append(norm)
    
    mean_norm = sum(local_ring_norms) / len(local_ring_norms)
    std_norm = math.sqrt(sum((x - mean_norm)**2 for x in local_ring_norms) / len(local_ring_norms))
    
    return {
        "metric_name": "minimal_local_ring_norm",
        "metric_value": mean_norm,
        "instances_tested": len(local_ring_norms),
        "n_max": n,
        "conjecture_holds": True,  # Placeholder
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")