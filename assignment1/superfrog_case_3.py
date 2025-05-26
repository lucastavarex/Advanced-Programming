import datetime

class SuperFrogRequestManager:
    def __init__(self):
        self.requests_list = []

    def request(self, user_id_param, s_date, f_date):
        actual_user_id = user_id_param if user_id_param else "superfrog"

        return {
            "Request": {
                "RequestId": f"{actual_user_id}_{s_date}_{f_date}",
                "Parameters": {
                    "userId": f"{actual_user_id}",
                    "startDate": f"{s_date}",
                    "endDate": f"{f_date}",  
                    "Status": "Pending"
                }
            }
        }

    def change_request_status(self, request_payload, status):
        if status in ["Pending", "Completed", "Rejected"]:
            request_payload["Request"]["Parameters"]["Status"] = status
        else:
            return("Status invalido. Use 'Completed', 'Pending', ou 'Rejected'.")
        return request_payload 

    def save_request(self, user_id, start_date, end_date):
        new_request_payload = self.request(user_id, start_date, end_date)
        self.requests_list.append(new_request_payload)
        return new_request_payload

    def clear_requests(self):
        self.requests_list.clear()

    def get_all_requests(self):
        return self.requests_list

    def filter_requests(self, filter_criteria, start_date_str=None, end_date_str=None):
        if filter_criteria not in ["Pending", "Completed", "Rejected"]:
            return "Invalid filter. Please use 'Pending', 'Completed', or 'Rejected'."

        filtered_list = []
        
        filter_dt_start = None
        filter_dt_end = None

        if start_date_str and end_date_str:
            try:
                filter_dt_start = datetime.datetime.strptime(start_date_str, "%d-%m-%y")
                filter_dt_end = datetime.datetime.strptime(end_date_str, "%d-%m-%y")
                if filter_dt_start > filter_dt_end:
                    return "Start date cannot be after end date. Please check your input."
            except ValueError:
                return "Date format error: expected 'dd-mm-yy'."
        elif start_date_str or end_date_str: 
            return "Both start and end dates must be provided for filtering, or leave both empty."

        for req_payload in self.requests_list:
            req_params = req_payload["Request"]["Parameters"]
            
            if req_params["Status"] == filter_criteria:
                if filter_dt_start and filter_dt_end:
                    try:
                        req_dt_start = datetime.datetime.strptime(req_params["startDate"], "%d-%m-%y")
                        req_dt_end = datetime.datetime.strptime(req_params["endDate"], "%d-%m-%y")
                    except ValueError:
                        continue 

                    date_condition_met = (
                        (filter_dt_start <= req_dt_start <= filter_dt_end) or \
                        (filter_dt_start <= req_dt_end <= filter_dt_end)
                    )
                    
                    if date_condition_met:
                        filtered_list.append(req_payload)
                else:
                    filtered_list.append(req_payload)
                    
        if not filtered_list:
            return "No requests found with the specified filter and date range."
        else:
            return filtered_list
