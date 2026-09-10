MATERIAL = (
    '{"verdict":"MATERIAL","severity":88,"category":"MONEY",'
    '"summary":"The refund window is reduced from 30 days to 7 days."}'
)
NON_MATERIAL = (
    '{"verdict":"NON_MATERIAL","severity":8,"category":"NONE",'
    '"summary":"The revision changes wording without changing user rights."}'
)
INITIAL = "Customers may request a full refund within 30 calendar days of purchase."
MATERIAL_REVISION = "Customers may request a full refund within 7 calendar days of purchase."
WORDING_REVISION = "A full refund may be requested during the 30 days following purchase."


def test_initial_registry_state(direct_deploy):
    contract = direct_deploy("contract.py", "Example Terms", INITIAL)
    active = contract.get_active_policy()
    assert active.status == "ACTIVE"
    assert active.text == INITIAL
    assert contract.get_revision_count() == 1


def test_material_revision_requires_review(direct_vm, direct_deploy):
    direct_vm.mock_llm(r".*", MATERIAL)
    contract = direct_deploy("contract.py", "Example Terms", INITIAL)
    contract.propose_revision(MATERIAL_REVISION, "Shorten refund period")
    assert contract.get_revision(1).status == "REVIEW_REQUIRED"
    assert contract.get_active_policy().text == INITIAL
    assert direct_vm.run_validator() is True


def test_owner_can_approve_material_revision(direct_vm, direct_deploy):
    direct_vm.mock_llm(r".*", MATERIAL)
    contract = direct_deploy("contract.py", "Example Terms", INITIAL)
    contract.propose_revision(MATERIAL_REVISION, "Shorten refund period")
    contract.review_material_revision(1, True)
    assert contract.get_revision(0).status == "SUPERSEDED"
    assert contract.get_revision(1).status == "ACTIVE"


def test_non_material_revision_auto_activates(direct_vm, direct_deploy):
    direct_vm.mock_llm(r".*", NON_MATERIAL)
    contract = direct_deploy("contract.py", "Example Terms", INITIAL)
    contract.propose_revision(WORDING_REVISION, "Clarify wording")
    assert contract.get_revision(0).status == "SUPERSEDED"
    assert contract.get_revision(1).status == "ACTIVE"


def test_non_owner_cannot_propose(direct_vm, direct_deploy, direct_bob):
    contract = direct_deploy("contract.py", "Example Terms", INITIAL)
    with direct_vm.prank(direct_bob):
        with direct_vm.expect_revert("Only the registry owner"):
            contract.propose_revision(MATERIAL_REVISION, "Unauthorized")


def test_validator_rejects_different_decision(direct_vm, direct_deploy):
    direct_vm.mock_llm(r".*", MATERIAL)
    contract = direct_deploy("contract.py", "Example Terms", INITIAL)
    contract.propose_revision(MATERIAL_REVISION, "Shorten refund period")
    direct_vm.clear_mocks()
    direct_vm.mock_llm(r".*", NON_MATERIAL)
    assert direct_vm.run_validator() is False
