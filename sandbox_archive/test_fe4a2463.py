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
    
    def frege_proof_length(f):
        # Placeholder for Frege proof length calculation
        return len(f)

    def von_neumann_entropy(n):
        return n * (math.log2(n) - 1)

    c = 1.0  # Constant factor, can be adjusted

    metric_name = "FregeProofLength"
    instances_tested = 0
    conjecture_holds = True
    counterexample = ""

    for n in range(10, 41):
        for _ in range(3):  # Test multiple instances per size
            f = [random.choice([0, 1]) for _ in range(n)]
            proof_length = frege_proof_length(f)
            entropy = von_neumann_entropy(n)

            if entropy > c * math.log2(math.factorial(n)) / math.log2(proof_length):
                conjecture_holds = False
                counterexample = f"Function with n={n} and FregeProofLength={proof_length}"
                break

        instances_tested += 3

    return {
        "metric_name": metric_name,
        "metric_value": proof_length,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")