from superfrog_case_3 import SuperFrogRequestManager
from superfrog_case_5 import HonorariumRequestService, HonorariumRequestForm
import pytest

def test_filter_completed_requests_pytest():
    """
    Pytest test: Ensures filter_requests returns only requests with status 'Completed'.
    """
    manager = SuperFrogRequestManager()

    req1 = manager.save_request("user_X", "01-01-23", "05-01-23")
    req2 = manager.save_request("user_Y", "10-01-23", "15-01-23")
    req3 = manager.save_request("user_Z", "20-01-23", "25-01-23")
    req4 = manager.save_request("user_W", "01-02-23", "05-02-23")

    manager.change_request_status(req1, "Completed")
    manager.change_request_status(req3, "Completed")

    completed_requests = manager.filter_requests("Completed")

    assert isinstance(completed_requests, list), "Expected a list of requests."
    assert len(completed_requests) == 2, f"Expected 2 completed requests, but got {len(completed_requests)}"

    expected_request_ids = {"user_X_01-01-23_05-01-23", "user_Z_20-01-23_25-01-23"}
    actual_request_ids = {req["Request"]["RequestId"] for req in completed_requests}

    assert actual_request_ids == expected_request_ids, \
        f"Expected request IDs {expected_request_ids}, but got {actual_request_ids}"


@pytest.fixture
def setup_systems():
    request_manager = SuperFrogRequestManager()
    honorarium_system = HonorariumRequestService()

    req1_payload = request_manager.save_request("superfrog_A", "01-05-25", "01-05-25")
    req2_payload = request_manager.save_request("superfrog_B", "05-05-25", "05-05-25")
    req3_payload = request_manager.save_request("superfrog_A", "10-05-25", "10-05-25")
    request_manager.save_request("superfrog_C", "12-05-25", "12-05-25")

    request_manager.change_request_status(req1_payload, "Completed")
    request_manager.change_request_status(req2_payload, "Completed")
    request_manager.change_request_status(req3_payload, "Completed")
    
    return request_manager, honorarium_system

def test_case_5_generate_tcu_honorarium_forms(setup_systems, capsys):

    request_manager, honorarium_system = setup_systems
    
    print("\n--- Case 5 initializing ---")

    # PRECONDITION: The Spiritual Director has selected specific apparitions.
    # 1. Simulate the recovery of "Completed" apparitions
    # (The year 25 is used to match the setup data)
    all_completed_requests_result = request_manager.filter_requests("Completed", "01-05-25", "30-05-25")

    assert isinstance(all_completed_requests_result, list), \
        f"filter_requests deveria retornar uma lista. Retornou: {all_completed_requests_result}"
    assert len(all_completed_requests_result) == 3, "Deveria haver 3 aparições 'Completed' no período."

    # 2. Simulate the selection by the Spiritual Director (we will select the first two on the list)
    selected_requests_for_payment = all_completed_requests_result[:2]
    assert len(selected_requests_for_payment) == 2, "Diretor deveria ter selecionado 2 aparições."
    print(f"[TestSetup] Diretor selecionou {len(selected_requests_for_payment)} aparições para pagamento.")

    print("[TestRun] Passo 1: Seleção confirmada pelo Diretor.")

    print("[TestRun] Passo 2: Solicitando geração de formulários...")
    generated_honorarium_forms = honorarium_system.generate_honorarium_forms_from_selected_requests(
        selected_requests_for_payment
    )
    honorarium_system.display_generated_forms_to_director(generated_honorarium_forms)

    # Expected Results of Test Case 5:
    assert len(generated_honorarium_forms) == len(selected_requests_for_payment), \
        "Número de formulários gerados não corresponde ao número de aparições selecionadas."
    print(f"[Assert] Verificado: {len(generated_honorarium_forms)} formulários gerados como esperado.")

    assert honorarium_system.last_displayed_forms_to_director == generated_honorarium_forms, \
        "Formulários exibidos ao diretor não são os mesmos que foram gerados."
    print("[Assert] Verificado: Formulários corretos foram 'exibidos' ao diretor.")

    # Check the content of generated forms
    for i, form in enumerate(generated_honorarium_forms):
        assert isinstance(form, HonorariumRequestForm)
        original_request_payload = selected_requests_for_payment[i]
        original_params = original_request_payload["Request"]["Parameters"]

        assert form.original_request_id == original_request_payload["Request"]["RequestId"]
        assert form.user_id == original_params["userId"]
        expected_period_str = f"{original_params['startDate']} a {original_params['endDate']}"
        assert form.period_str == expected_period_str
        assert form.amount == 150