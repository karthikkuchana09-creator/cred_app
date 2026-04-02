from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .models import Card, Transaction, AdminLog
from .serializers import RegisterSerializer, CardSerializer, TransactionSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer


class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({'id': request.user.id, 'username': request.user.username, 'email': request.user.email})


class CardListCreateView(generics.ListCreateAPIView):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Card.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()


class CardDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Card.objects.all()

    def get_object(self):
        card = super().get_object()
        if card.user != self.request.user:
            raise permissions.PermissionDenied('Not your card')
        return card

    def delete(self, request, *args, **kwargs):
        self.perform_destroy(self.get_object())
        return Response({"detail": "Card deleted"}, status=status.HTTP_200_OK)


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Transaction.objects.filter(user=self.request.user)
        status_q = self.request.query_params.get('status')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        amount_min = self.request.query_params.get('amount_min')
        amount_max = self.request.query_params.get('amount_max')

        if status_q:
            qs = qs.filter(status=status_q.upper())
        if date_from:
            qs = qs.filter(created_at__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__lte=date_to)
        if amount_min:
            qs = qs.filter(amount__gte=amount_min)
        if amount_max:
            qs = qs.filter(amount__lte=amount_max)
        return qs


class ExportTransactionsAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        import csv
        from django.http import HttpResponse

        transactions = Transaction.objects.all().order_by('-created_at')
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
        writer = csv.writer(response)
        writer.writerow(['id', 'user', 'card', 'amount', 'status', 'created_at'])
        for t in transactions:
            writer.writerow([t.id, t.user.email, t.card.masked_number if t.card else '', t.amount, t.status, t.created_at])
        return response


class DailyPaymentSummaryAdminView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        from django.db.models import Sum
        from django.utils import timezone
        today = timezone.now().date()
        summary = Transaction.objects.filter(created_at__date=today).values('status').annotate(total=Sum('amount'))
        return Response({'date': str(today), 'summary': list(summary)})
