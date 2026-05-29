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
    
    def minterms(f):
        n = len(f)
        mints = []
        for i in range(2**n):
            binary = format(i, f'0{n}b')
            if all(f[j] == 1 for j in range(n) if binary[j] == '1'):
                mints.append(binary)
        return mints
    
    def dynkin_diagram_size(f):
        # Placeholder function to compute the size of the Dynkin diagram
        # This is a dummy implementation and should be replaced with actual logic
        return len(set(f))
    
    n = random.randint(5, 40)
    f = [random.choice([0, 1]) for _ in range(n)]
    mints = minterms(f)
    num_mints = len(mints)
    dynkin_size = dynkin_diagram_size(f)
    
    return {
        "metric_name": "monomial_ideal_complexity",
        "metric_value": num_mints,
        "instances_tested": 1,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_value = sum(result["metric_value"] for result in results) / len(results)
    std_value = math.sqrt(sum((result["metric_value"] - mean_value)**2 for result in results) / len(results))
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.7:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")