import csv
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.db.models import Count, Sum, Q
from apps.accounts.models import CustomUser
from apps.rooms.models import Room, Bed, Allocation
from apps.fees.models import Payment
from apps.complaints.models import Complaint
from apps.visitors.models import VisitorEntry


@login_required
def home(request):
    """Main dashboard - different views for students and admin."""
    if request.user.is_hostel_admin or request.user.is_warden:
        return admin_dashboard(request)
    return student_dashboard(request)


def student_dashboard(request):
    """Dashboard for students."""
    allocation = Allocation.objects.filter(
        student=request.user, is_active=True
    ).select_related('bed', 'bed__room').first()

    recent_payments = Payment.objects.filter(student=request.user)[:5]
    open_complaints = Complaint.objects.filter(student=request.user, status__in=['open', 'in_progress']).count()
    total_complaints = Complaint.objects.filter(student=request.user).count()

    context = {
        'allocation': allocation,
        'recent_payments': recent_payments,
        'open_complaints': open_complaints,
        'total_complaints': total_complaints,
    }
    return render(request, 'dashboard/student_dashboard.html', context)


def admin_dashboard(request):
    """Dashboard for admin/warden with analytics."""
    total_students = CustomUser.objects.filter(role='student').count()
    total_rooms = Room.objects.count()
    total_beds = Bed.objects.count()
    occupied_beds = Bed.objects.filter(status='occupied').count()
    available_beds = Bed.objects.filter(status='available').count()

    occupancy_pct = round((occupied_beds / total_beds * 100)) if total_beds > 0 else 0

    # Fee stats
    total_collected = Payment.objects.filter(status='paid').aggregate(
        total=Sum('amount'))['total'] or 0
    pending_payments = Payment.objects.filter(status='pending').count()

    # Complaint stats
    open_complaints = Complaint.objects.filter(status='open').count()
    in_progress_complaints = Complaint.objects.filter(status='in_progress').count()
    resolved_complaints = Complaint.objects.filter(status='resolved').count()
    total_complaints = Complaint.objects.count()

    # Complaint by category for chart
    complaint_categories = Complaint.objects.values('category').annotate(
        count=Count('id')).order_by('-count')

    # Recent activity
    recent_allocations = Allocation.objects.filter(is_active=True).select_related(
        'student', 'bed', 'bed__room')[:5]
    recent_complaints = Complaint.objects.all()[:5]
    recent_visitors = VisitorEntry.objects.all()[:5]

    context = {
        'total_students': total_students,
        'total_rooms': total_rooms,
        'total_beds': total_beds,
        'occupied_beds': occupied_beds,
        'available_beds': available_beds,
        'occupancy_pct': occupancy_pct,
        'total_collected': total_collected,
        'pending_payments': pending_payments,
        'open_complaints': open_complaints,
        'in_progress_complaints': in_progress_complaints,
        'resolved_complaints': resolved_complaints,
        'total_complaints': total_complaints,
        'complaint_categories': list(complaint_categories),
        'recent_allocations': recent_allocations,
        'recent_complaints': recent_complaints,
        'recent_visitors': recent_visitors,
    }
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
def chart_data(request):
    """Return chart data as JSON for AJAX."""
    if not (request.user.is_hostel_admin or request.user.is_warden):
        return JsonResponse({'error': 'Access denied'}, status=403)

    # Complaint by category
    complaint_cats = list(Complaint.objects.values('category').annotate(count=Count('id')))

    # Room occupancy by floor
    floors = Room.objects.values_list('floor', flat=True).distinct().order_by('floor')
    occupancy_by_floor = []
    for floor in floors:
        total = Bed.objects.filter(room__floor=floor).count()
        occupied = Bed.objects.filter(room__floor=floor, status='occupied').count()
        occupancy_by_floor.append({
            'floor': floor,
            'total': total,
            'occupied': occupied,
        })

    # Payment status breakdown
    payment_stats = list(Payment.objects.values('status').annotate(
        count=Count('id'), total=Sum('amount')))

    return JsonResponse({
        'complaint_categories': complaint_cats,
        'occupancy_by_floor': occupancy_by_floor,
        'payment_stats': payment_stats,
    })


@login_required
def export_csv(request, report_type):
    """Export data as CSV."""
    if not (request.user.is_hostel_admin or request.user.is_warden):
        return redirect('dashboard:home')

    response = HttpResponse(content_type='text/csv')

    if report_type == 'students':
        response['Content-Disposition'] = 'attachment; filename="students_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Username', 'Name', 'Email', 'Phone', 'Institution', 'Room', 'Bed'])
        for student in CustomUser.objects.filter(role='student'):
            allocation = Allocation.objects.filter(student=student, is_active=True).first()
            room = allocation.bed.room.room_number if allocation else 'Not Allocated'
            bed = allocation.bed.bed_label if allocation else '-'
            writer.writerow([student.username, student.get_full_name(), student.email,
                           student.phone, student.institution, room, bed])

    elif report_type == 'payments':
        response['Content-Disposition'] = 'attachment; filename="payments_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['Receipt #', 'Student', 'Amount', 'Month', 'Status', 'Date', 'Transaction ID'])
        for p in Payment.objects.all().select_related('student'):
            writer.writerow([p.receipt_number, p.student.get_full_name(), p.amount,
                           p.fee_month, p.status, p.payment_date.strftime('%Y-%m-%d'), p.transaction_id])

    elif report_type == 'complaints':
        response['Content-Disposition'] = 'attachment; filename="complaints_report.csv"'
        writer = csv.writer(response)
        writer.writerow(['ID', 'Student', 'Category', 'Priority', 'Subject', 'Status', 'Created', 'Resolved'])
        for c in Complaint.objects.all().select_related('student'):
            writer.writerow([c.id, c.student.get_full_name(), c.category, c.priority,
                           c.subject, c.status, c.created_at.strftime('%Y-%m-%d'),
                           c.resolved_at.strftime('%Y-%m-%d') if c.resolved_at else '-'])

    return response
