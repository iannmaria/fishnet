from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("fishermen/", views.view_fishermen, name="view_fishermen"),
    path("fishermen/detail/<int:fisherman_id>/", views.view_fisherman_detail, name="view_fisherman_detail"),
    path("fishermen/approve/<int:fisherman_id>/", views.approve_fisherman, name="approve_fisherman"),
    path("fishermen/remove/<int:fisherman_id>/", views.remove_fisherman, name="remove_fisherman"),
    path("users/", views.view_users, name="view_users"),
    path("users/remove/<int:user_id>/", views.remove_user, name="remove_user"),
    path("staff/", views.view_staff, name="view_staff"),
    path("staff/assign-region/<int:staff_id>/", views.assign_region_to_staff, name="assign_region_to_staff"),
    path("fish/", views.manage_fish, name="manage_fish"),
    path("fish/add/", views.add_fish, name="add_fish"),
    path("fish/edit/<int:fish_id>/", views.edit_fish, name="edit_fish"),
    path("fish/remove/<int:fish_id>/", views.remove_fish, name="remove_fish"),
    path("categories/", views.manage_categories, name="manage_categories"),
    path("categories/add/", views.add_category, name="add_category"),
    path("categories/remove/<int:category_id>/", views.remove_category, name="remove_category"),
    path("shipping/", views.shipping_handling, name="shipping_handling"),
    path("shipping/update-status/<int:order_id>/", views.update_order_status, name="update_order_status"),
    path("complaints/", views.view_complaints, name="view_complaints"),
    path("complaints/reply/<int:complaint_id>/", views.reply_to_complaint, name="reply_to_complaint"),
    path("reports/", views.reports, name="reports"),
]
