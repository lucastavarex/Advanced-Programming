import datetime
import unittest
from unittest.mock import MagicMock

class HonorariumRequestForm:
    def __init__(self, original_request_id, user_id, period_str, amount=0.0):
        self.original_request_id = original_request_id
        self.user_id = user_id
        self.period_str = period_str
        self.amount = amount
        self.event_details = "Event details"

    def __repr__(self):
        return (f"HonorariumRequestForm(ReqID: {self.original_request_id}, User: {self.user_id}, "
                f"Period: {self.period_str}, Amount: {self.amount})")

class HonorariumRequestService:
    def __init__(self):
        self.last_displayed_forms_to_director = []

    def generate_honorarium_forms_from_selected_requests(self, selected_appearance_requests):
        if not isinstance(selected_appearance_requests, list):
            print(f"[HonorariumRequestService] ERRO: selected_appearance_requests não é uma lista. Recebido: {selected_appearance_requests}")
            return [] 

        generated_forms = []
        print(f"\n[HonorariumRequestService] Iniciando geração de formulários para {len(selected_appearance_requests)} aparições selecionadas...")
        for req_payload in selected_appearance_requests:
            if not isinstance(req_payload, dict) or \
               "Request" not in req_payload or \
               "Parameters" not in req_payload["Request"] or \
               "RequestId" not in req_payload["Request"]:
                print(f"[HonorariumRequestService] ATENÇÃO: Payload de aparição inválido ou malformado ignorado: {req_payload}")
                continue

            params = req_payload["Request"]["Parameters"]
            request_id = req_payload["Request"]["RequestId"]

            if params.get("Status") != "Completed":
                print(f"[HonorariumRequestService] ATENÇÃO: Aparição {request_id} (Status: {params.get('Status')}) não está 'Completed'. Formulário não gerado.")
                continue

            form = HonorariumRequestForm(
                original_request_id=request_id,
                user_id=params.get("userId", "N/A"),
                period_str=f"{params.get('startDate', 'N/A')} a {params.get('endDate', 'N/A')}",
                amount=150
            )
            generated_forms.append(form)
            print(f"[HonorariumRequestService] Formulário gerado para RequestId: {request_id}")

        return generated_forms

    def display_generated_forms_to_director(self, forms_to_display):
        print(f"[HonorariumRequestService] Exibindo {len(forms_to_display)} formulários para o Diretor Espiritual.")
        self.last_displayed_forms_to_director = forms_to_display
