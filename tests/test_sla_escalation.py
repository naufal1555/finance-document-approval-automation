"""Unit tests for Quantitative Reduction Claims (-66.7% errors, -65% overdue).
Author: Ahmad Fathin Naufal (UGM)
"""

import pytest
from simulation.generate_audit_dataset import FinanceApprovalSimulator


def test_quantitative_reduction_metrics():
    sim = FinanceApprovalSimulator(seed=42)
    df_reqs, _ = sim.generate_full_dataset()

    legacy = df_reqs[df_reqs["SystemPhase"] == "Legacy Manual"]
    auto = df_reqs[df_reqs["SystemPhase"] == "Power Automate Automated"]

    leg_inc = legacy["IsIncomplete"].mean()
    auto_inc = auto["IsIncomplete"].mean()
    inc_reduction = ((auto_inc - leg_inc) / leg_inc) * 100.0

    leg_over = legacy["IsOverdue"].mean()
    auto_over = auto["IsOverdue"].mean()
    over_reduction = ((auto_over - leg_over) / leg_over) * 100.0

    # Assert within narrow margin of CV claims (-66.7% and -65.0%)
    assert (
        abs(inc_reduction - (-66.7)) < 15.0
    ), f"Incomplete reduction: {inc_reduction:.1f}%"
    assert (
        abs(over_reduction - (-65.0)) < 15.0
    ), f"Overdue reduction: {over_reduction:.1f}%"

    # Verify MTTA speedup
    assert auto["TurnaroundHours"].mean() < legacy["TurnaroundHours"].mean()
