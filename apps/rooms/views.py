from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Room, Bed, Allocation
from .forms import RoomForm, BedForm, AllocationForm


def admin_required(view_func):
    """Decorator to restrict access to admin/warden only."""
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('accounts:login')
        if not (request.user.is_hostel_admin or request.user.is_warden):
            messages.error(request, 'Access denied. Admin/Warden only.')
            return redirect('dashboard:home')
        return view_func(request, *args, **kwargs)
    return wrapper


@login_required
def room_list(request):
    """Display all rooms with availability info."""
    rooms = Room.objects.all()

    # Filters
    floor = request.GET.get('floor')
    room_type = request.GET.get('room_type')
    availability = request.GET.get('availability')

    if floor:
        rooms = rooms.filter(floor=floor)
    if room_type:
        rooms = rooms.filter(room_type=room_type)
    if availability == 'available':
        rooms = [r for r in rooms if not r.is_full]
    elif availability == 'full':
        rooms = [r for r in rooms if r.is_full]

    floors = Room.objects.values_list('floor', flat=True).distinct().order_by('floor')

    context = {
        'rooms': rooms,
        'floors': floors,
        'selected_floor': floor,
        'selected_type': room_type,
        'selected_availability': availability,
    }
    return render(request, 'rooms/room_list.html', context)


@login_required
def room_detail(request, pk):
    """Show room details with beds and allocations."""
    room = get_object_or_404(Room, pk=pk)
    beds = room.beds.all()
    allocations = Allocation.objects.filter(bed__room=room, is_active=True).select_related('student', 'bed')

    context = {
        'room': room,
        'beds': beds,
        'allocations': allocations,
    }
    return render(request, 'rooms/room_detail.html', context)


@admin_required
def room_create(request):
    """Create a new room (admin only)."""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save()
            # Auto-create beds
            for i in range(room.total_beds):
                Bed.objects.create(
                    room=room,
                    bed_label=chr(65 + i)  # A, B, C...
                )
            messages.success(request, f'Room {room.room_number} created with {room.total_beds} beds.')
            return redirect('rooms:room_list')
    else:
        form = RoomForm()

    return render(request, 'rooms/room_form.html', {'form': form, 'title': 'Add New Room'})


@admin_required
def room_edit(request, pk):
    """Edit a room (admin only)."""
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, f'Room {room.room_number} updated.')
            return redirect('rooms:room_detail', pk=room.pk)
    else:
        form = RoomForm(instance=room)

    return render(request, 'rooms/room_form.html', {'form': form, 'title': f'Edit Room {room.room_number}'})


@admin_required
def room_delete(request, pk):
    """Delete a room (admin only)."""
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room_number = room.room_number
        room.delete()
        messages.success(request, f'Room {room_number} deleted.')
        return redirect('rooms:room_list')
    return render(request, 'rooms/room_confirm_delete.html', {'room': room})


@admin_required
def allocate_bed(request, bed_id):
    """Allocate a bed to a student (admin only)."""
    bed = get_object_or_404(Bed, pk=bed_id)

    if bed.status != 'available':
        messages.error(request, 'This bed is not available for allocation.')
        return redirect('rooms:room_detail', pk=bed.room.pk)

    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            allocation = form.save(commit=False)
            allocation.bed = bed
            allocation.allocated_by = request.user
            allocation.save()
            messages.success(request, f'Bed {bed.bed_label} in Room {bed.room.room_number} allocated to {allocation.student.get_full_name()}.')
            return redirect('rooms:room_detail', pk=bed.room.pk)
    else:
        form = AllocationForm()

    return render(request, 'rooms/allocate_bed.html', {
        'form': form,
        'bed': bed,
    })


@admin_required
def deallocate_bed(request, allocation_id):
    """Deallocate a bed (admin only)."""
    allocation = get_object_or_404(Allocation, pk=allocation_id)

    if request.method == 'POST':
        allocation.is_active = False
        allocation.end_date = timezone.now().date()
        allocation.save()
        messages.success(request, f'Bed {allocation.bed.bed_label} in Room {allocation.bed.room.room_number} has been deallocated.')
        return redirect('rooms:room_detail', pk=allocation.bed.room.pk)

    return render(request, 'rooms/deallocate_confirm.html', {'allocation': allocation})


@login_required
def my_room(request):
    """Show current room allocation for a student."""
    allocation = Allocation.objects.filter(
        student=request.user, is_active=True
    ).select_related('bed', 'bed__room').first()

    past_allocations = Allocation.objects.filter(
        student=request.user, is_active=False
    ).select_related('bed', 'bed__room').order_by('-end_date')

    return render(request, 'rooms/my_room.html', {
        'allocation': allocation,
        'past_allocations': past_allocations,
    })
