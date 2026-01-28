# -*- coding: utf-8 -*-
"""
Migration script: Di chuyển dữ liệu từ model cũ sang model mới
- Xóa model tai_khoan_ke_toan và so_cai từ module quan_ly_tai_san
- Di chuyển liên kết sang ke_toan.tai_khoan và ke_toan.but_toan
"""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """
    Post-migration script
    """
    _logger.info("====== BẮT ĐẦU MIGRATION 15.0.1.0.1 ======")
    
    # 1. Kiểm tra và xóa bảng so_cai nếu tồn tại
    _drop_so_cai_table(cr)
    
    # 2. Kiểm tra và xóa bảng tai_khoan_ke_toan nếu tồn tại
    _drop_tai_khoan_ke_toan_table(cr)
    
    # 3. Xóa các field cũ trong danh_muc_tai_san
    _cleanup_danh_muc_tai_san_fields(cr)
    
    # 4. Xóa field so_cai_id trong khau_hao
    _cleanup_khau_hao_fields(cr)
    
    _logger.info("====== HOÀN THÀNH MIGRATION 15.0.1.0.1 ======")


def _drop_so_cai_table(cr):
    """Xóa bảng so_cai và các ràng buộc liên quan"""
    try:
        # Kiểm tra bảng có tồn tại không
        cr.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = 'so_cai'
            )
        """)
        
        if cr.fetchone()[0]:
            _logger.info("Tìm thấy bảng so_cai, tiến hành xóa...")
            
            # Xóa các foreign key constraints
            cr.execute("""
                SELECT constraint_name 
                FROM information_schema.table_constraints 
                WHERE table_name = 'so_cai' 
                AND constraint_type = 'FOREIGN KEY'
            """)
            for row in cr.fetchall():
                constraint_name = row[0]
                cr.execute(f"ALTER TABLE so_cai DROP CONSTRAINT IF EXISTS {constraint_name} CASCADE")
                _logger.info(f"Đã xóa constraint: {constraint_name}")
            
            # Xóa bảng
            cr.execute("DROP TABLE IF EXISTS so_cai CASCADE")
            _logger.info("✅ Đã xóa bảng so_cai")
            
            # Xóa ir.model.data
            cr.execute("""
                DELETE FROM ir_model_data 
                WHERE model = 'ir.model' 
                AND name = 'model_so_cai'
            """)
            
            # Xóa ir.model
            cr.execute("""
                DELETE FROM ir_model 
                WHERE model = 'so_cai'
            """)
            _logger.info("✅ Đã xóa metadata cho model so_cai")
        else:
            _logger.info("Bảng so_cai không tồn tại, bỏ qua")
            
    except Exception as e:
        _logger.error(f"Lỗi khi xóa bảng so_cai: {str(e)}")


def _drop_tai_khoan_ke_toan_table(cr):
    """Xóa bảng tai_khoan_ke_toan và các ràng buộc liên quan"""
    try:
        # Kiểm tra bảng có tồn tại không
        cr.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public'
                AND table_name = 'tai_khoan_ke_toan'
            )
        """)
        
        if cr.fetchone()[0]:
            _logger.info("Tìm thấy bảng tai_khoan_ke_toan, tiến hành xóa...")
            
            # Xóa các foreign key từ bảng khác trỏ đến
            cr.execute("""
                SELECT 
                    tc.table_name, 
                    tc.constraint_name 
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.referential_constraints rc 
                    ON tc.constraint_name = rc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                AND kcu.referenced_table_name = 'tai_khoan_ke_toan'
            """)
            
            for row in cr.fetchall():
                table_name, constraint_name = row
                cr.execute(f"ALTER TABLE {table_name} DROP CONSTRAINT IF EXISTS {constraint_name} CASCADE")
                _logger.info(f"Đã xóa FK từ {table_name}: {constraint_name}")
            
            # Xóa bảng
            cr.execute("DROP TABLE IF EXISTS tai_khoan_ke_toan CASCADE")
            _logger.info("✅ Đã xóa bảng tai_khoan_ke_toan")
            
            # Xóa metadata
            cr.execute("""
                DELETE FROM ir_model_data 
                WHERE model = 'ir.model' 
                AND name = 'model_tai_khoan_ke_toan'
            """)
            
            cr.execute("""
                DELETE FROM ir_model 
                WHERE model = 'tai_khoan_ke_toan'
            """)
            _logger.info("✅ Đã xóa metadata cho model tai_khoan_ke_toan")
        else:
            _logger.info("Bảng tai_khoan_ke_toan không tồn tại, bỏ qua")
            
    except Exception as e:
        _logger.error(f"Lỗi khi xóa bảng tai_khoan_ke_toan: {str(e)}")


def _cleanup_danh_muc_tai_san_fields(cr):
    """Xóa các field cũ trong bảng danh_muc_tai_san"""
    try:
        _logger.info("Xóa các field cũ trong danh_muc_tai_san...")
        
        # Danh sách các column cần xóa
        columns_to_drop = [
            'tai_khoan_nguyen_gia_id',
            'tai_khoan_khau_hao_id',
            'tai_khoan_chi_phi_id',
        ]
        
        # Kiểm tra và xóa từng column
        for column in columns_to_drop:
            cr.execute(f"""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'danh_muc_tai_san'
                    AND column_name = '{column}'
                )
            """)
            
            if cr.fetchone()[0]:
                cr.execute(f"ALTER TABLE danh_muc_tai_san DROP COLUMN IF EXISTS {column} CASCADE")
                _logger.info(f"✅ Đã xóa column {column} từ danh_muc_tai_san")
                
                # Xóa ir.model.fields
                cr.execute(f"""
                    DELETE FROM ir_model_fields 
                    WHERE model = 'danh_muc_tai_san'
                    AND name = '{column}'
                """)
        
    except Exception as e:
        _logger.error(f"Lỗi khi xóa fields từ danh_muc_tai_san: {str(e)}")


def _cleanup_khau_hao_fields(cr):
    """Xóa field so_cai_id trong bảng khau_hao"""
    try:
        _logger.info("Xóa field so_cai_id từ khau_hao...")
        
        cr.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'khau_hao'
                AND column_name = 'so_cai_id'
            )
        """)
        
        if cr.fetchone()[0]:
            cr.execute("ALTER TABLE khau_hao DROP COLUMN IF EXISTS so_cai_id CASCADE")
            _logger.info("✅ Đã xóa column so_cai_id từ khau_hao")
            
            # Xóa ir.model.fields
            cr.execute("""
                DELETE FROM ir_model_fields 
                WHERE model = 'khau_hao'
                AND name = 'so_cai_id'
            """)
            
    except Exception as e:
        _logger.error(f"Lỗi khi xóa field so_cai_id: {str(e)}")
