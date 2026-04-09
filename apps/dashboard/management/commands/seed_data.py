"""
Management command to seed the database with sample data for demonstration.
Run: python manage.py seed_data
"""

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import CustomUser
from apps.rooms.models import Room, Bed, Allocation
from apps.fees.models import FeeStructure, Payment
from apps.complaints.models import Complaint
from apps.visitors.models import VisitorEntry
from datetime import timedelta


class Command(BaseCommand):
    help = 'Seeds the database with sample data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create admin user
        admin, created = CustomUser.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@hostelhub.com',
                'first_name': 'Admin',
                'last_name': 'User',
                'role': 'admin',
                'is_staff': True,
                'is_superuser': True,
                'phone': '9876543210',
            }
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Admin user created (admin / admin123)'))

        # Create warden
        warden, created = CustomUser.objects.get_or_create(
            username='warden',
            defaults={
                'email': 'warden@hostelhub.com',
                'first_name': 'Rajesh',
                'last_name': 'Kumar',
                'role': 'warden',
                'is_staff': True,
                'phone': '9876543211',
            }
        )
        if created:
            warden.set_password('warden123')
            warden.save()
            self.stdout.write(self.style.SUCCESS('  ✓ Warden user created (warden / warden123)'))

        # Create students
        student_data = [
            ('rahul', 'Rahul', 'Sharma', 'rahul@gmail.com', '9876500001'),
            ('priya', 'Priya', 'Patel', 'priya@gmail.com', '9876500002'),
            ('amit', 'Amit', 'Singh', 'amit@gmail.com', '9876500003'),
            ('neha', 'Neha', 'Gupta', 'neha@gmail.com', '9876500004'),
            ('vikram', 'Vikram', 'Reddy', 'vikram@gmail.com', '9876500005'),
            ('ananya', 'Ananya', 'Iyer', 'ananya@gmail.com', '9876500006'),
            ('rohan', 'Rohan', 'Mehta', 'rohan@gmail.com', '9876500007'),
            ('kavita', 'Kavita', 'Nair', 'kavita@gmail.com', '9876500008'),
        ]

        students = []
        for uname, fname, lname, email, phone in student_data:
            student, created = CustomUser.objects.get_or_create(
                username=uname,
                defaults={
                    'email': email,
                    'first_name': fname,
                    'last_name': lname,
                    'role': 'student',
                    'phone': phone,
                    'parent_phone': f'98765{random.randint(10000, 99999)}',
                    'institution': 'ABC Engineering College',
                    'address': f'{random.randint(1, 500)}, Main Street, Bangalore',
                }
            )
            if created:
                student.set_password('student123')
                student.save()
            students.append(student)

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(students)} students created (password: student123)'))

        # Create rooms
        rooms = []
        room_configs = [
            ('101', 1, 'single', 1, False, 5000),
            ('102', 1, 'double', 2, False, 4000),
            ('103', 1, 'double', 2, True, 6000),
            ('104', 1, 'triple', 3, False, 3500),
            ('201', 2, 'single', 1, True, 7000),
            ('202', 2, 'double', 2, False, 4000),
            ('203', 2, 'double', 2, True, 6000),
            ('204', 2, 'triple', 3, True, 5000),
            ('301', 3, 'single', 1, False, 5000),
            ('302', 3, 'double', 2, True, 6000),
        ]

        for rnum, floor, rtype, beds, ac, rent in room_configs:
            room, created = Room.objects.get_or_create(
                room_number=rnum,
                defaults={
                    'floor': floor,
                    'room_type': rtype,
                    'total_beds': beds,
                    'is_ac': ac,
                    'monthly_rent': rent,
                }
            )
            if created:
                for i in range(beds):
                    Bed.objects.create(room=room, bed_label=chr(65 + i))
            rooms.append(room)

        self.stdout.write(self.style.SUCCESS(f'  ✓ {len(rooms)} rooms created with beds'))

        # Allocate some students
        available_beds = list(Bed.objects.filter(status='available')[:6])
        for i, bed in enumerate(available_beds):
            if i < len(students):
                Allocation.objects.get_or_create(
                    student=students[i],
                    bed=bed,
                    defaults={
                        'start_date': timezone.now().date() - timedelta(days=random.randint(30, 180)),
                        'is_active': True,
                        'allocated_by': admin,
                    }
                )
        self.stdout.write(self.style.SUCCESS(f'  ✓ {min(len(available_beds), 6)} allocations created'))

        # Create fee structures
        fee_configs = [
            ('single', False, 5000), ('single', True, 7000),
            ('double', False, 4000), ('double', True, 6000),
            ('triple', False, 3500), ('triple', True, 5000),
        ]
        for rtype, ac, amount in fee_configs:
            FeeStructure.objects.get_or_create(
                room_type=rtype, is_ac=ac, fee_period='monthly',
                defaults={'amount': amount}
            )
        self.stdout.write(self.style.SUCCESS('  ✓ Fee structures created'))

        # Create some payments
        months = ['January 2026', 'February 2026', 'March 2026', 'April 2026']
        for student in students[:6]:
            for month in random.sample(months, random.randint(1, 3)):
                alloc = Allocation.objects.filter(student=student, is_active=True).first()
                if alloc:
                    Payment.objects.get_or_create(
                        student=student,
                        fee_month=month,
                        defaults={
                            'amount': alloc.bed.room.monthly_rent,
                            'status': random.choice(['paid', 'paid', 'paid', 'failed']),
                        }
                    )
        self.stdout.write(self.style.SUCCESS('  ✓ Sample payments created'))

        # Create complaints
        complaints_data = [
            ('plumbing', 'medium', 'Water leakage in bathroom', 'There is continuous water leakage from the bathroom tap. It has been dripping for 3 days.'),
            ('electrical', 'high', 'Fan not working', 'The ceiling fan in my room has stopped working. It makes a grinding noise when turned on.'),
            ('cleaning', 'low', 'Room not cleaned properly', 'The cleaning staff did not mop the floor today. Dust is accumulating.'),
            ('internet', 'high', 'WiFi connectivity issues', 'The WiFi has been extremely slow for the past week. Cannot attend online classes.'),
            ('furniture', 'medium', 'Broken chair', 'The study chair in my room has a broken leg and is unsafe to use.'),
            ('security', 'urgent', 'Main gate lock broken', 'The main gate lock is broken and the gate does not close properly at night.'),
            ('noise', 'low', 'Noise from adjacent room', 'There is excessive noise coming from Room 203 during late hours.'),
        ]

        for i, (cat, pri, subj, desc) in enumerate(complaints_data):
            if i < len(students):
                statuses = ['open', 'in_progress', 'resolved', 'open', 'in_progress']
                c, created = Complaint.objects.get_or_create(
                    student=students[i % len(students)],
                    subject=subj,
                    defaults={
                        'category': cat,
                        'priority': pri,
                        'description': desc,
                        'status': statuses[i % len(statuses)],
                        'resolution_notes': 'Issue has been fixed by the maintenance team.' if statuses[i % len(statuses)] == 'resolved' else '',
                        'resolved_at': timezone.now() if statuses[i % len(statuses)] == 'resolved' else None,
                    }
                )
        self.stdout.write(self.style.SUCCESS('  ✓ Sample complaints created'))

        # Create visitor entries
        visitor_data = [
            ('Mr. Sharma', '9876600001', 'parent', 'Monthly visit'),
            ('Sneha Patel', '9876600002', 'sibling', 'Birthday celebration'),
            ('Dr. Singh', '9876600003', 'guardian', 'Parent-teacher meeting'),
            ('Akash Kumar', '9876600004', 'friend', 'Study group'),
        ]
        for i, (name, phone, rel, purpose) in enumerate(visitor_data):
            if i < len(students):
                VisitorEntry.objects.get_or_create(
                    student=students[i],
                    visitor_name=name,
                    defaults={
                        'visitor_phone': phone,
                        'relation': rel,
                        'purpose': purpose,
                        'logged_by': admin,
                        'check_out': timezone.now() if i % 2 == 0 else None,
                    }
                )
        self.stdout.write(self.style.SUCCESS('  ✓ Visitor entries created'))

        self.stdout.write(self.style.SUCCESS('\n✅ Database seeded successfully!'))
        self.stdout.write(self.style.WARNING('\nLogin credentials:'))
        self.stdout.write('  Admin:   admin / admin123')
        self.stdout.write('  Warden:  warden / warden123')
        self.stdout.write('  Students: rahul, priya, amit, neha, vikram, ananya, rohan, kavita / student123')
