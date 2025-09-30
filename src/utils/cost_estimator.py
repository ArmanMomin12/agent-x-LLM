# src/utils/cost_estimator.py

def estimate_cost(plan: dict) -> dict:
    """
    Estimate duration, team size, and budget based on a structured plan dictionary.

    Parameters:
        plan (dict): Dictionary output from planner agent.

    Returns:
        dict: Estimated time (weeks), team size, and budget in USD.
    """

    # Simple heuristic mapping
    phase_duration = {
        "Phase 1": 4,
        "Phase 2": 8,
        "Phase 3": 8,
        "Phase 4": 8,
        "Phase 5": 8,
        "Phase 6": 16
    }

    team_roles = {
        "Frontend developers": 2,
        "Backend developers": 2,
        "Data scientists": 2,
        "Designers": 1,
        "QA engineers": 1
    }

    # Cost estimation (USD/month)
    salary_rates = {
        "Frontend developers": 5000,
        "Backend developers": 5500,
        "Data scientists": 6000,
        "Designers": 4000,
        "QA engineers": 4500
    }

    total_weeks = 0
    total_cost = 0
    total_people = 0

    for key, weeks in phase_duration.items():
        total_weeks += weeks

    for role, count in team_roles.items():
        total_people += count
        monthly_cost = salary_rates[role] * count
        total_cost += monthly_cost * (total_weeks / 4)  # convert weeks to months

    return {
        "estimated_duration_weeks": total_weeks,
        "estimated_team_size": total_people,
        "estimated_total_cost_usd": int(total_cost)
    }

# 🧪 Example Usage
if __name__ == "__main__":
    dummy_plan = {
        "**Phase 1": "Requirements Gathering and Planning (Weeks 1-4)**",
        "**Phase 2": "Frontend Development (Weeks 5-12)**",
        "**Phase 3": "Backend Development (Weeks 13-20)**",
        "**Phase 4": "Model Development (Weeks 21-28)**",
        "**Phase 5": "Deployment and Testing (Weeks 29-36)**",
        "**Phase 6": "Launch and Maintenance (Weeks 37-52)**"
    }

    result = estimate_cost(dummy_plan)
    print("\n🧾 Cost Estimate Summary:")
    print(result)


