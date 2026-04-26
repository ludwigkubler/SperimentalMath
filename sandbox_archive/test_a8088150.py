import random
import math
import json
from sys import argv

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def factorial(n):
        if n == 0:
            return 1
        else:
            return n * factorial(n-1)
    
    def binomial_coefficient(n, k):
        return factorial(n) // (factorial(k) * factorial(n - k))
    
    def young_tableau_to_shape(tableau):
        shape = []
        for row in tableau:
            shape.append(len(row))
        return tuple(shape)
    
    def hook_length_formula(shape):
        n = sum(shape)
        numerator = factorial(n)
        denominator = 1
        for i, row in enumerate(shape):
            for j in range(row):
                hook = (row - j) + (len(shape) - i - 1) - j
                denominator *= hook
        return numerator // denominator
    
    def irreducible_representation_dimension(shape):
        n = sum(shape)
        return hook_length_formula(shape)
    
    def generate_symmetric_group_action(n, k):
        # Simplified representation of a symmetric group action on {0,1}^n
        # This is a placeholder and should be replaced with actual group theory code
        return [random.randint(0, 1) for _ in range(n)]
    
    def communication_complexity(f):
        # Placeholder for computing deterministic communication complexity
        # This is a placeholder and should be replaced with actual protocol enumeration code
        return len(f)
    
    n = random.choice([5, 8, 11, 14])
    k = math.ceil(n / 2)
    action = generate_symmetric_group_action(n, k)
    f = [action[i] for i in range(n) if (i % 2 == 0)]
    
    shape = young_tableau_to_shape([[k]])
    dimension = irreducible_representation_dimension(shape)
    complexity = communication_complexity(f)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": complexity,
        "instances_tested": 1,
        "conjecture_holds": complexity <= dimension,
        "counterexample": "" if complexity <= dimension else f"complexity={complexity} > dimension={dimension}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    total_complexity = 0
    total_dimension = 0
    num_supporting = 0
    
    for seed in seeds:
        result = run_trial(seed)
        results.append(result)
        total_complexity += result["metric_value"]
        total_dimension += irreducible_representation_dimension(young_tableau_to_shape([[math.ceil(n / 2)]]))
        if result["conjecture_holds"]:
            num_supporting += 1
    
    mean_complexity = total_complexity / len(seeds)
    std_complexity = math.sqrt(sum((x - mean_complexity) ** 2 for x in [r["metric_value"] for r in results]) / len(seeds))
    support_fraction = num_supporting / len(seeds)
    
    print(json.dumps({"TRIAL": {"seed": seed, "metric_name": result["metric_name"], "metric_value": result["metric_value"], "instances_tested": result["instances_tested"], "conjecture_holds": result["conjecture_holds"], "counterexample": result["counterexample"]}}))
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_complexity} std={std_complexity} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")