from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework import status
from warrior_app.models import *
from warrior_app.serializers import *
from rest_framework.viewsets import ModelViewSet
from .permissions import *
from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_date
# views.py
import openpyxl
from django.http import HttpResponse

# Create your views here.: 

class OrdersView(APIView):
    permission_classes = [IsSuperuserOrStaff]
    def get(self, request):
        if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
            return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        orders = BuyNow.objects.all()
        date_filter = request.query_params.get("date")

        if date_filter == "today":
            orders = orders.filter(created_at__date=datetime.today().date())
        elif date_filter == "month":
            now = datetime.now()
            orders = orders.filter(created_at__year=now.year, created_at__month=now.month)
        elif date_filter == "year":
            now = datetime.now()
            orders = orders.filter(created_at__year=now.year)
        elif date_filter and len(date_filter) == 4 and date_filter.isdigit():
            orders = orders.filter(created_at__year=int(date_filter))
        elif date_filter and "-" in date_filter and len(date_filter) == 7:
            try:
                year, month = map(int, date_filter.split("-"))
                orders = orders.filter(created_at__year=year, created_at__month=month)
            except ValueError:
                pass
        else:
            try:
                parsed_date = parse_date(date_filter)
                if parsed_date:
                    orders = orders.filter(created_at__date=parsed_date)
            except Exception:
                pass

        orders = orders.order_by('-id')
        serializer = BuyNowSerializer(orders, many=True, context={'request': request})
        return Response(serializer.data)
    

    def patch(self, request):
        if not request.user.is_authenticated or not (request.user.is_superuser or request.user.is_staff):
            return Response({'message': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)

        order_id = request.data.get('id')
        if not order_id:
            return Response({'message': 'Order ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        order = get_object_or_404(BuyNow, id=order_id)

        serializer = BuyNowSerializer(order, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Order updated successfully', 'order': serializer.data}, status=200)
        return Response(serializer.errors, status=400)

class ContactViewSet(ModelViewSet):
    queryset = ContactSupport.objects.all()
    serializer_class = ContactSupportSerializer
    permission_classes = [IsSuperuserOrStaff]
    
    

def export_dashboard_data(request):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Dashboard Data"

    ws.append(["Order ID", "User", "Email", "Phone", "Amount", "Products", "Status","Address", "Date"])

    orders = BuyNow.objects.select_related("user").prefetch_related("items__product")

    for order in orders:
        items = order.items.all() 

        if items:
            products_summary = ", ".join([
                f"{item.product.title} - {item.product.variant} (Qty: {item.quantity})"
                for item in items
            ])
        else:
            products_summary = "N/A"

        ws.append([
            order.id,
            order.customer_name,
            order.customer_email,
            order.customer_phone,
            order.total_amount,
            products_summary,
            order.status,
            order.shipping_address,
            order.created_at.strftime('%Y-%m-%d'),
        ])

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename=dashboard_data.xlsx'
    wb.save(response)
    return response


class Warranty(viewsets.ModelViewSet):
    queryset = WarrentyRegistration.objects.all()
    serializer_class = WarrentyRegistrationSerializer