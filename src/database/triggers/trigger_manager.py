from src.database.triggers.trg_UpdateBillTotal import create_trigger_update_bill_total
from src.database.triggers.trg_UpdateCustomerRank import create_trigger_update_customer_rank
from src.database.triggers.trg_DefaultCustomerRank import create_trigger_default_customer_rank
from src.database.triggers.trg_UpdateProductImportPrice import create_trigger_update_product_import_price
from src.database.triggers.trg_UpdateInventoryAfterImport import create_trigger_update_inventory_after_import
from src.database.triggers.trg_UpdateInventoryAfterSale import create_trigger_update_inventory_after_sale
from src.database.triggers.trg_CheckInventoryBeforeSale import create_trigger_check_inventory_before_sale
from src.database.triggers.trg_DefaultProductValues import create_trigger_default_product_values
from src.database.triggers.trg_ApplyDiscountOnPromotion import create_trigger_apply_discount_on_promotion
from src.database.triggers.trg_RestorePriceOnPromotionDelete import create_trigger_restore_price_on_promotion_delete
from src.database.triggers.sp_RestorePriceAfterPromotionEnds import create_sp_restore_price_after_promotion_ends


def setup_all_triggers(cursor):
    """Thiết lập tất cả các trigger trong cơ sở dữ liệu"""

    # Danh sách kết quả tạo trigger
    results = []

    # Kiểm tra các bảng tồn tại trước khi tạo trigger
    tables_exist = check_tables_exist(cursor)

    if not tables_exist:
        print("Một số bảng cần thiết không tồn tại. Không thể tạo trigger.")
        return False

    # Tạo từng trigger và stored procedure
    results.append(create_trigger_update_bill_total(cursor))
    results.append(create_trigger_update_customer_rank(cursor))
    results.append(create_trigger_default_customer_rank(cursor))
    results.append(create_trigger_update_product_import_price(cursor))
    results.append(create_trigger_update_inventory_after_import(cursor))
    results.append(create_trigger_update_inventory_after_sale(cursor))
    results.append(create_trigger_check_inventory_before_sale(cursor))
    results.append(create_trigger_default_product_values(cursor))
    results.append(create_trigger_apply_discount_on_promotion(cursor))
    results.append(create_trigger_restore_price_on_promotion_delete(cursor))
    results.append(create_sp_restore_price_after_promotion_ends(cursor))

    # Kiểm tra kết quả
    if all(results):
        print("Đã thiết lập tất cả trigger và stored procedure thành công")
        return True
    else:
        print("Có lỗi xảy ra khi thiết lập một số trigger hoặc stored procedure")
        return False


def check_tables_exist(cursor):
    """Kiểm tra các bảng cần thiết có tồn tại không"""
    required_tables = [
        'Bill_detail', 'Bill', 'Customers', 'Import_detail',
        'Import', 'Products', 'Warehouse_Product', 'Promotion', 'Promotion_detail'
    ]

    all_exist = True

    for table in required_tables:
        try:
            cursor.execute(f"SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{table}'")
            if not cursor.fetchone():
                print(f"Bảng '{table}' không tồn tại trong cơ sở dữ liệu")
                all_exist = False
        except Exception as e:
            print(f"Lỗi khi kiểm tra bảng '{table}': {str(e)}")
            all_exist = False

    return all_exist