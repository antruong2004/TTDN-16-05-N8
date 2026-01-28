-- =====================================================
-- File SQL: Insert dữ liệu demo cho Module Kế Toán
-- Bao gồm: Kỳ kế toán, Bút toán, Chi tiết bút toán
-- =====================================================

-- Xóa dữ liệu cũ nếu có (optional - comment out nếu không muốn xóa)
-- DELETE FROM ke_toan_but_toan_chi_tiet WHERE but_toan_id IN (SELECT id FROM ke_toan_but_toan WHERE so_chung_tu LIKE 'BT%');
-- DELETE FROM ke_toan_but_toan WHERE so_chung_tu LIKE 'BT%';
-- DELETE FROM ke_toan_ky WHERE ten_ky LIKE '%2024%' OR ten_ky LIKE '%2025%';

-- =====================================================
-- 1. INSERT KỲ KẾ TOÁN (ke_toan_ky)
-- =====================================================

-- Năm 2024 (đã đóng)
INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Năm 2024', 'nam', '2024-01-01', '2024-12-31', 2024, 'dong', 2, 2, NOW(), NOW());

-- Năm 2025 (đang mở)
INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Năm 2025', 'nam', '2025-01-01', '2025-12-31', 2025, 'mo', 2, 2, NOW(), NOW());

-- Quý 1/2025
INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, quy, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Quý 1/2025', 'quy', '2025-01-01', '2025-03-31', 2025, 1, 'mo', 2, 2, NOW(), NOW());

-- Tháng 12/2024 (đã đóng)
INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, thang, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Tháng 12/2024', 'thang', '2024-12-01', '2024-12-31', 2024, 12, 'dong', 2, 2, NOW(), NOW());

-- Tháng 1/2025
INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, thang, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Tháng 1/2025', 'thang', '2025-01-01', '2025-01-31', 2025, 1, 'mo', 2, 2, NOW(), NOW());

-- Tháng 2/2025
INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, thang, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Tháng 2/2025', 'thang', '2025-02-01', '2025-02-28', 2025, 2, 'mo', 2, 2, NOW(), NOW());

-- Tháng 3/2025
INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, thang, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Tháng 3/2025', 'thang', '2025-03-01', '2025-03-31', 2025, 3, 'mo', 2, 2, NOW(), NOW());


-- =====================================================
-- 2. INSERT BÚT TOÁN (ke_toan_but_toan)
-- =====================================================

-- Lấy ID của kỳ kế toán tháng 1/2025
DO $$
DECLARE
    ky_thang_01 INTEGER;
    ky_thang_02 INTEGER;
    but_toan_01 INTEGER;
    but_toan_02 INTEGER;
    but_toan_03 INTEGER;
    but_toan_04 INTEGER;
    but_toan_05 INTEGER;
    but_toan_06 INTEGER;
    but_toan_07 INTEGER;
    but_toan_08 INTEGER;
    but_toan_09 INTEGER;
    but_toan_10 INTEGER;
    tk_1111 INTEGER;
    tk_1121 INTEGER;
    tk_131 INTEGER;
    tk_411 INTEGER;
    tk_152 INTEGER;
    tk_133 INTEGER;
    tk_622 INTEGER;
    tk_334 INTEGER;
    tk_338 INTEGER;
    tk_627 INTEGER;
    tk_214 INTEGER;
    tk_211 INTEGER;
    tk_511 INTEGER;
    tk_3331 INTEGER;
    tk_632 INTEGER;
BEGIN
    -- Lấy ID kỳ kế toán
    SELECT id INTO ky_thang_01 FROM ke_toan_ky WHERE ten_ky = 'Tháng 1/2025' LIMIT 1;
    SELECT id INTO ky_thang_02 FROM ke_toan_ky WHERE ten_ky = 'Tháng 2/2025' LIMIT 1;
    
    -- Lấy ID tài khoản
    SELECT id INTO tk_1111 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1111' LIMIT 1;
    SELECT id INTO tk_1121 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1121' LIMIT 1;
    SELECT id INTO tk_131 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '131' LIMIT 1;
    SELECT id INTO tk_411 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '411' LIMIT 1;
    SELECT id INTO tk_152 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '152' LIMIT 1;
    SELECT id INTO tk_133 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '133' LIMIT 1;
    SELECT id INTO tk_622 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '622' LIMIT 1;
    SELECT id INTO tk_334 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '334' LIMIT 1;
    SELECT id INTO tk_338 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '338' LIMIT 1;
    SELECT id INTO tk_627 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '627' LIMIT 1;
    SELECT id INTO tk_214 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '214' LIMIT 1;
    SELECT id INTO tk_211 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '211' LIMIT 1;
    SELECT id INTO tk_511 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '511' LIMIT 1;
    SELECT id INTO tk_3331 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '3331' LIMIT 1;
    SELECT id INTO tk_632 FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '632' LIMIT 1;
    
    -- BÚT TOÁN 1: Nhận vốn góp
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT001', '2025-01-02', 'thu', ky_thang_01, 'Nhận vốn góp từ chủ sở hữu', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_01;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_01, tk_1111, 500000000, 0, 'Tiền mặt tại quỹ', 10, 2, 2, NOW(), NOW()),
        (but_toan_01, tk_1121, 1000000000, 0, 'Tiền gửi ngân hàng', 20, 2, 2, NOW(), NOW()),
        (but_toan_01, tk_411, 0, 1500000000, 'Vốn đầu tư của chủ sở hữu', 30, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 2: Mua nguyên vật liệu
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT002', '2025-01-05', 'nhap', ky_thang_01, 'Mua nguyên vật liệu sản xuất', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_02;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_02, tk_152, 100000000, 0, 'Nguyên vật liệu nhập kho', 10, 2, 2, NOW(), NOW()),
        (but_toan_02, tk_133, 10000000, 0, 'Thuế GTGT được khấu trừ', 20, 2, 2, NOW(), NOW()),
        (but_toan_02, tk_1121, 0, 110000000, 'Thanh toán qua ngân hàng', 30, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 3: Chi phí lương tháng 1
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT003', '2025-01-10', 'luong', ky_thang_01, 'Trích lương và BHXH tháng 1/2025', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_03;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_03, tk_622, 80000000, 0, 'Chi phí nhân viên quản lý', 10, 2, 2, NOW(), NOW()),
        (but_toan_03, tk_334, 0, 72000000, 'Phải trả người lao động', 20, 2, 2, NOW(), NOW()),
        (but_toan_03, tk_338, 0, 8000000, 'Phải nộp BHXH, BHYT, BHTN', 30, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 4: Chi phí điện nước
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT004', '2025-01-15', 'chi', ky_thang_01, 'Chi phí điện nước tháng 1/2025', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_04;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_04, tk_627, 15000000, 0, 'Chi phí dịch vụ mua ngoài', 10, 2, 2, NOW(), NOW()),
        (but_toan_04, tk_1111, 0, 15000000, 'Thanh toán bằng tiền mặt', 20, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 5: Khấu hao TSCĐ
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT005', '2025-01-31', 'khau_hao', ky_thang_01, 'Khấu hao TSCĐ tháng 1/2025', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_05;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_05, tk_627, 5000000, 0, 'Chi phí khấu hao', 10, 2, 2, NOW(), NOW()),
        (but_toan_05, tk_214, 0, 5000000, 'Hao mòn TSCĐ', 20, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 6: Thu tiền từ khách hàng
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT006', '2025-01-20', 'thu', ky_thang_01, 'Thu tiền từ khách hàng ABC', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_06;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_06, tk_1121, 200000000, 0, 'Tiền gửi ngân hàng', 10, 2, 2, NOW(), NOW()),
        (but_toan_06, tk_131, 0, 200000000, 'Phải thu khách hàng', 20, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 7: Mua sắm TSCĐ
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT007', '2025-02-01', 'mua_sam', ky_thang_02, 'Mua máy tính văn phòng', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_07;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_07, tk_211, 30000000, 0, 'TSCĐ hữu hình', 10, 2, 2, NOW(), NOW()),
        (but_toan_07, tk_1121, 0, 30000000, 'Thanh toán qua ngân hàng', 20, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 8: Bán hàng và doanh thu
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT008', '2025-02-10', 'xuat', ky_thang_02, 'Doanh thu bán hàng tháng 2', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_08;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_08, tk_131, 220000000, 0, 'Phải thu khách hàng', 10, 2, 2, NOW(), NOW()),
        (but_toan_08, tk_511, 0, 200000000, 'Doanh thu bán hàng', 20, 2, 2, NOW(), NOW()),
        (but_toan_08, tk_3331, 0, 20000000, 'Thuế GTGT đầu ra', 30, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 9: Giá vốn hàng bán
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT009', '2025-02-10', 'xuat', ky_thang_02, 'Giá vốn hàng bán tháng 2', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_09;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_09, tk_632, 120000000, 0, 'Giá vốn hàng bán', 10, 2, 2, NOW(), NOW()),
        (but_toan_09, tk_152, 0, 120000000, 'Xuất kho nguyên vật liệu', 20, 2, 2, NOW(), NOW());
    
    -- BÚT TOÁN 10: Trả lương nhân viên
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT010', '2025-02-15', 'chi', ky_thang_02, 'Trả lương nhân viên tháng 1', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO but_toan_10;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    VALUES 
        (but_toan_10, tk_334, 72000000, 0, 'Phải trả người lao động', 10, 2, 2, NOW(), NOW()),
        (but_toan_10, tk_1121, 0, 72000000, 'Chuyển khoản lương', 20, 2, 2, NOW(), NOW());
    
    RAISE NOTICE 'Đã insert thành công % bút toán với tổng % dòng chi tiết', 10, 28;
    
END $$;

-- =====================================================
-- Cập nhật sequence cho số chứng từ
-- =====================================================
UPDATE ir_sequence 
SET number_next = 11 
WHERE code = 'ke_toan.but_toan';

-- =====================================================
-- Hoàn thành
-- =====================================================
