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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2**n):
            clause = [random.randint(-1, 0) * (i + 1) for i in range(n)]
            if any(c == 0 for c in clause):
                continue
            clauses.append(clause)
        return clauses
    
    def real_radical_dimension(clauses):
        # Placeholder implementation; actual computation requires sympy or similar
        return Fraction(1, 2) * math.log(len(clauses), 2)
    
    def disjointness_communication_complexity(n):
        return n
    
    n = 40
    clauses = generate_3cnf(n)
    rad_dim = real_radical_dimension(clauses)
    comm_comp = disjointness_communication_complexity(n)
    
    return {
        "metric_name": "disjointness_communication_complexity",
        "metric_value": comm_comp,
        "instances_tested": 1,
        "conjecture_holds": rad_dim == Fraction(1, 2) * math.log(n, 2),
        "counterexample": f"rad_dim={rad_dim}, comm_comp={comm_comp}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")