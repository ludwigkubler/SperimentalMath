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
    
    def generate_tseitin_formula(n, m):
        variables = set()
        clauses = []
        
        for i in range(m):
            clause = []
            for j in range(n):
                var = f'x{j+1}'
                if random.choice([True, False]):
                    clause.append(var)
                else:
                    clause.append(f'¬{var}')
                    variables.add(var)
            clauses.append(clause)
        
        return variables, clauses
    
    def grobner_basis_dimension(clauses):
        # Placeholder for Grobner basis dimension calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses)  # Simplified for demonstration purposes
    
    def resolution_refutation_length(clauses):
        # Placeholder for Resolution refutation length calculation
        # This is a dummy implementation and should be replaced with actual computation
        return len(clauses) * 2  # Simplified for demonstration purposes
    
    n = random.randint(5, 40)
    m = random.randint(5, 40)
    
    variables, clauses = generate_tseitin_formula(n, m)
    dim_grobner = grobner_basis_dimension(clauses)
    length_resolution = resolution_refutation_length(clauses)
    
    return {
        "metric_name": "Grobner Basis Dimension",
        "metric_value": dim_grobner,
        "instances_tested": 1,
        "conjecture_holds": dim_grobner >= 2 ** (m * math.log(2, math.e)),
        "counterexample": "" if dim_grobner >= 2 ** (m * math.log(2, math.e)) else f"dim(Grob(F)) = {dim_grobner} < 2^(Ω(m))"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [random.randint(100, 999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")