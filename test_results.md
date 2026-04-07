# Kết quả kiểm thử - TravelBuddy Agent

## Test 1 – Trả lời trực tiếp (Không cần tool)

**Người dùng:** "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu."

**Kỳ vọng:** Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

**Kết quả:**
```
Trả lời trực tiếp
TravelBuddy: Chào bạn! Bạn đang có ý định đi du lịch vào thời gian nào? Và bạn thích
những loại điểm đến nào, ví dụ như biển, núi, hay thành phố? Ngoài ra, bạn có ngân sách
nhất định cho chuyến đi không?
```

**Đánh giá:** PASS – Agent không gọi tool, hỏi thêm thông tin từ người dùng (thời gian, sở thích, ngân sách).

---

## Test 2 – Gọi một tool duy nhất (Single Tool Call)

**Người dùng:** "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng"

**Kỳ vọng:** Gọi `search_flights("Hà Nội", "Đà Nẵng")`, liệt kê 4 chuyến bay.

**Kết quả:**
```
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
Trả lời trực tiếp
TravelBuddy: Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng:

1. Vietnam Airlines
   - Giờ bay: 06:00 → 07:20
   - Hạng ghế: Economy
   - Giá: 1.450.000đ

2. Vietnam Airlines
   - Giờ bay: 14:00 → 15:20
   - Hạng ghế: Business
   - Giá: 2.800.000đ

3. VietJet Air
   - Giờ bay: 08:30 → 09:50
   - Hạng ghế: Economy
   - Giá: 890.000đ

4. Bamboo Airways
   - Giờ bay: 11:00 → 12:20
   - Hạng ghế: Economy
   - Giá: 1.200.000đ
```

**Đánh giá:** PASS – Gọi đúng `search_flights`, liệt kê đủ 4 chuyến bay với đầy đủ thông tin giá vé.

---

## Test 3 – Chuỗi nhiều tool (Multi-Step Tool Chaining)

**Người dùng:** "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!"

**Kỳ vọng:** Agent phải tự chuỗi nhiều bước: tìm vé rẻ nhất → tính ngân sách → tìm khách sạn → gợi ý điểm tham quan → tổng hợp.

**Kết quả:**
```
Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000'})
Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 1950000})
Gọi tool: search_attractions({'city': 'Phú Quốc'})
Trả lời trực tiếp

TravelBuddy: Tư vấn chuyến đi Phú Quốc

Chuyến bay:
- VietJet Air: 16:00 → 18:15, giá vé: 1.100.000đ

Khách sạn:
- 9Station Hostel: 200.000đ/đêm, đánh giá 4.5/5, khu vực Dương Đông.
- Sol by Meliá: 1.500.000đ/đêm, đánh giá 4.2/5, khu vực Bãi Trường.

Tổng chi phí ước tính:
- Vé máy bay: 1.100.000đ
- Khách sạn (9Station): 400.000đ (hoặc Sol by Meliá: 3.000.000đ)
- Tổng tối thiểu: 1.500.000đ, tối đa: 4.100.000đ

Gợi ý điểm tham quan:
- VinWonders Phú Quốc: 880.000đ
- Safari Phú Quốc: 650.000đ
- Nhà tù Phú Quốc: Miễn phí
- Chợ đêm Dinh Cậu: Miễn phí
```

**Đánh giá:** PASS – Agent tự động chuỗi 4 tools (search_flights → calculate_budget → search_hotels → search_attractions). Chọn đúng vé rẻ nhất (1.100.000đ), đưa ra 2 phương án khách sạn trong ngân sách, và gợi ý điểm tham quan kèm giá vé.

---

## Test 4 – Thiếu thông tin / Hỏi lại (Clarification)

**Người dùng:** "Tôi muốn đặt khách sạn"

**Kỳ vọng:** Agent hỏi lại: thành phố nào? ngân sách bao nhiêu? Không gọi tool vội.

**Kết quả:**
```
Trả lời trực tiếp
TravelBuddy: Bạn có thể cho mình biết thành phố mà bạn muốn đặt khách sạn và ngân sách
tối đa mỗi đêm không?
```

**Đánh giá:** PASS – Agent không gọi tool, hỏi lại 2 thông tin cần thiết (thành phố và ngân sách).

---

## Test 5 – Từ chối yêu cầu ngoài phạm vi (Guardrail / Refusal)

**Người dùng:** "Giải giúp tôi bài tập lập trình Python về linked list"

**Kỳ vọng:** Từ chối lịch sự, nói rằng chỉ hỗ trợ về du lịch.

**Kết quả:**
```
Trả lời trực tiếp
TravelBuddy: Xin lỗi, nhưng mình không thể giúp bạn về lập trình hay bài tập liên quan
đến Python. Tuy nhiên, nếu bạn cần thông tin về du lịch, đặt vé, khách sạn, mình rất
vui lòng hỗ trợ bạn!
```

**Đánh giá:** PASS – Từ chối lịch sự, hướng dẫn người dùng về đúng phạm vi hỗ trợ.

---

## Tổng kết

| Test | Kết quả | Ghi chú |
|:-----|:--------|:--------|
| Test 1 – Trả lời trực tiếp | PASS | Không gọi tool, hỏi thêm thông tin |
| Test 2 – Gọi một tool | PASS | Gọi đúng search_flights, đủ 4 kết quả |
| Test 3 – Chuỗi nhiều tool | PASS | Chuỗi 4 tools thành công, chọn vé rẻ nhất |
| Test 4 – Hỏi lại thông tin | PASS | Không gọi tool, hỏi lại thành phố + ngân sách |
| Test 5 – Từ chối ngoài phạm vi | PASS | Từ chối lịch sự, đúng phạm vi |

**Tất cả 5/5 test cases agent PASSED.**
