from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

from students.models import Candidate
from calling.models import CallingTask
from accounts.models import UserProfile


def get_user_role(user):

    if user.is_superuser:
        return 'Super Admin'

    try:
        return user.profile.role

    except Exception:
        return None


def login_view(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

    error = None

    if request.method == 'POST':

        username = request.POST.get(
            'username'
        )

        password = request.POST.get(
            'password'
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # A superuser created with Django's createsuperuser command
            # has no application profile by default. Create its profile
            # before the first dashboard render so navigation can resolve
            # the user's role.
            if user.is_superuser:
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={
                        'role': 'Super Admin',
                        'contact_no': '',
                    }
                )

            login(
                request,
                user
            )

            return redirect(
                'dashboard'
            )

        error = (
            'Invalid username or password.'
        )

    return render(
        request,
        'login.html',
        {
            'error': error
        }
    )


@login_required
def dashboard(request):

    role = get_user_role(
        request.user
    )

    today = timezone.localdate()


    # =====================================================
    # COUNSELLOR DASHBOARD
    # =====================================================

    if role == 'Counsellor':

        calling_tasks = (
            CallingTask.objects.filter(
                counsellor=request.user
            )
        )

        today_tasks = (
            calling_tasks.filter(
                assigned_date=today
            )
        )


        today_assigned = (
            today_tasks.count()
        )

        today_completed = (
            today_tasks.filter(
                status='Completed'
            ).count()
        )

        today_pending = (
            today_tasks.filter(
                status='Pending'
            ).count()
        )


        candidates = (
            Candidate.objects.filter(
                counsellor=request.user
            )
        )


        total_candidates = (
            candidates.count()
        )

        interested_count = (
            candidates.filter(
                status='Interested'
            ).count()
        )

        waiting_count = (
            candidates.filter(
                status='Yet to Confirm'
            ).count()
        )

        not_interested_count = (
            candidates.filter(
                status='Non-Interested'
            ).count()
        )


        context = {

            'is_counsellor':
                True,

            'current_role':
                'Counsellor',

            'today_assigned':
                today_assigned,

            'today_completed':
                today_completed,

            'today_pending':
                today_pending,

            'total_candidates':
                total_candidates,

            'interested_count':
                interested_count,

            'waiting_count':
                waiting_count,

            'not_interested_count':
                not_interested_count,

        }


        return render(
            request,
            'dashboard.html',
            context
        )


    # =====================================================
    # SUPER ADMIN / ADMIN DASHBOARD
    # =====================================================

    candidates = Candidate.objects.all()
    calling_tasks = CallingTask.objects.all()

    week_start = today - timedelta(days=6)
    weekly_candidates = {row['enquiry_date']: row['count'] for row in candidates.filter(enquiry_date__gte=week_start, enquiry_date__lte=today).values('enquiry_date').annotate(count=Count('id'))}
    weekly_assigned = {row['assigned_date']: row['count'] for row in calling_tasks.filter(assigned_date__gte=week_start, assigned_date__lte=today).values('assigned_date').annotate(count=Count('id'))}
    weekly_completed = {row['assigned_date']: row['count'] for row in calling_tasks.filter(assigned_date__gte=week_start, assigned_date__lte=today, status='Completed').values('assigned_date').annotate(count=Count('id'))}
    weekly_activity = []
    peak = 1
    for offset in range(7):
        day = week_start + timedelta(days=offset)
        activity = {
            'label': day.strftime('%a'), 'date_label': day.strftime('%d %b'),
            'candidates': weekly_candidates.get(day, 0),
            'assigned': weekly_assigned.get(day, 0),
            'completed': weekly_completed.get(day, 0),
        }
        peak = max(peak, activity['candidates'], activity['assigned'], activity['completed'])
        weekly_activity.append(activity)
    for activity in weekly_activity:
        for key in ('candidates', 'assigned', 'completed'):
            activity[f'{key}_height'] = max(4, round(activity[key] * 100 / peak)) if activity[key] else 2

    counsellors = User.objects.filter(
        is_active=True, is_superuser=False, profile__role='Counsellor'
    ).select_related('profile').order_by('first_name', 'username')
    candidate_counts = {row['counsellor_id']: row['count'] for row in candidates.filter(
        counsellor__isnull=False, enquiry_date__gte=week_start, enquiry_date__lte=today
    ).values('counsellor_id').annotate(count=Count('id'))}
    task_counts = {row['counsellor_id']: row for row in calling_tasks.filter(
        assigned_date__gte=week_start, assigned_date__lte=today
    ).values('counsellor_id').annotate(
        assigned=Count('id'), completed=Count('id', filter=Q(status='Completed')),
        pending=Count('id', filter=Q(status='Pending')),
    )}
    counsellor_summary = []
    for counsellor in counsellors:
        stats = task_counts.get(counsellor.id, {})
        counsellor_summary.append({
            'name': counsellor.get_full_name() or counsellor.username,
            'enquiries': candidate_counts.get(counsellor.id, 0),
            'assigned': stats.get('assigned', 0), 'completed': stats.get('completed', 0),
            'pending': stats.get('pending', 0),
        })

    weekly_totals = {
        'enquiries': sum(item['candidates'] for item in weekly_activity),
        'assigned': sum(item['assigned'] for item in weekly_activity),
        'completed': sum(item['completed'] for item in weekly_activity),
        'pending': calling_tasks.filter(status='Pending', assigned_date__gte=week_start, assigned_date__lte=today).count(),
    }


    context = {

        'is_counsellor':
            False,

        'current_role':
            role,

        'today': today,

        'week_start': week_start,
        'weekly_totals': weekly_totals,
        'weekly_activity': weekly_activity,
        'counsellor_summary': counsellor_summary,

    }


    return render(
        request,
        'dashboard.html',
        context
    )


def logout_view(request):

    logout(
        request
    )

    return redirect(
        'login'
    )


@login_required
def training_placeholder(request, section):
    if request.user.is_superuser:
        role = 'Super Admin'
    else:
        try:
            role = request.user.profile.role
        except Exception:
            role = None
    if role not in {'Super Admin', 'Admin', 'Trainer'}:
        return redirect('dashboard')

    sections = {
        'batches': ('Batch Management', 'Batch setup and enrollment tools will be available here in a future update.'),
        'sessions': ('Training', 'Training session planning and delivery tools are under development.'),
        'attendance': ('Attendance', 'Attendance recording and reporting are under development.'),
    }
    title, description = sections.get(section, sections['batches'])
    return render(request, 'training/placeholder.html', {
        'section': section,
        'section_title': title,
        'section_description': description,
    })
