from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from .models import CallingTask


def get_user_role(user):

    if user.is_superuser:
        return 'Super Admin'

    try:
        return user.profile.role

    except Exception:
        return None


@login_required
def task_list(request):

    role = get_user_role(
        request.user
    )

    # Calling Task page is for Counsellors.
    if role != 'Counsellor':
        return redirect(
            'dashboard'
        )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    page_size = request.GET.get(
        'page_size',
        '10'
    )

    if page_size not in [
        '10',
        '20',
        '50',
        '100'
    ]:
        page_size = '10'


    # -----------------------------------------------------
    # ALL TASKS BELONGING TO CURRENT COUNSELLOR
    # -----------------------------------------------------

    all_tasks = CallingTask.objects.filter(
        counsellor=request.user
    )


    # -----------------------------------------------------
    # SUMMARY
    # -----------------------------------------------------

    total_assigned = (
        all_tasks.count()
    )

    pending_count = (
        all_tasks.filter(
            status='Pending'
        ).count()
    )

    completed_count = (
        all_tasks.filter(
            status='Completed'
        ).count()
    )


    # -----------------------------------------------------
    # ACTIVE LIST
    #
    # Only pending records are shown.
    # Completed records disappear from this table.
    # -----------------------------------------------------

    tasks = (
        all_tasks
        .filter(
            status='Pending'
        )
        .order_by(
            '-assigned_date',
            '-id'
        )
    )


    # -----------------------------------------------------
    # SEARCH
    # -----------------------------------------------------

    if search:

        tasks = tasks.filter(

            Q(
                candidate_name__icontains=
                search
            )

            |

            Q(
                mobile__icontains=
                search
            )

            |

            Q(
                reg_no__icontains=
                search
            )

            |

            Q(
                reference__icontains=
                search
            )

        )


    # -----------------------------------------------------
    # PAGINATION
    # -----------------------------------------------------

    paginator = Paginator(
        tasks,
        int(page_size)
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )


    context = {


        'page_obj':
            page_obj,

        'search':
            search,

        'page_size':
            page_size,

        'total_assigned':
            total_assigned,

        'pending_count':
            pending_count,

        'completed_count':
            completed_count,

    }

    

    return render(
        request,
        'calling/task_list.html',
        context
    )