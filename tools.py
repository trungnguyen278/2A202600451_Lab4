from langchain_core.tools import tool

# ==========================================================
# MOCK DATA - Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ==========================================================

ATTRACTIONS_DB = {
    "Đà Nẵng": [
        {"name": "Bà Nà Hills", "type": "Công viên giải trí", "price": 900_000, "rating": 4.5, "duration": "1 ngày"},
        {"name": "Cầu Vàng", "type": "Điểm tham quan", "price": 0, "rating": 4.8, "duration": "1-2 giờ"},
        {"name": "Ngũ Hành Sơn", "type": "Di tích lịch sử", "price": 40_000, "rating": 4.3, "duration": "2-3 giờ"},
        {"name": "Bảo tàng Chăm", "type": "Bảo tàng", "price": 60_000, "rating": 4.1, "duration": "1-2 giờ"},
    ],
    "Phú Quốc": [
        {"name": "VinWonders Phú Quốc", "type": "Công viên giải trí", "price": 880_000, "rating": 4.6, "duration": "1 ngày"},
        {"name": "Safari Phú Quốc", "type": "Vườn thú", "price": 650_000, "rating": 4.4, "duration": "Nửa ngày"},
        {"name": "Nhà tù Phú Quốc", "type": "Di tích lịch sử", "price": 0, "rating": 4.2, "duration": "1-2 giờ"},
        {"name": "Chợ đêm Dinh Cậu", "type": "Chợ đêm", "price": 0, "rating": 4.3, "duration": "Buổi tối"},
    ],
    "Hồ Chí Minh": [
        {"name": "Địa đạo Củ Chi", "type": "Di tích lịch sử", "price": 110_000, "rating": 4.5, "duration": "Nửa ngày"},
        {"name": "Dinh Độc Lập", "type": "Di tích lịch sử", "price": 65_000, "rating": 4.4, "duration": "1-2 giờ"},
        {"name": "Chợ Bến Thành", "type": "Chợ", "price": 0, "rating": 4.0, "duration": "1-2 giờ"},
        {"name": "Bảo tàng Chứng tích Chiến tranh", "type": "Bảo tàng", "price": 40_000, "rating": 4.6, "duration": "2-3 giờ"},
    ],
}


FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air", "departure": "08:30", "arrival": "09:50", "price": 890_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "07:30", "arrival": "09:40", "price": 950_000, "class": "economy"},
        {"airline": "Bamboo Airways", "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "13:00", "arrival": "14:20", "price": 780_000, "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air", "departure": "15:00", "arrival": "16:00", "price": 650_000, "class": "economy"},
    ],
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury", "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê", "rating": 4.5},
        {"name": "Sala Danang Beach", "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê", "rating": 4.3},
        {"name": "Fivitel Danang", "stars": 3, "price_per_night": 650_000, "area": "Sơn Trà", "rating": 4.1},
        {"name": "Memory Hostel", "stars": 2, "price_per_night": 250_000, "area": "Hải Châu", "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000, "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort", "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài", "rating": 4.4},
        {"name": "Sol by Meliá", "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort", "stars": 3, "price_per_night": 800_000, "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel", "stars": 2, "price_per_night": 200_000, "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel", "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central", "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel", "stars": 3, "price_per_night": 550_000, "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room", "stars": 2, "price_per_night": 180_000, "area": "Quận 1", "rating": 4.6},
    ],
}

def format_price(price: int) -> str:
    """Format giá tiền theo chuẩn Việt Nam (VD: 1.450.000đ)."""
    return f"{price:,}".replace(",", ".") + "đ"

@tool
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """

    flights = FLIGHTS_DB.get((origin, destination))
    reversed_route = False
    if not flights :
        flights = FLIGHTS_DB.get((destination, origin))
        reversed_route = True
    if not flights:
        return f"Không tìm thấy chuyến bay từ {origin} đến {destination}."
    
    
    result = []

    route_text = f"{origin} → {destination}"
    if reversed_route:
        route_text = f"{destination} → {origin} (đảo chiều)"

    result.append(f"✈️ Các chuyến bay {route_text}:\n")

    for i, f in enumerate(flights, 1):
        result.append(
            f"{i}. {f['airline']}\n"
            f"   🕒 {f['departure']} → {f['arrival']}\n"
            f"   💺 {f['class']}\n"
            f"   💰 {format_price(f['price'])}\n"
        )

    return "\n".join(result)
   
@tool
def search_hotels(city: str, max_price_per_night: int = 99999999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    hotels = HOTELS_DB.get(city)
    if not hotels:
        return f"Không có dữ liệu khách sạn tại {city}."
        
    filtered_hotels = [h for h in hotels if h["price_per_night"] <= max_price_per_night]
    
    if not filtered_hotels:
        return f"Không tìm thấy khách sạn tại {city} với giá dưới {format_price(max_price_per_night)}/đêm. Hãy thử tăng ngân sách."
        
    filtered_hotels.sort(key=lambda x: x["rating"], reverse=True)
    
    result = [f"🏨 Các khách sạn tại {city}:\n"]
    for i, h in enumerate(filtered_hotels, 1):
        result.append(
            f"{i}. {h['name']}\n"
            f"   ⭐ {h['stars']} sao | Đánh giá: {h['rating']}/5\n"
            f"   📍 Khu vực: {h['area']}\n"
            f"   💰 {format_price(h['price_per_night'])}/đêm\n"
        )
    return "\n".join(result)

@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy, 
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        expense_parts = expenses.split(',') if expenses else []
        expense_dict = {}
        for part in expense_parts:
            part = part.strip()
            if not part:
                continue
            name, amount_str = part.split(':')
            amount = int(amount_str.strip())
            name_formatted = name.strip().replace('_', ' ').capitalize()
            expense_dict[name_formatted] = amount
            
        total_expense = sum(expense_dict.values())
        remaining = total_budget - total_expense
        
        result = ["Bảng chi phí:"]
        for name, amount in expense_dict.items():
            result.append(f"- {name}: {format_price(amount)}")
            
        result.append("---")
        result.append(f"Tổng chi: {format_price(total_expense)}")
        result.append(f"Ngân sách: {format_price(total_budget)}")
        
        if remaining >= 0:
            result.append(f"Còn lại: {format_price(remaining)}")
        else:
            result.append(f"Vượt ngân sách {format_price(abs(remaining))}! Cần điều chỉnh.")
            
        return "\n".join(result)
    except ValueError:
        return "Lỗi định dạng expenses. Hãy đảm bảo format là 'tên_khoản:số_tiền', ví dụ: 'vé_máy_bay:890000,khách_sạn:650000'"
    except Exception as e:
        return f"Đã xảy ra lỗi khi tính toán ngân sách: {str(e)}"


@tool
def search_attractions(city: str) -> str:
    """
    Tìm kiếm các địa điểm du lịch, tham quan tại một thành phố.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    Trả về danh sách điểm tham quan với tên, loại hình, giá vé, đánh giá, thời gian tham quan.
    """
    attractions = ATTRACTIONS_DB.get(city)
    if not attractions:
        return f"Không có dữ liệu điểm tham quan tại {city}."

    result = [f"🎯 Các điểm tham quan tại {city}:\n"]
    for i, a in enumerate(attractions, 1):
        price_text = "Miễn phí" if a["price"] == 0 else format_price(a["price"])
        result.append(
            f"{i}. {a['name']}\n"
            f"   📌 Loại: {a['type']}\n"
            f"   🎟️ Giá vé: {price_text}\n"
            f"   ⭐ Đánh giá: {a['rating']}/5\n"
            f"   ⏱️ Thời gian: {a['duration']}\n"
        )
    return "\n".join(result)



