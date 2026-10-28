"""Unit tests for Finance Approval Routing and Data Modeling.
Author: Ahmad Fathin Naufal (UGM)
"""

import pytest
from simulation.generate_audit_dataset import (
    FinanceApprovalSimulator,
    USERS,
    DEPARTMENTS,
)


def test_user_and_department_directory():
    assert (
        len(USERS) >= 20
    ), f"Expected >= 20 users for CV metric, got {len(USERS)}"
    assert len(DEPARTMENTS) == 5


def test_dataset_generation_volume():
    sim = FinanceApprovalSimulator(seed=42)
    df_reqs, df_audit = sim.generate_full_dataset()

    # Strictly verify CV claim: 300+ documents
    assert (
        len(df_reqs) >= 300
    ), f"Expected >= 300 documents, got {len(df_reqs)}"
    assert len(df_audit) == len(df_reqs)
    assert "RequestID" in df_reqs.columns
    assert "AmountIDR" in df_reqs.columns
    assert "ApprovalTier" in df_reqs.columns


def test_tier_assignment_logic():
    sim = FinanceApprovalSimulator(seed=42)
    df_reqs, _ = sim.generate_full_dataset()

    tier1 = df_reqs[df_reqs["ApprovalTier"] == "Tier 1 (<= 5M)"]
    tier2 = df_reqs[df_reqs["ApprovalTier"] == "Tier 2 (5M - 25M)"]
    tier3 = df_reqs[df_reqs["ApprovalTier"] == "Tier 3 (> 25M)"]

    assert (tier1["AmountIDR"] <= 5_000_000).all()
    assert (
        (tier2["AmountIDR"] > 5_000_000) & (tier2["AmountIDR"] <= 25_000_000)
    ).all()
    assert (tier3["AmountIDR"] > 25_000_000).all()
