class GuideModel:
    """Model chứa dữ liệu hướng dẫn chăm sóc cây trồng"""
    
    # Dữ liệu các loại cây
    PLANTS_DATA = {
        "cam": {
            "id": "cam",
            "name": "🍊 Cam",
            "name_vi": "Cây cam",
            "category": "Cây ăn quả",
            "image": "/static/uploads/cay_cam.jpg",
            "description": "Cây cam là loại cây ăn quả có múi, giàu vitamin C, được trồng phổ biến ở các tỉnh miền núi phía Bắc và Đồng bằng sông Cửu Long.",
            "growing_season": "Tháng 2-4 và tháng 8-10",
            "harvest_time": "Sau 3-4 năm trồng, thu hoạch vào tháng 11-12",
            "stages": [
                {"stage": "Gieo hạt/Trồng cây con", "duration": "0-6 tháng", "care": "Tưới nước đều đặn, che bớt nắng, bón lót phân chuồng"},
                {"stage": "Chăm sóc cây non", "duration": "6-24 tháng", "care": "Tỉa cành, tạo tán, bón phân định kỳ 3 tháng/lần"},
                {"stage": "Cây cho quả", "duration": "3-10 năm", "care": "Bón phân trước và sau khi thu hoạch, cắt tỉa cành già"}
            ],
            "watering": {
                "frequency": "Tưới 2-3 ngày/lần mùa khô, 5-7 ngày/lần mùa mưa",
                "amount": "20-30 lít/cây/lần đối với cây trưởng thành",
                "best_time": "Sáng sớm (6-8h)",
                "notes": "Không để cây bị úng nước, cần thoát nước tốt"
            },
            "fertilizer": {
                "types": ["Phân chuồng hoai mục", "NPK 16-16-8", "Phân hữu cơ vi sinh", "Vôi bột"],
                "schedule": [
                    {"time": "Sau thu hoạch (tháng 1-2)", "type": "Phân chuồng + NPK", "amount": "20-30kg phân chuồng + 1-2kg NPK/cây"},
                    {"time": "Trước ra hoa (tháng 8-9)", "type": "NPK + Kali", "amount": "1-1.5kg NPK + 0.5kg Kali/cây"},
                    {"time": "Nuôi quả (tháng 10-11)", "type": "Kali + vi lượng", "amount": "0.5-1kg Kali/cây"}
                ],
                "notes": "Bón phân theo hình chiếu của tán cây, xới nhẹ sau khi bón"
            },
            "diseases": [
                {"name": "Bệnh vàng lá greening", "symptom": "Lá vàng không đều, quả nhỏ lệch", "treatment": "Nhổ bỏ cây bệnh, phun thuốc trừ rầy chổng cánh"},
                {"name": "Bệnh loét (đốm mắt cua)", "symptom": "Vết bệnh màu nâu trên lá, quả", "treatment": "Phun Copper hydroxide, cắt tỉa cành bệnh"},
                {"name": "Bệnh thán thư", "symptom": "Vết bệnh màu nâu đen trên lá non", "treatment": "Phun Mancozeb, Propineb, vệ sinh vườn"}
            ],
            "pests": [
                {"name": "Rầy chổng cánh", "symptom": "Lá vàng, quăn queo", "treatment": "Phun Trebon, Actara, Applaud"},
                {"name": "Nhện đỏ", "symptom": "Lá vàng, có mạng nhện", "treatment": "Phun Ortus, Comite, Nissorun"},
                {"name": "Ruồi vàng", "symptom": "Quả bị chích, thối", "treatment": "Treo bả dính, bao trái"}
            ],
            "tips": [
                "🍃 Cắt tỉa cành tạo tán thông thoáng giúp giảm sâu bệnh",
                "💧 Tưới nước đều đặn, tránh tưới quá nhiều gây úng rễ",
                "🛡️ Phun phòng bệnh định kỳ 15-20 ngày/lần",
                "🌱 Bón bổ sung phân hữu cơ để cải tạo đất"
            ]
        },
        
        "chanh": {
            "id": "chanh",
            "name": "🍋 Chanh",
            "name_vi": "Cây chanh",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_chanh.jpg",
            "description": "Cây chanh dễ trồng, cho quả quanh năm, được trồng phổ biến ở nhiều vùng miền.",
            "growing_season": "Quanh năm",
            "harvest_time": "Sau 2-3 năm, thu hoạch sau khi trồng 8-10 tháng",
            "stages": [
                {"stage": "Trồng cây con", "duration": "0-6 tháng", "care": "Tưới nước thường xuyên, che bớt nắng"},
                {"stage": "Chăm sóc cây non", "duration": "6-24 tháng", "care": "Tỉa cành, tạo tán, bón phân 2 tháng/lần"},
                {"stage": "Cây cho quả", "duration": "2-10 năm", "care": "Bón phân sau mỗi đợt thu hoạch"}
            ],
            "watering": {
                "frequency": "Tưới 2 ngày/lần mùa khô, 5-7 ngày/lần mùa mưa",
                "amount": "15-25 lít/cây/lần",
                "best_time": "Sáng sớm (6-8h)",
                "notes": "Chanh ưa ẩm nhưng không chịu úng"
            },
            "fertilizer": {
                "types": ["Phân chuồng", "NPK 20-20-15", "Phân hữu cơ", "Đạm cá"],
                "schedule": [
                    {"time": "Sau thu hoạch", "type": "Phân chuồng + NPK", "amount": "15-20kg phân chuồng + 0.5-1kg NPK/cây"},
                    {"time": "Trước ra hoa", "type": "NPK + Kali", "amount": "0.5kg NPK + 0.3kg Kali/cây"},
                    {"time": "Nuôi quả", "type": "Kali + vi lượng", "amount": "0.3-0.5kg Kali/cây"}
                ],
                "notes": "Bón phân làm nhiều đợt, không bón quá tập trung"
            },
            "diseases": [
                {"name": "Bệnh loét", "symptom": "Vết bệnh nổi cộm trên lá, quả", "treatment": "Phun Copper hydroxide, cắt tỉa cành bệnh"},
                {"name": "Bệnh thán thư", "symptom": "Lá cháy mép, quả bị thối", "treatment": "Phun Mancozeb, Carbendazim"},
                {"name": "Bệnh phấn trắng", "symptom": "Lớp phấn trắng trên lá non", "treatment": "Phun Anvil, Score, Tilt"}
            ],
            "pests": [
                {"name": "Rầy mềm", "symptom": "Lá quăn, chồi non héo", "treatment": "Phun Confidor, Actara"},
                {"name": "Sâu vẽ bùa", "symptom": "Lá có đường ngoằn ngoèo", "treatment": "Phun Vertimec, Pegasus"},
                {"name": "Nhện đỏ", "symptom": "Lá vàng, có mạng", "treatment": "Phun Ortus, Nissorun"}
            ],
            "tips": [
                "🍋 Chanh ưa ánh sáng, nên trồng nơi thoáng đãng",
                "💧 Tưới nước đều đặn, nhất là giai đoạn ra hoa, đậu quả",
                "✂️ Cắt tỉa cành già, cành bệnh để cây thông thoáng"
            ]
        },
        
        "dua_hau": {
            "id": "dua_hau",
            "name": "🍉 Dưa hấu",
            "name_vi": "Cây dưa hấu",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_dua_hau.jpg",
            "description": "Cây dưa hấu là loại cây thân leo, quả to, nhiều nước, được trồng nhiều ở các tỉnh Nam Trung Bộ.",
            "growing_season": "Tháng 10-12 (vụ Đông) hoặc tháng 2-4 (vụ Xuân Hè)",
            "harvest_time": "Sau 65-75 ngày trồng",
            "stages": [
                {"stage": "Gieo hạt - Nảy mầm", "duration": "5-7 ngày", "care": "Giữ ẩm, che phủ nilon"},
                {"stage": "Cây con", "duration": "15-20 ngày", "care": "Tưới nước nhẹ, bón phân lót"},
                {"stage": "Cây leo - Ra hoa", "duration": "25-30 ngày", "care": "Làm giàn, tưới đủ ẩm, bón thúc"},
                {"stage": "Đậu quả - Nuôi quả", "duration": "25-30 ngày", "care": "Tưới nước đều, bón kali, phòng bệnh"}
            ],
            "watering": {
                "frequency": "Tưới 2 ngày/lần mùa khô, 4-5 ngày/lần mùa mưa",
                "amount": "15-20 lít/m²/lần",
                "best_time": "Sáng sớm (6-8h)",
                "notes": "Dưa hấu cần nước nhưng không chịu úng, cần thoát nước tốt"
            },
            "fertilizer": {
                "types": ["Phân chuồng", "NPK 15-15-15", "Phân bón lá", "Kali"],
                "schedule": [
                    {"time": "Bón lót trước trồng", "type": "Phân chuồng + NPK", "amount": "1-1.5 tấn phân chuồng + 50kg NPK/ha"},
                    {"time": "Bón thúc lần 1 (10-15 ngày)", "type": "NPK + Ure", "amount": "30kg NPK + 20kg Ure/ha"},
                    {"time": "Bón thúc lần 2 (25-30 ngày)", "type": "NPK + Kali", "amount": "40kg NPK + 30kg Kali/ha"},
                    {"time": "Bón nuôi quả (40-45 ngày)", "type": "Kali", "amount": "30-40kg Kali/ha"}
                ],
                "notes": "Không bón phân khi trời mưa, tưới nước sau khi bón"
            },
            "diseases": [
                {"name": "Bệnh phấn trắng", "symptom": "Lớp phấn trắng trên lá", "treatment": "Phun Anvil, Score, Tilt"},
                {"name": "Bệnh sương mai", "symptom": "Lá có đốm vàng, cháy lá", "treatment": "Phun Ridomil, Mancozeb"},
                {"name": "Bệnh thối trái", "symptom": "Quả bị thối, có nấm", "treatment": "Phun Copper, Carbendazim, vệ sinh vườn"}
            ],
            "pests": [
                {"name": "Rệp bông", "symptom": "Lá quăn, chồi non héo", "treatment": "Phun Confidor, Actara"},
                {"name": "Nhện đỏ", "symptom": "Lá vàng, có mạng", "treatment": "Phun Ortus, Nissorun"},
                {"name": "Sâu xanh", "symptom": "Cắn phá lá non", "treatment": "Phun Dipel, BT, Karate"}
            ],
            "tips": [
                "🍉 Chọn giống dưa hấu phù hợp với mùa vụ",
                "💧 Ngưng tưới 7-10 ngày trước thu hoạch để tăng độ ngọt",
                "🌱 Làm giàn hoặc cho leo trên rơm rạ để tránh thối quả",
                "🛡️ Phun phòng bệnh định kỳ 7-10 ngày/lần"
            ]
        },
        
        "le": {
            "id": "le",
            "name": "🍐 Lê",
            "name_vi": "Cây lê",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_le.jpg",
            "description": "Cây lê thích hợp trồng ở vùng khí hậu mát mẻ như Sa Pa, Bảo Lộc, Đà Lạt.",
            "growing_season": "Tháng 1-3",
            "harvest_time": "Sau 3-4 năm, thu hoạch vào tháng 7-9",
            "stages": [
                {"stage": "Trồng cây con", "duration": "0-12 tháng", "care": "Che bớt nắng, tưới đủ ẩm"},
                {"stage": "Phát triển thân lá", "duration": "1-3 năm", "care": "Tạo tán, cắt tỉa, bón phân định kỳ"},
                {"stage": "Ra hoa - Đậu quả", "duration": "Tháng 2-3", "care": "Tỉa hoa, tỉa quả non"},
                {"stage": "Nuôi quả - Thu hoạch", "duration": "Tháng 4-8", "care": "Bón kali, tưới đủ ẩm, bao quả"}
            ],
            "watering": {
                "frequency": "Tưới 3-4 ngày/lần mùa khô, 7-10 ngày/lần mùa mưa",
                "amount": "30-50 lít/cây/lần",
                "best_time": "Sáng sớm (6-8h)",
                "notes": "Lê cần đủ nước nhưng không chịu úng"
            },
            "fertilizer": {
                "types": ["Phân chuồng hoai", "NPK 20-20-15", "Phân hữu cơ", "Vôi"],
                "schedule": [
                    {"time": "Sau thu hoạch (tháng 9-10)", "type": "Phân chuồng + NPK", "amount": "30-40kg phân chuồng + 2kg NPK/cây"},
                    {"time": "Trước ra hoa (tháng 12-1)", "type": "NPK + Kali", "amount": "1.5kg NPK + 1kg Kali/cây"},
                    {"time": "Nuôi quả (tháng 3-4)", "type": "Kali + vi lượng", "amount": "1-1.5kg Kali/cây"}
                ],
                "notes": "Bón phân theo hình chiếu tán cây"
            },
            "diseases": [
                {"name": "Bệnh đốm lá", "symptom": "Đốm nâu trên lá", "treatment": "Phun Mancozeb, Carbendazim"},
                {"name": "Bệnh thán thư", "symptom": "Vết bệnh trên quả", "treatment": "Phun Copper, Propineb"},
                {"name": "Bệnh rỉ sắt", "symptom": "Vết màu vàng cam trên lá", "treatment": "Phun Anvil, Score"}
            ],
            "pests": [
                {"name": "Rầy xanh", "symptom": "Chồi non quăn", "treatment": "Phun Actara, Confidor"},
                {"name": "Nhện đỏ", "symptom": "Lá vàng, rụng sớm", "treatment": "Phun Ortus, Nissorun"},
                {"name": "Sâu đục thân", "symptom": "Cành héo đột ngột", "treatment": "Cắt bỏ cành bị hại, phun Regent"}
            ],
            "tips": [
                "🍐 Lê cần nhiệt độ mát (15-25°C) để cho quả ngon",
                "✂️ Cắt tỉa cành tạo tán thông thoáng",
                "💧 Tưới nước đều đặn, nhất là giai đoạn nuôi quả"
            ]
        },
        
        "oi": {
            "id": "oi",
            "name": "🍏 Ổi",
            "name_vi": "Cây ổi",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_oi.jpg",
            "description": "Cây ổi dễ trồng, cho quả quanh năm, được trồng phổ biến ở nhiều vùng.",
            "growing_season": "Quanh năm",
            "harvest_time": "Sau 1-2 năm, thu hoạch sau trồng 6-8 tháng",
            "stages": [
                {"stage": "Trồng cây con", "duration": "0-3 tháng", "care": "Tưới nước đều, che bớt nắng"},
                {"stage": "Chăm sóc cây non", "duration": "3-12 tháng", "care": "Tạo tán, bón phân 2 tháng/lần"},
                {"stage": "Ra hoa - Đậu quả", "duration": "Liên tục", "care": "Bón phân sau mỗi đợt thu hoạch"}
            ],
            "watering": {
                "frequency": "Tưới 1-2 ngày/lần mùa khô, 3-4 ngày/lần mùa mưa",
                "amount": "10-20 lít/cây/lần",
                "best_time": "Sáng sớm hoặc chiều mát",
                "notes": "Ổi ưa ẩm, cần tưới đủ nước"
            },
            "fertilizer": {
                "types": ["Phân chuồng", "NPK 20-20-15", "Phân hữu cơ", "Đạm cá"],
                "schedule": [
                    {"time": "Bón lót khi trồng", "type": "Phân chuồng + NPK", "amount": "10-15kg phân chuồng + 0.3kg NPK/cây"},
                    {"time": "Bón thúc (2 tháng/lần)", "type": "NPK", "amount": "0.3-0.5kg NPK/cây"},
                    {"time": "Sau thu hoạch", "type": "Phân chuồng + NPK", "amount": "10kg phân chuồng + 0.3kg NPK/cây"}
                ],
                "notes": "Bón phân xung quanh gốc, xới nhẹ"
            },
            "diseases": [
                {"name": "Bệnh thán thư", "symptom": "Quả bị đốm đen, thối", "treatment": "Phun Mancozeb, Carbendazim"},
                {"name": "Bệnh phấn trắng", "symptom": "Lớp phấn trắng trên lá", "treatment": "Phun Anvil, Score"},
                {"name": "Bệnh đốm dầu", "symptom": "Vết bệnh đen trên lá", "treatment": "Phun Copper hydroxide"}
            ],
            "pests": [
                {"name": "Rầy mềm", "symptom": "Chồi non quăn", "treatment": "Phun Confidor, Actara"},
                {"name": "Ruồi đục quả", "symptom": "Quả bị thối, có lỗ", "treatment": "Bao quả, treo bả dính"},
                {"name": "Sâu đục thân", "symptom": "Cây héo, thân có lỗ", "treatment": "Cắt cành bị hại, bơm thuốc vào lỗ"}
            ],
            "tips": [
                "🍏 Ổi rất dễ trồng, thích hợp với nhiều loại đất",
                "✂️ Cắt tỉa thường xuyên để cây ra nhiều quả",
                "🌱 Bón phân hữu cơ để quả ngọt và thơm hơn"
            ]
        },
        
        "xoai": {
            "id": "xoai",
            "name": "🥭 Xoài",
            "name_vi": "Cây xoài",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_xoai.jpg",
            "description": "Cây xoài được trồng nhiều ở Đồng bằng sông Cửu Long, đặc biệt là xoài cát Hòa Lộc.",
            "growing_season": "Tháng 10-12",
            "harvest_time": "Sau 3-4 năm, thu hoạch vào tháng 3-5",
            "stages": [
                {"stage": "Trồng cây con", "duration": "0-12 tháng", "care": "Tưới nước đều, che bớt nắng, bón lót"},
                {"stage": "Phát triển thân lá", "duration": "1-3 năm", "care": "Tạo tán, cắt tỉa, bón phân 3 tháng/lần"},
                {"stage": "Ra hoa - Đậu quả", "duration": "Tháng 12-1", "care": "Xiết nước, phun thuốc kích thích ra hoa"},
                {"stage": "Nuôi quả - Thu hoạch", "duration": "Tháng 2-5", "care": "Bón kali, tưới đủ ẩm, bao quả"}
            ],
            "watering": {
                "frequency": "Tưới 3-4 ngày/lần mùa khô, 7-10 ngày/lần mùa mưa",
                "amount": "40-60 lít/cây/lần",
                "best_time": "Sáng sớm (6-8h)",
                "notes": "Xoài cần xiết nước trước khi ra hoa 2-3 tháng"
            },
            "fertilizer": {
                "types": ["Phân chuồng", "NPK 20-20-15", "Phân hữu cơ", "Kali"],
                "schedule": [
                    {"time": "Sau thu hoạch", "type": "Phân chuồng + NPK", "amount": "30-40kg phân chuồng + 2kg NPK/cây"},
                    {"time": "Trước ra hoa (tháng 9-10)", "type": "NPK + Kali", "amount": "1.5kg NPK + 1kg Kali/cây"},
                    {"time": "Nuôi quả (tháng 2-3)", "type": "Kali", "amount": "1-1.5kg Kali/cây"}
                ],
                "notes": "Bón phân sau khi tưới nước, xới nhẹ"
            },
            "diseases": [
                {"name": "Bệnh thán thư", "symptom": "Đốm đen trên lá, quả", "treatment": "Phun Mancozeb, Carbendazim"},
                {"name": "Bệnh phấn trắng", "symptom": "Lớp phấn trắng trên chùm hoa", "treatment": "Phun Anvil, Score"},
                {"name": "Bệnh đốm dầu", "symptom": "Vết bệnh nâu đen trên lá", "treatment": "Phun Copper hydroxide"}
            ],
            "pests": [
                {"name": "Rầy xanh", "symptom": "Chùm hoa bị khô", "treatment": "Phun Actara, Confidor"},
                {"name": "Ruồi đục quả", "symptom": "Quả bị thối, có lỗ", "treatment": "Bao quả, treo bả dính"},
                {"name": "Sâu đục thân", "symptom": "Cành héo đột ngột", "treatment": "Cắt bỏ cành bị hại"}
            ],
            "tips": [
                "🥭 Xoài cần xiết nước 2-3 tháng trước khi ra hoa",
                "✂️ Cắt tỉa cành sau thu hoạch để cây ra lộc mới",
                "🌱 Bón kali nhiều hơn đạm để quả ngọt"
            ]
        },
        
        "vai": {
            "id": "vai",
            "name": "🍒 Vải",
            "name_vi": "Cây vải",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_vai.jpg",
            "description": "Cây vải nổi tiếng ở vùng Lục Ngạn (Bắc Giang), Thanh Hà (Hải Dương).",
            "growing_season": "Tháng 2-3",
            "harvest_time": "Sau 4-5 năm, thu hoạch vào tháng 5-6",
            "stages": [
                {"stage": "Trồng cây con", "duration": "0-12 tháng", "care": "Che bớt nắng, tưới đủ ẩm"},
                {"stage": "Phát triển thân lá", "duration": "1-4 năm", "care": "Tạo tán, cắt tỉa, bón phân định kỳ"},
                {"stage": "Ra hoa - Đậu quả", "duration": "Tháng 2-3", "care": "Xiết nước, phun thuốc kích thích ra hoa"},
                {"stage": "Nuôi quả - Thu hoạch", "duration": "Tháng 4-6", "care": "Bón kali, tưới đủ ẩm"}
            ],
            "watering": {
                "frequency": "Tưới 5-7 ngày/lần mùa khô, 10-15 ngày/lần mùa mưa",
                "amount": "40-60 lít/cây/lần",
                "best_time": "Sáng sớm",
                "notes": "Vải cần xiết nước trước ra hoa 1-2 tháng"
            },
            "fertilizer": {
                "types": ["Phân chuồng", "NPK 20-20-15", "Phân hữu cơ", "Kali"],
                "schedule": [
                    {"time": "Sau thu hoạch", "type": "Phân chuồng + NPK", "amount": "30-40kg phân chuồng + 2kg NPK/cây"},
                    {"time": "Trước ra hoa (tháng 12-1)", "type": "NPK + Kali", "amount": "1.5kg NPK + 1kg Kali/cây"},
                    {"time": "Nuôi quả (tháng 3-4)", "type": "Kali", "amount": "1-1.5kg Kali/cây"}
                ],
                "notes": "Bón phân sau khi tưới nước"
            },
            "diseases": [
                {"name": "Bệnh thán thư", "symptom": "Đốm đen trên lá, quả", "treatment": "Phun Mancozeb, Carbendazim"},
                {"name": "Bệnh sương mai", "symptom": "Lá có đốm vàng", "treatment": "Phun Ridomil, Mancozeb"},
                {"name": "Bệnh cháy lá", "symptom": "Lá khô cháy", "treatment": "Phun Copper hydroxide"}
            ],
            "pests": [
                {"name": "Rầy xanh", "symptom": "Chùm hoa khô", "treatment": "Phun Actara, Confidor"},
                {"name": "Sâu đục quả", "symptom": "Quả bị đục lỗ", "treatment": "Phun BT, Dipel"},
                {"name": "Nhện lông nhung", "symptom": "Lá có lông màu nâu", "treatment": "Phun Ortus, Nissorun"}
            ],
            "tips": [
                "🍒 Vải cần nhiệt độ mát (15-25°C) để ra hoa",
                "✂️ Cắt tỉa cành sau thu hoạch",
                "💧 Xiết nước trước khi ra hoa 1-2 tháng"
            ]
        },
        
        "buoi": {
            "id": "buoi",
            "name": "🍊 Bưởi",
            "name_vi": "Cây bưởi",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_buoi.jpg",
            "description": "Cây bưởi nổi tiếng với bưởi Năm Roi (Vĩnh Long), bưởi Diễn (Hà Nội), bưởi Đoan Hùng (Phú Thọ).",
            "growing_season": "Tháng 2-4",
            "harvest_time": "Sau 3-4 năm, thu hoạch vào tháng 8-10",
            "stages": [
                {"stage": "Trồng cây con", "duration": "0-12 tháng", "care": "Che bớt nắng, tưới đủ ẩm"},
                {"stage": "Phát triển thân lá", "duration": "1-3 năm", "care": "Tạo tán, cắt tỉa, bón phân định kỳ"},
                {"stage": "Ra hoa - Đậu quả", "duration": "Tháng 2-3", "care": "Phun thuốc kích thích ra hoa"},
                {"stage": "Nuôi quả - Thu hoạch", "duration": "Tháng 4-9", "care": "Bón kali, tưới đủ ẩm, bao quả"}
            ],
            "watering": {
                "frequency": "Tưới 3-4 ngày/lần mùa khô, 7-10 ngày/lần mùa mưa",
                "amount": "40-60 lít/cây/lần",
                "best_time": "Sáng sớm",
                "notes": "Bưởi cần đủ nước nhưng không chịu úng"
            },
            "fertilizer": {
                "types": ["Phân chuồng", "NPK 20-20-15", "Phân hữu cơ", "Kali", "Vôi"],
                "schedule": [
                    {"time": "Sau thu hoạch (tháng 10-11)", "type": "Phân chuồng + NPK", "amount": "30-40kg phân chuồng + 2kg NPK/cây"},
                    {"time": "Trước ra hoa (tháng 12-1)", "type": "NPK + Kali", "amount": "1.5kg NPK + 1kg Kali/cây"},
                    {"time": "Nuôi quả (tháng 3-4)", "type": "Kali + vi lượng", "amount": "1-1.5kg Kali/cây"}
                ],
                "notes": "Bón vôi 2 lần/năm để cải tạo đất"
            },
            "diseases": [
                {"name": "Bệnh vàng lá greening", "symptom": "Lá vàng, quả nhỏ", "treatment": "Nhổ bỏ cây bệnh, phun thuốc trừ rầy"},
                {"name": "Bệnh loét", "symptom": "Vết loét trên lá, quả", "treatment": "Phun Copper hydroxide"},
                {"name": "Bệnh thán thư", "symptom": "Quả bị đốm đen", "treatment": "Phun Mancozeb, Carbendazim"}
            ],
            "pests": [
                {"name": "Rầy chổng cánh", "symptom": "Lá vàng, quăn", "treatment": "Phun Actara, Confidor"},
                {"name": "Nhện đỏ", "symptom": "Lá vàng, có mạng", "treatment": "Phun Ortus, Nissorun"},
                {"name": "Ruồi vàng", "symptom": "Quả bị chích", "treatment": "Bao quả, treo bả dính"}
            ],
            "tips": [
                "🍊 Bưởi cần bón vôi định kỳ để giảm chua đất",
                "✂️ Cắt tỉa cành tạo tán thông thoáng",
                "🌱 Bón phân hữu cơ để quả ngọt hơn"
            ]
        },
        
        "nhan": {
            "id": "nhan",
            "name": "🫘 Nhãn",
            "name_vi": "Cây nhãn",
            "category": "Cây ăn quả",
            "image": "static/uploads/cay_nhan.jpg",
            "description": "Cây nhãn nổi tiếng ở Hưng Yên, Đồng Tháp, Vĩnh Long.",
            "growing_season": "Tháng 2-3",
            "harvest_time": "Sau 4-5 năm, thu hoạch vào tháng 7-8",
            "stages": [
                {"stage": "Trồng cây con", "duration": "0-12 tháng", "care": "Che bớt nắng, tưới đủ ẩm"},
                {"stage": "Phát triển thân lá", "duration": "1-4 năm", "care": "Tạo tán, cắt tỉa, bón phân định kỳ"},
                {"stage": "Ra hoa - Đậu quả", "duration": "Tháng 2-3", "care": "Xiết nước, phun thuốc kích thích ra hoa"},
                {"stage": "Nuôi quả - Thu hoạch", "duration": "Tháng 4-7", "care": "Bón kali, tưới đủ ẩm"}
            ],
            "watering": {
                "frequency": "Tưới 4-5 ngày/lần mùa khô, 10-15 ngày/lần mùa mưa",
                "amount": "40-60 lít/cây/lần",
                "best_time": "Sáng sớm",
                "notes": "Nhãn cần xiết nước trước ra hoa 2-3 tháng"
            },
            "fertilizer": {
                "types": ["Phân chuồng", "NPK 20-20-15", "Phân hữu cơ", "Kali"],
                "schedule": [
                    {"time": "Sau thu hoạch (tháng 8-9)", "type": "Phân chuồng + NPK", "amount": "30-40kg phân chuồng + 2kg NPK/cây"},
                    {"time": "Trước ra hoa (tháng 11-12)", "type": "NPK + Kali", "amount": "1.5kg NPK + 1kg Kali/cây"},
                    {"time": "Nuôi quả (tháng 3-4)", "type": "Kali", "amount": "1-1.5kg Kali/cây"}
                ],
                "notes": "Bón phân sau khi tưới nước"
            },
            "diseases": [
                {"name": "Bệnh thán thư", "symptom": "Quả bị đốm đen", "treatment": "Phun Mancozeb, Carbendazim"},
                {"name": "Bệnh cháy lá", "symptom": "Lá khô cháy", "treatment": "Phun Copper hydroxide"},
                {"name": "Bệnh phấn trắng", "symptom": "Lớp phấn trắng trên chùm hoa", "treatment": "Phun Anvil, Score"}
            ],
            "pests": [
                {"name": "Rầy xanh", "symptom": "Chùm hoa khô", "treatment": "Phun Actara, Confidor"},
                {"name": "Sâu đục quả", "symptom": "Quả bị đục lỗ", "treatment": "Phun BT, Dipel"},
                {"name": "Nhện lông nhung", "symptom": "Lá có lông màu nâu", "treatment": "Phun Ortus, Nissorun"}
            ],
            "tips": [
                "🫘 Nhãn cần xiết nước trước ra hoa 2-3 tháng",
                "✂️ Cắt tỉa cành sau thu hoạch",
                "🌱 Bón kali nhiều để quả ngọt"
            ]
        }
    }
    
    @staticmethod
    def get_all_plants():
        """Lấy danh sách tất cả cây trồng"""
        return list(GuideModel.PLANTS_DATA.values())
    
    @staticmethod
    def get_plant_by_id(plant_id):
        """Lấy thông tin cây trồng theo ID"""
        return GuideModel.PLANTS_DATA.get(plant_id)
    
    @staticmethod
    def get_plants_by_category(category):
        """Lấy cây trồng theo danh mục"""
        return [plant for plant in GuideModel.PLANTS_DATA.values() if plant.get("category") == category]
    
    @staticmethod
    def search_plants(keyword):
        """Tìm kiếm cây trồng"""
        if not keyword:
            return GuideModel.get_all_plants()
        
        keyword_lower = keyword.lower()
        return [
            plant for plant in GuideModel.PLANTS_DATA.values()
            if keyword_lower in plant["name"].lower() or keyword_lower in plant["name_vi"].lower()
        ]