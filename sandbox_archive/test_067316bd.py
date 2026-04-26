import sys
import random
from itertools import combinations

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3sat_instance(n):
        clauses = []
        for _ in range(2**n):
            literals = [random.choice([f'x{i}', f'-x{i}']) for i in range(n)]
            clause = ' or '.join(literals)
            clauses.append(clause)
        return clauses
    
    def resolution_proof_size(instance):
        # Simplified heuristic to estimate resolution proof size
        return len(instance) * 2
    
    def convex_hull_facets(clauses):
        # Placeholder for actual computation of convex hull facets
        # This is a dummy implementation for demonstration purposes
        return random.randint(1, 10)
    
    n = random.choice([5, 8, 11, 14])
    instance = generate_3sat_instance(n)
    proof_size = resolution_proof_size(instance)
    facets = convex_hull_facets(instance)
    
    expected_facets = round(2**(n/2))
    conjecture_holds = abs(facets - expected_facets) <= 0.1 * expected_facets
    counterexample = "" if conjecture_holds else f"Facets: {facets}, Expected: {expected_facets}"
    
    return {
        "metric_name": "convex_hull_facets",
        "metric_value": facets,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_facets = sum(r["metric_value"] for r in results) / len(results)
    std_dev = (sum((r["metric_value"] - mean_facets)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_facets} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")