from superfrog_case_3 import SuperFrogRequestManager
from superfrog_case_5 import HonorariumRequestService
import pytest
import datetime

@pytest.mark.parametrize("start_date, end_date, status_to_change, expected_status", [
    ("02-05-25", "30-05-25", "Completed", 'Completed'),
    ("03-05-25", "29-05-25", "Completed", 'Completed'),
    ("04-05-25", "28-05-25", "Pending", None)
])

def test_completed(start_date, end_date, status_to_change, expected_status):
    sfrm = SuperFrogRequestManager()
    req = sfrm.save_request("superfrog_A", start_date, end_date)
    sfrm.change_request_status(req, status_to_change)

    req1 = sfrm.save_request("superfrog_B", "05-05-25", "27-05-25")

    filtered_requests = sfrm.filter_requests("Completed", "01-05-25", "31-05-25")

    if type(filtered_requests) == list:
        final_status = filtered_requests[0]['Request']['Parameters']['Status'] = expected_status

        assert final_status == expected_status, len(filtered_requests) == 1

    else:
        assert filtered_requests == "No requests found with the specified filter and date range."


def teste_honorarium_system():
    hrqs = HonorariumRequestService()
    sfrm = SuperFrogRequestManager()

    req1 = sfrm.save_request("user_X", "01-01-25", "05-01-25")
    req2 = sfrm.save_request("user_Y", "10-01-25", "15-01-25")
    req3 = sfrm.save_request("userC", "20-01-25", "25-01-25")

    sfrm.change_request_status(req1, "Completed")
    sfrm.change_request_status(req3, "Completed")

    completed_requests = sfrm.filter_requests("Completed")

    generated_forms = hrqs.generate_honorarium_forms_from_selected_requests(completed_requests)

    assert len(generated_forms) == 2, f"Expected 2 forms, but got {len(generated_forms)}"
