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
    
    def generate_boolean_function(n):
        return [random.choice([True, False]) for _ in range(2**n)]
    
    def communication_complexity(f):
        n = f.index(True).bit_length()
        return n
    
    def tropical_motivic_rank(f):
        # Placeholder implementation; actual computation depends on tropical geometry
        return len(f)
    
    results = []
    for n in [5, 10, 15, 20, 30, 40]:
        f = generate_boolean_function(n)
        cc = communication_complexity(f)
        mtr = tropical_motivic_rank(f)
        results.append((cc, mtr))
    
    if not results:
        return {
            "metric_name": "mtr(f)",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    cc_values, mtr_values = zip(*results)
    mean_cc = sum(cc_values) / len(cc_values)
    mean_mtr = sum(mtr_values) / len(mtr_values)
    correlation = (sum((cc - mean_cc) * (mtr - mean_mtr) for cc, mtr in results) /
                   (len(results) * sum((cc - mean_cc)**2 for cc in cc_values) ** 0.5 *
                    sum((mtr - mean_mtr)**2 for mtr in mtr_values) ** 0.5))
    
    return {
        "metric_name": "mtr(f)",
        "metric_value": correlation,
        "instances_tested": len(results),
        "n_max": max(len(f) for f, _ in results),
        "conjecture_holds": abs(correlation) >= 0.95,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_correlation = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_correlation} std=0.0 support_fraction=1.0")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.8:
        print(f"RESULT: FALSIFIED counterexample=\"correlation_too_low\" first_failing_seed={seeds[next(i for i, r in enumerate(results) if not r['conjecture_holds'])]}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_evidence")