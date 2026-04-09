from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import VisitorEntry
from .forms import VisitorEntryForm


@login_required
def visitor_list(request):
    """List visitor entries."""
    if request.user.is_hostel_admin or request.user.is_warden:
        visitors = VisitorEntry.objects.all().select_related('student')
    else:
        visitors = VisitorEntry.objects.filter(student=request.user)

    search = request.GET.get('search')
    if search:
        visitors = visitors.filter(visitor_name__icontains=search) | \
                   visitors.filter(visitor_phone__icontains=search)

    context = {
        'visitors': visitors,
        'search_query': search or '',
    }
    return render(request, 'visitors/visitor_list.html', context)


@login_required
def visitor_create(request):
    """Log a new visitor entry."""
    if request.method == 'POST':
        form = VisitorEntryForm(request.POST, user=request.user)
        if form.is_valid():
            entry = form.save(commit=False)
            if request.user.is_student:
                entry.student = request.user
            entry.logged_by = request.user
            entry.save()
            messages.success(request, f'Visitor {entry.visitor_name} logged successfully.')
            return redirect('visitors:visitor_list')
    else:
        form = VisitorEntryForm(user=request.user)

    return render(request, 'visitors/visitor_form.html', {'form': form})


@login_required
def visitor_checkout(request, pk):
    """Check out a visitor."""
    entry = get_object_or_404(VisitorEntry, pk=pk)

    if not (request.user.is_hostel_admin or request.user.is_warden or entry.student == request.user):
        messages.error(request, 'Access denied.')
        return redirect('visitors:visitor_list')

    if not entry.is_checked_out:
        entry.check_out = timezone.now()
        entry.save()
        messages.success(request, f'{entry.visitor_name} checked out successfully.')

    return redirect('visitors:visitor_list')
