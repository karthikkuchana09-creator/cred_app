from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, UserProfileView, CardListCreateView, CardDeleteView, TransactionListView, ExportTransactionsAdminView, DailyPaymentSummaryAdminView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', UserProfileView.as_view(), name='profile'),
    path('cards/', CardListCreateView.as_view(), name='cards'),
    path('cards/<int:pk>/', CardDeleteView.as_view(), name='delete_card'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('admin/export-transactions/', ExportTransactionsAdminView.as_view(), name='export_transactions'),
    path('admin/daily-summary/', DailyPaymentSummaryAdminView.as_view(), name='daily_summary'),
]
