-- =====================================================
-- File SQL đơn giản: Insert dữ liệu demo vào database
-- =====================================================

-- Xóa dữ liệu cũ nếu có
DELETE FROM ke_toan_but_toan_chi_tiet WHERE but_toan_id IN (SELECT id FROM ke_toan_but_toan WHERE so_chung_tu LIKE 'BT0%');
DELETE FROM ke_toan_but_toan WHERE so_chung_tu LIKE 'BT0%';
DELETE FROM ke_toan_ky WHERE ten_ky IN ('Năm 2024', 'Năm 2025', 'Quý 1/2025', 'Tháng 12/2024', 'Tháng 1/2025', 'Tháng 2/2025', 'Tháng 3/2025');

-- =====================================================
-- 1. INSERT KỲ KẾ TOÁN
-- =====================================================

INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES 
('Năm 2024', 'nam', '2024-01-01', '2024-12-31', 2024, 'dong', 2, 2, NOW(), NOW()),
('Năm 2025', 'nam', '2025-01-01', '2025-12-31', 2025, 'mo', 2, 2, NOW(), NOW()),
('Tháng 12/2024', 'thang', '2024-12-01', '2024-12-31', 2024, 'dong', 2, 2, NOW(), NOW()),
('Tháng 1/2025', 'thang', '2025-01-01', '2025-01-31', 2025, 'mo', 2, 2, NOW(), NOW()),
('Tháng 2/2025', 'thang', '2025-02-01', '2025-02-28', 2025, 'mo', 2, 2, NOW(), NOW()),
('Tháng 3/2025', 'thang', '2025-03-01', '2025-03-31', 2025, 'mo', 2, 2, NOW(), NOW());

UPDATE ke_toan_ky SET thang = 12 WHERE ten_ky = 'Tháng 12/2024';
UPDATE ke_toan_ky SET thang = 1 WHERE ten_ky = 'Tháng 1/2025';
UPDATE ke_toan_ky SET thang = 2 WHERE ten_ky = 'Tháng 2/2025';
UPDATE ke_toan_ky SET thang = 3 WHERE ten_ky = 'Tháng 3/2025';

INSERT INTO ke_toan_ky (ten_ky, loai_ky, ngay_bat_dau, ngay_ket_thuc, nam_tai_chinh, quy, trang_thai, create_uid, write_uid, create_date, write_date)
VALUES ('Quý 1/2025', 'quy', '2025-01-01', '2025-03-31', 2025, 1, 'mo', 2, 2, NOW(), NOW());

-- =====================================================
-- 2. INSERT BÚT TOÁN VÀ CHI TIẾT
-- =====================================================

DO $$
DECLARE
    ky_thang_01 INTEGER;
    ky_thang_02 INTEGER;
    bt_id INTEGER;
BEGIN
    -- Lấy ID kỳ kế toán
    SELECT id INTO ky_thang_01 FROM ke_toan_ky WHERE ten_ky = 'Tháng 1/2025' LIMIT 1;
    SELECT id INTO ky_thang_02 FROM ke_toan_ky WHERE ten_ky = 'Tháng 2/2025' LIMIT 1;
    
    -- BÚT TOÁN 1: Nhận vốn góp (Nợ 1111, 1121 / Có 411)
    -- Chú ý: Cần tạo TK 411 trong tai_khoan_data.xml trước
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT001', '2025-01-02', 'thu', ky_thang_01, 'Nhận vốn góp từ chủ sở hữu', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 500000000, 0, 'Tiền mặt tại quỹ', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1111' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 1000000000, 0, 'Tiền gửi ngân hàng', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1121' LIMIT 1;
    
    -- Tạm thời sử dụng TK 331 thay vì 411 (vì chưa có TK 411)
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 1500000000, 'Vốn chủ sở hữu', 30, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '331' LIMIT 1;
    
    
    -- BÚT TOÁN 2: Chi phí lương (Nợ 6421 / Có 334, 338)
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT002', '2025-01-10', 'luong', ky_thang_01, 'Trích lương và BHXH tháng 1/2025', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 80000000, 0, 'Chi phí nhân viên quản lý', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '6421' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 72000000, 'Phải trả người lao động', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '334' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 8000000, 'Phải nộp BHXH', 30, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '3383' LIMIT 1;
    
    
    -- BÚT TOÁN 3: Chi phí điện nước (Nợ 6424 / Có 1111)
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT003', '2025-01-15', 'chi', ky_thang_01, 'Chi phí điện nước tháng 1/2025', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 15000000, 0, 'Chi phí quản lý khác', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '6424' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 15000000, 'Thanh toán bằng tiền mặt', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1111' LIMIT 1;
    
    
    -- BÚT TOÁN 4: Khấu hao TSCĐ (Nợ 6424 / Có 2141)
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT004', '2025-01-31', 'khau_hao', ky_thang_01, 'Khấu hao TSCĐ tháng 1/2025', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 5000000, 0, 'Chi phí khấu hao TSCĐ', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '6424' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 5000000, 'Hao mòn TSCĐ hữu hình', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '2141' LIMIT 1;
    
    
    -- BÚT TOÁN 5: Thu tiền từ khách hàng (Nợ 1121 / Có 131)
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT005', '2025-01-20', 'thu', ky_thang_01, 'Thu tiền từ khách hàng ABC', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 200000000, 0, 'Tiền gửi ngân hàng', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1121' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 200000000, 'Phải thu khách hàng', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '131' LIMIT 1;
    
    
    -- BÚT TOÁN 6: Mua sắm TSCĐ (Nợ 2112 / Có 1121)
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT006', '2025-02-01', 'mua_sam', ky_thang_02, 'Mua máy tính văn phòng', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 30000000, 0, 'Máy móc, thiết bị', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '2112' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 30000000, 'Thanh toán qua ngân hàng', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1121' LIMIT 1;
    
    
    -- BÚT TOÁN 7: Bán hàng và doanh thu (Nợ 131 / Có 511)
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT007', '2025-02-10', 'xuat', ky_thang_02, 'Doanh thu bán hàng tháng 2', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 200000000, 0, 'Phải thu khách hàng', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '131' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 200000000, 'Doanh thu bán hàng', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '511' LIMIT 1;
    
    
    -- BÚT TOÁN 8: Trả lương nhân viên (Nợ 334 / Có 1121)
    INSERT INTO ke_toan_but_toan (so_chung_tu, ngay_chung_tu, loai_chung_tu, ky_ke_toan_id, dien_giai, trang_thai, nguoi_lap_id, create_uid, write_uid, create_date, write_date)
    VALUES ('BT008', '2025-02-15', 'chi', ky_thang_02, 'Trả lương nhân viên tháng 1', 'da_ghi_so', 2, 2, 2, NOW(), NOW())
    RETURNING id INTO bt_id;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 72000000, 0, 'Phải trả người lao động', 10, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '334' LIMIT 1;
    
    INSERT INTO ke_toan_but_toan_chi_tiet (but_toan_id, tai_khoan_id, so_tien_no, so_tien_co, dien_giai, sequence, create_uid, write_uid, create_date, write_date)
    SELECT bt_id, id, 0, 72000000, 'Chuyển khoản lương', 20, 2, 2, NOW(), NOW() FROM ke_toan_tai_khoan WHERE ma_tai_khoan = '1121' LIMIT 1;
    
    RAISE NOTICE 'Đã insert thành công 8 bút toán!';
    
END $$;

-- Cập nhật sequence
UPDATE ir_sequence SET number_next = 9 WHERE code = 'ke_toan.but_toan';

-- Kiểm tra kết quả
SELECT COUNT(*) as "Số kỳ kế toán" FROM ke_toan_ky WHERE ten_ky LIKE '%2024%' OR ten_ky LIKE '%2025%';
SELECT COUNT(*) as "Số bút toán" FROM ke_toan_but_toan WHERE so_chung_tu LIKE 'BT0%';
SELECT COUNT(*) as "Số dòng chi tiết" FROM ke_toan_but_toan_chi_tiet WHERE but_toan_id IN (SELECT id FROM ke_toan_but_toan WHERE so_chung_tu LIKE 'BT0%');
