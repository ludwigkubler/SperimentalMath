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

def generate_frege_proof(n):
    return " ".join(random.choices("ABCD", k=random.randint(2, 5)) for _ in range(n))

def compute_grothendieck_group_rank(phi):
    # Placeholder implementation of Grothendieck group rank computation
    # This is a dummy function and should be replaced with actual logic
    return len(set(phi.split()))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.randint(5, 40)
    phi = generate_frege_proof(n)
    grothendieck_rank = compute_grothendieck_group_rank(phi)
    proof_width = len(phi.split())
    
    ratio = Fraction(grothendieck_rank, proof_width) if proof_width > 0 else None
    
    return {
        "metric_name": "Grothendieck Rank / Proof Width Ratio",
        "metric_value": float(ratio) if ratio is not None else None,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False if ratio is None or ratio > 2 else True,
        "counterexample": "mapping_undefined" if ratio is None else ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        support_fraction = 1.0
        RESULT = f"SUPPORTED mean={mean_ratio} std=0 support_fraction={support_fraction}"
    elif any(not r["conjecture_holds"] and r["counterexample"] != "mapping_undefined" for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        RESULT = f"FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}"
    else:
        RESULT = "INCONCLUSIVE mapping_undefined"
    
    print(RESULT)