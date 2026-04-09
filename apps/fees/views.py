import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils import timezone
from .models import FeeStructure, Payment
from apps.rooms.models import Allocation


@login_required
def fee_dashboard(request):
    """Show fee info and payment history for a student."""
    # Get current allocation to determine fee
    allocation = Allocation.objects.filter(
        student=request.user, is_active=True
    ).select_related('bed', 'bed__room').first()

    fee_structure = None
    if allocation:
        room = allocation.bed.room
        fee_structure = FeeStructure.objects.filter(
            room_type=room.room_type,
            is_ac=room.is_ac
        ).first()

    payments = Payment.objects.filter(student=request.user)
    total_paid = sum(p.amount for p in payments if p.status == 'paid')

    context = {
        'allocation': allocation,
        'fee_structure': fee_structure,
        'payments': payments,
        'total_paid': total_paid,
    }
    return render(request, 'fees/fee_dashboard.html', context)


@login_required
def make_payment(request):
    """Mock payment flow."""
    allocation = Allocation.objects.filter(
        student=request.user, is_active=True
    ).select_related('bed', 'bed__room').first()

    if not allocation:
        messages.error(request, 'You do not have a room allocation. Cannot process payment.')
        return redirect('fees:fee_dashboard')

    room = allocation.bed.room
    fee_structure = FeeStructure.objects.filter(
        room_type=room.room_type, is_ac=room.is_ac
    ).first()

    amount = fee_structure.amount if fee_structure else room.monthly_rent

    if request.method == 'POST':
        fee_month = request.POST.get('fee_month', timezone.now().strftime('%B %Y'))

        # Simulate payment gateway (90% success rate)
        is_success = random.random() < 0.9

        payment = Payment.objects.create(
            student=request.user,
            amount=amount,
            fee_month=fee_month,
            status='paid' if is_success else 'failed',
        )

        if is_success:
            messages.success(request, f'Payment of ₹{amount} successful! Receipt: {payment.receipt_number}')
        else:
            messages.error(request, 'Payment failed! Please try again.')

        return redirect('fees:fee_dashboard')

    # Generate month options
    now = timezone.now()
    months = []
    for i in range(12):
        month = now.month + i
        year = now.year + (month - 1) // 12
        month = ((month - 1) % 12) + 1
        from datetime import date
        d = date(year, month, 1)
        months.append(d.strftime('%B %Y'))

    context = {
        'amount': amount,
        'room': room,
        'months': months,
    }
    return render(request, 'fees/make_payment.html', context)


@login_required
def payment_receipt(request, pk):
    """Download PDF receipt."""
    payment = get_object_or_404(Payment, pk=pk, student=request.user)

    if payment.status != 'paid':
        messages.error(request, 'Receipt not available for failed/pending payments.')
        return redirect('fees:fee_dashboard')

    allocation = Allocation.objects.filter(
        student=request.user, is_active=True
    ).select_related('bed', 'bed__room').first()

    context = {
        'payment': payment,
        'student': request.user,
        'allocation': allocation,
    }

    # Try PDF generation, fall back to HTML
    try:
        from xhtml2pdf import pisa
        from io import BytesIO

        template = get_template('fees/receipt_pdf.html')
        html = template.render(context)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)

        if not pdf.err:
            response = HttpResponse(result.getvalue(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="Receipt_{payment.receipt_number}.pdf"'
            return response
    except Exception:
        pass

    # Fallback: render HTML receipt
    return render(request, 'fees/receipt_pdf.html', context)


def admin_required(view_func):
    """Decorator to restrict access to admin/warden only."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_hostel_admin or request.user.is_warden):
            messages.error(request, 'Access denied.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@admin_required
def all_payments(request):
    """Admin view: all payments with filters."""
    payments = Payment.objects.all().select_related('student')

    status_filter = request.GET.get('status')
    if status_filter:
        payments = payments.filter(status=status_filter)

    search = request.GET.get('search')
    if search:
        payments = payments.filter(
            student__first_name__icontains=search
        ) | payments.filter(
            student__last_name__icontains=search
        ) | payments.filter(
            student__username__icontains=search
        ) | payments.filter(
            receipt_number__icontains=search
        )

    total_collected = sum(p.amount for p in payments if p.status == 'paid')

    context = {
        'payments': payments,
        'total_collected': total_collected,
        'selected_status': status_filter,
        'search_query': search or '',
    }
    return render(request, 'fees/all_payments.html', context)
