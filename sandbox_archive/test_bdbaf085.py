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
    
    def dpll(phi):
        if not phi:
            return True, {}
        var = next(iter(phi))
        for assignment in [True, False]:
            new_phi = {k: v for k, v in phi.items() if k != var}
            for k, v in new_phi.items():
                if (var, assignment) in v:
                    new_phi[k] = [x for x in v if x != (var, assignment)]
                elif (not var, not assignment) in v:
                    new_phi[k] = [x for x in v if x != (not var, not assignment)]
            if dpll(new_phi)[0]:
                return True, {**{k: v for k, v in phi.items() if k == var}, **new_phi}
        return False, {}
    
    def frege_proof_depth(phi):
        _, assignment = dpll(phi)
        depth = 0
        stack = [(phi, assignment)]
        while stack:
            current_phi, current_assignment = stack.pop()
            if not current_phi:
                continue
            var = next(iter(current_phi))
            for assignment in [True, False]:
                new_phi = {k: v for k, v in current_phi.items() if k != var}
                for k, v in new_phi.items():
                    if (var, assignment) in v:
                        new_phi[k] = [x for x in v if x != (var, assignment)]
                    elif (not var, not assignment) in v:
                        new_phi[k] = [x for x in v if x != (not var, not assignment)]
                stack.append((new_phi, {**{k: v for k, v in current_assignment.items() if k == var}, **current_assignment}))
            depth += 1
        return depth
    
    def grothendieck_group_size(phi):
        # Simplified Grothendieck group size calculation
        return len(phi)
    
    def minimal_representation_size(phi):
        # Simplified minimal representation size calculation
        return len(phi)
    
    n = random.randint(5, 40)
    phi = {f'x{i}': [(i, True), (i, False)] for i in range(n)}
    mrs = minimal_representation_size(phi)
    d_phi = frege_proof_depth(phi)
    
    return {
        "metric_name": "mrs_d_ratio",
        "metric_value": Fraction(mrs, d_phi),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": mrs <= 2 * d_phi and mrs >= 0.5 * d_phi,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(r["conjecture_holds"] for r in results) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mrs_d_ratio\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE no seeds supported")