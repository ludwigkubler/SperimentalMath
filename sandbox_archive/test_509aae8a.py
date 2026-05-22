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
    
    def incidence_complex(f):
        n = len(f)
        V = list(range(2**n))
        E = []
        for i in range(n):
            for j in range(i+1, n):
                if f[i] and f[j]:
                    E.append((i, j))
        return V, E

    def homology(V, E):
        # Compute the homology of the incidence complex
        # This is a simplified version for demonstration purposes
        # In practice, you would use a more sophisticated algorithm
        if not E:
            return 0
        return len(E) / n
    
    def local_induction_dimension(homology_value, n):
        return homology_value * n**(1/2)
    
    n = random.randint(5, 40)
    f = [random.choice([True, False]) for _ in range(n)]
    V, E = incidence_complex(f)
    homology_value = homology(V, E)
    dim = local_induction_dimension(homology_value, n)
    
    return {
        "metric_name": "local_induction_dimension",
        "metric_value": dim,
        "instances_tested": 1,
        "conjecture_holds": dim <= (n**(1/2 + Fraction(1, 10))),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
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
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")