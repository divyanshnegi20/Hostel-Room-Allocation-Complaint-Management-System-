from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Complaint
from .forms import ComplaintForm, ComplaintUpdateForm


@login_required
def complaint_list(request):
    """List complaints - students see their own, admin sees all."""
    if request.user.is_hostel_admin or request.user.is_warden:
        complaints = Complaint.objects.all().select_related('student')
    else:
        complaints = Complaint.objects.filter(student=request.user)

    # Filters
    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')

    if status_filter:
        complaints = complaints.filter(status=status_filter)
    if category_filter:
        complaints = complaints.filter(category=category_filter)

    context = {
        'complaints': complaints,
        'selected_status': status_filter,
        'selected_category': category_filter,
    }
    return render(request, 'complaints/complaint_list.html', context)


@login_required
def complaint_create(request):
    """Submit a new complaint."""
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.student = request.user
            complaint.save()
            messages.success(request, f'Complaint #{complaint.pk} submitted successfully.')
            return redirect('complaints:complaint_list')
    else:
        form = ComplaintForm()

    return render(request, 'complaints/complaint_form.html', {'form': form})


@login_required
def complaint_detail(request, pk):
    """View complaint details."""
    if request.user.is_hostel_admin or request.user.is_warden:
        complaint = get_object_or_404(Complaint, pk=pk)
    else:
        complaint = get_object_or_404(Complaint, pk=pk, student=request.user)

    return render(request, 'complaints/complaint_detail.html', {'complaint': complaint})


@login_required
def complaint_update(request, pk):
    """Admin/Warden updates complaint status."""
    if not (request.user.is_hostel_admin or request.user.is_warden):
        messages.error(request, 'Access denied.')
        return redirect('dashboard:home')

    complaint = get_object_or_404(Complaint, pk=pk)

    if request.method == 'POST':
        form = ComplaintUpdateForm(request.POST, instance=complaint)
        if form.is_valid():
            complaint = form.save(commit=False)
            if complaint.status == 'resolved' and not complaint.resolved_at:
                complaint.resolved_at = timezone.now()
            complaint.save()
            messages.success(request, f'Complaint #{complaint.pk} updated.')
            return redirect('complaints:complaint_detail', pk=complaint.pk)
    else:
        form = ComplaintUpdateForm(instance=complaint)

    return render(request, 'complaints/complaint_update.html', {
        'form': form,
        'complaint': complaint,
    })
