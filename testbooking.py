import unittest
from datetime import datetime
from collections import defaultdict

# Simulasi Database
# Data Booking 
database_data = [
    {"id": 1001, "Booking_id": "BK/000001", "venue_id": 15, "User_id": 12, "date": "2022-12-10", "Start_time": "09:00:00", "end_time": "11:00:00", "price": 1200000},
    {"id": 1005, "Booking_id": "BK/000005", "venue_id": 15, "User_id": 12, "date": "2022-12-10", "Start_time": "09:00:00", "end_time": "11:00:00", "price": 1000000}
]

# Database jadwal dan harga yang disimpan
schedule_data = [
    {"id": 11, "venue_id": 15, "date": "2022-12-10", "start_time": "07:00:00", "end_time": "09:00:00", "price": 800000},
    {"id": 12, "venue_id": 15, "date": "2022-12-10", "start_time": "09:00:00", "end_time": "11:00:00", "price": 1000000},
    {"id": 13, "venue_id": 15, "date": "2022-12-10", "start_time": "11:00:00", "end_time": "13:00:00", "price": 1200000}
]


class TestBookingPriceAndOverlap(unittest.TestCase):

    # Test konsisten Harga    
    def test_price_consistency(self):
        price_mismatch = []
        
        for booking in database_data:
            booking_date = booking["date"]
            start_time = booking["Start_time"]
            
            for schedule in schedule_data:
                if schedule["date"] == booking_date and schedule["start_time"] == start_time:
                    if schedule["price"] != booking["price"]:
                        price_mismatch.append(booking)
                    break
        
        self.assertEqual(len(price_mismatch), 0, f"Price mismatch detected: {price_mismatch}")
    
    # Test Booking Bertumpukan atau Bersamaan    
    def test_overlap_detection(self):
        overlap_detected = defaultdict(list)
        
        for i, booking1 in enumerate(database_data):
            for j, booking2 in enumerate(database_data):
                if i != j and booking1["date"] == booking2["date"]:
                    start_time1 = datetime.strptime(booking1["Start_time"], "%H:%M:%S")
                    end_time1 = datetime.strptime(booking1["end_time"], "%H:%M:%S")
                    start_time2 = datetime.strptime(booking2["Start_time"], "%H:%M:%S")
                    end_time2 = datetime.strptime(booking2["end_time"], "%H:%M:%S")
                    
                    if start_time1 < end_time2 and end_time1 > start_time2:
                        overlap_detected[booking1["date"]].append((booking1["Booking_id"], booking2["Booking_id"]))
        
        overlap_messages = []
        for date, overlaps in overlap_detected.items():
            overlap_messages.append(f"Date: {date}, Overlaps: {overlaps}")
        
        self.assertEqual(len(overlap_messages), 0, f"Overlaps detected: {overlap_messages}")

if __name__ == "__main__":
    unittest.main()
