from .auth import register, activate_account
from .home import home
from .field import (detail, admin_all_fields, admin_field_detail,
                    admin_add_field, admin_edit_field)
from .order import (order_field, order_detail, my_orders, 
                    order_edit, order_cancel, all_orders, 
                    admin_cancel_order, admin_accept_order, 
                    admin_order_detail, review_field, edit_review)
from .voucher import (voucher_list_user, voucher_list_admin, 
                      voucher_create, voucher_edit, voucher_delete)
from .field_request import (my_field_requests, create_field_request,
                           edit_field_request, field_request_detail,
                           admin_field_requests, admin_field_request_detail,
                           cancel_field_request, admin_update_field_request_status,
                           admin_field_request_detail)
