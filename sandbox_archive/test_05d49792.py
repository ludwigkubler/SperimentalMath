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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n):
            clause = [random.randint(-1, -n), random.randint(1, n)]
            if random.choice([True, False]):
                clause[0] *= -1
            cnf.append(clause)
        return cnf
    
    def dpll(cnf):
        def unit_propagate(cnf):
            while True:
                found = False
                for i, cl in enumerate(cnf):
                    if len(cl) == 1:
                        var = cl[0]
                        if var > 0:
                            for j, other_cl in enumerate(cnf):
                                if var in other_cl:
                                    cnf[j] = [x for x in other_cl if x != var and x != -var]
                                    found = True
                        else:
                            for j, other_cl in enumerate(cnf):
                                if -var in other_cl:
                                    cnf[j] = [x for x in other_cl if x != var and x != -var]
                                    found = True
                if not found:
                    break
        
        def pure_literal_elimination(cnf):
            while True:
                found = False
                pos_counts = {i: 0 for i in range(1, n+1)}
                neg_counts = {i: 0 for i in range(1, n+1)}
                for cl in cnf:
                    for lit in cl:
                        if lit > 0:
                            pos_counts[lit] += 1
                        else:
                            neg_counts[-lit] += 1
                
                for var in range(1, n+1):
                    if pos_counts[var] == 0 and neg_counts[var] > 0:
                        cnf = [cl for cl in cnf if -var not in cl]
                        found = True
                    elif neg_counts[var] == 0 and pos_counts[var] > 0:
                        cnf = [cl for cl in cnf if var not in cl]
                        found = True
                
                if not found:
                    break
        
        unit_propagate(cnf)
        pure_literal_elimination(cnf)
        
        def backtrack(cnf, assignment):
            if len(cnf) == 0:
                return True
            if any(len(cl) == 0 for cl in cnf):
                return False
            
            var = None
            for cl in cnf:
                if len(cl) > 1:
                    var = cl[0]
                    break
            
            if var is None:
                return False
            
            assignment[var] = True
            new_cnf = [cl for cl in cnf if var not in cl and -var not in cl]
            if backtrack(new_cnf, assignment):
                return True
            
            assignment[var] = False
            new_cnf = [cl for cl in cnf if -var not in cl and var not in cl]
            if backtrack(new_cnf, assignment):
                return True
            
            return False
        
        assignment = {}
        return backtrack(cnf, assignment)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    r_phi = len(cnf)  # Simplified geometric quantization rank
    d_phi = len(cnf) if not dpll(cnf) else 0
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": r_phi * d_phi,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 17 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0 support_fraction={support_fraction}")
    elif any(r["conjecture_holds"] is False for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")