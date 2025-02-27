from locust import HttpUser, task, between

class ReservationUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def reserve_seat(self):
        test_seat_id = "A1"  # 使用固定座位测试并发
        self.client.post("/reserve/", {
            "seat_id": test_seat_id,
            "start_time": "2024-03-20T14:00",
            "end_time": "2024-03-20T16:00"
        })
