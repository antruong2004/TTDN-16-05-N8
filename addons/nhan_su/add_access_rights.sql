-- Script SQL để thêm access rights cho các models mới
-- Chạy script này sau khi module đã upgrade thành công

INSERT INTO ir_model_access (name, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink)
SELECT 
    'access_cham_cong_user',
    id,
    (SELECT id FROM res_groups WHERE name = 'User types / Internal User' LIMIT 1),
    true, true, true, true
FROM ir_model 
WHERE model = 'cham_cong'
AND NOT EXISTS (SELECT 1 FROM ir_model_access WHERE name = 'access_cham_cong_user');

INSERT INTO ir_model_access (name, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink)
SELECT 
    'access_bao_cao_cham_cong_user',
    id,
    (SELECT id FROM res_groups WHERE name = 'User types / Internal User' LIMIT 1),
    true, true, true, true
FROM ir_model 
WHERE model = 'bao_cao_cham_cong'
AND NOT EXISTS (SELECT 1 FROM ir_model_access WHERE name = 'access_bao_cao_cham_cong_user');

INSERT INTO ir_model_access (name, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink)
SELECT 
    'access_bang_luong_user',
    id,
    (SELECT id FROM res_groups WHERE name = 'User types / Internal User' LIMIT 1),
    true, true, true, true
FROM ir_model 
WHERE model = 'bang_luong'
AND NOT EXISTS (SELECT 1 FROM ir_model_access WHERE name = 'access_bang_luong_user');

INSERT INTO ir_model_access (name, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink)
SELECT 
    'access_chi_tiet_phu_cap_user',
    id,
    (SELECT id FROM res_groups WHERE name = 'User types / Internal User' LIMIT 1),
    true, true, true, true
FROM ir_model 
WHERE model = 'chi_tiet_phu_cap'
AND NOT EXISTS (SELECT 1 FROM ir_model_access WHERE name = 'access_chi_tiet_phu_cap_user');

INSERT INTO ir_model_access (name, model_id, group_id, perm_read, perm_write, perm_create, perm_unlink)
SELECT 
    'access_chi_tiet_khau_tru_user',
    id,
    (SELECT id FROM res_groups WHERE name = 'User types / Internal User' LIMIT 1),
    true, true, true, true
FROM ir_model 
WHERE model = 'chi_tiet_khau_tru'
AND NOT EXISTS (SELECT 1 FROM ir_model_access WHERE name = 'access_chi_tiet_khau_tru_user');
