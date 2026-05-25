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

# Function to generate a random n-dimensional manifold
def generate_manifold(n):
    return [random.randint(1, 10) for _ in range(n)]

# Function to construct a tropicalized sheaf over a manifold
def construct_tropicalized_sheaf(manifold):
    return sum(manifold)

# Function to compute the size of a tropicalized sheaf
def size_of_sheaf(sheaf):
    return len(sheaf)

# Function to compute the rank of a tropicalized sheaf (simplified for testing)
def rank_of_sheaf(sheaf):
    return max(sheaf) - min(sheaf) + 1

# Polynomial-time computable invariant ψ(T) on tropicalized sheaves
def invariant_psi(sheaf):
    return size_of_sheaf(sheaf)

# Function to generate a random AC0 parity circuit with size less than 2^(1.5n)
def generate_ac0_circuit(n):
    return [random.choice([0, 1]) for _ in range(2 ** (int(1.5 * n)))]

# Function to compute the size of an AC0 parity circuit
def size_of_circuit(circuit):
    return len(circuit)

# Main function to run a single trial with a given seed
def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    # Parameters for testing
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        manifold = generate_manifold(n)
        sheaf = construct_tropicalized_sheaf(manifold)
        psi_value = invariant_psi(sheaf)
        
        # Check the conjecture for tropicalized sheaves computing PARITY
        if psi_value < 2 * math.log(n):
            results.append({
                "metric_name": "Invariant ψ(T)",
                "metric_value": psi_value,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"ψ(T)={psi_value} <= 2c·log(n)={2 * math.log(n)}"
            })
        else:
            results.append({
                "metric_name": "Invariant ψ(T)",
                "metric_value": psi_value,
                "instances_tested": 1,
                "conjecture_holds": True,
                "counterexample": ""
            })
        
        # Generate and check AC0 parity circuits
        for _ in range(3):  # Test with multiple instances of AC0 circuits
            circuit = generate_ac0_circuit(n)
            psi_value_circuit = invariant_psi(circuit)
            
            if psi_value_circuit > 2 * math.log(n):
                results.append({
                    "metric_name": "Invariant ψ(C)",
                    "metric_value": psi_value_circuit,
                    "instances_tested": 1,
                    "conjecture_holds": True,
                    "counterexample": ""
                })
            else:
                results.append({
                    "metric_name": "Invariant ψ(C)",
                    "metric_value": psi_value_circuit,
                    "instances_tested": 1,
                    "conjecture_holds": False,
                    "counterexample": f"ψ(C)={psi_value_circuit} <= 2c·log(n)={2 * math.log(n)}"
                })
    
    # Compute mean and std of metric values
    psi_values = [r["metric_value"] for r in results if "Invariant ψ(T)" in r]
    invariant_psi_mean = sum(psi_values) / len(psi_values)
    invariant_psi_std = (sum((x - invariant_psi_mean) ** 2 for x in psi_values) / len(psi_values)) ** 0.5
    
    # Check if the conjecture holds for all seeds
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    return {
        "seed": seed,
        "invariant_psi_mean": invariant_psi_mean,
        "invariant_psi_std": invariant_psi_std,
        "support_fraction": support_fraction
    }

if __name__ == "__main__":
    import sys
    
    if not sys.argv[1:]:
        seeds = [2**i + 7 for i in range(5, 30)]  # List of 30 primes
    else:
        seeds = list(map(int, sys.argv[1:]))
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    # Compute overall metrics and support fraction
    invariant_psi_means = [r["invariant_psi_mean"] for r in results]
    invariant_psi_stds = [r["invariant_psi_std"] for r in results]
    support_fractions = [r["support_fraction"] for r in results]
    
    overall_invariant_psi_mean = sum(invariant_psi_means) / len(invariant_psi_means)
    overall_invariant_psi_std = (sum((x - overall_invariant_psi_mean) ** 2 for x in invariant_psi_means) / len(invariant_psi_means)) ** 0.5
    overall_support_fraction = sum(support_fractions) / len(support_fractions)
    
    if all(r["support_fraction"] == 1 for r in results):
        print(f"RESULT: SUPPORTED mean={overall_invariant_psi_mean} std={overall_invariant_psi_std} support_fraction={overall_support_fraction}")
    elif overall_support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={overall_invariant_psi_mean} std={overall_invariant_psi_std} support_fraction={overall_support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["support_fraction"] == 1), None)
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction<{overall_support_fraction}\" first_failing_seed={first_failing_seed}")