from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from django.db import transaction
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone

from openpyxl import Workbook

from .models import Candidate
from .forms import CandidateForm

from calling.models import CallingTask

from accounts.permissions import (
    can_view_students,
    can_manage_students,
    can_delete_students,
    can_export_students,
)


# =========================================================
# ROLE HELPER
# =========================================================

def get_user_role(user):

    if user.is_superuser:
        return 'Super Admin'

    try:
        return user.profile.role

    except Exception:
        return None


# =========================================================
# STUDENT LIST
# =========================================================

@login_required
def student_list(request):

    if not can_view_students(request.user):
        return redirect('dashboard')

    role = get_user_role(
        request.user
    )

    search = request.GET.get(
        'search',
        ''
    ).strip()

    status_filter = request.GET.get(
        'status',
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


    # =====================================================
    # BASE QUERY
    # =====================================================

    candidates = Candidate.objects.select_related(
        'counsellor'
    ).all()


    # Counsellor can see only his/her candidates.
    if role == 'Counsellor':

        candidates = candidates.filter(
            counsellor=request.user
        )


    # =====================================================
    # SEARCH
    # =====================================================

    if search:

        candidates = candidates.filter(

            Q(
                candidate_name__icontains=search
            )

            |

            Q(
                contact_no__icontains=search
            )

            |

            Q(
                guardian_name__icontains=search
            )

            |

            Q(
                location__icontains=search
            )

            |

            Q(
                other_location__icontains=search
            )

            |

            Q(
                course_interested__icontains=search
            )

            |

            Q(
                counsellor__first_name__icontains=search
            )

            |

            Q(
                counsellor__username__icontains=search
            )

        )


    if status_filter:

        candidates = candidates.filter(
            status=status_filter
        )


    # =====================================================
    # SUMMARY COUNTS
    # =====================================================

    summary_candidates = Candidate.objects.all()


    if role == 'Counsellor':

        summary_candidates = (
            summary_candidates.filter(
                counsellor=request.user
            )
        )


    total_candidates = (
        summary_candidates.count()
    )

    interested_count = (
        summary_candidates.filter(
            status='Interested'
        ).count()
    )

    waiting_count = (
        summary_candidates.filter(
            status='Yet to Confirm'
        ).count()
    )

    not_interested_count = (
        summary_candidates.filter(
            status='Non-Interested'
        ).count()
    )


    # =====================================================
    # PAGINATION
    # =====================================================

    paginator = Paginator(
        candidates,
        int(page_size)
    )

    page_number = request.GET.get(
        'page'
    )

    page_obj = paginator.get_page(
        page_number
    )


    # =====================================================
    # COUNSELLOR LIST
    # =====================================================

    counsellors = User.objects.filter(
        profile__role='Counsellor',
        is_active=True
    ).order_by(
        'first_name',
        'username'
    )


    # =====================================================
    # CALLING TASK
    # =====================================================

    calling_task = None

    calling_task_id = request.GET.get(
        'calling_task',
        ''
    ).strip()


    if calling_task_id:

        try:

            calling_task = (
                CallingTask.objects
                .select_related(
                    'counsellor',
                    'candidate'
                )
                .get(
                    pk=calling_task_id
                )
            )


            # Counsellor can open only his/her own task.
            if role == 'Counsellor':

                if (
                    calling_task.counsellor_id
                    !=
                    request.user.id
                ):

                    messages.error(
                        request,
                        'You do not have permission '
                        'to access this calling task.'
                    )

                    return redirect(
                        'calling:task_list'
                    )


            # Completed task cannot be processed again.
            if (
                calling_task.status == 'Completed'
                or
                calling_task.candidate_id
            ):

                messages.warning(
                    request,
                    'This calling task has already '
                    'been completed.'
                )

                if role == 'Counsellor':

                    return redirect(
                        'calling:task_list'
                    )

                calling_task = None


        except (
            CallingTask.DoesNotExist,
            ValueError
        ):

            messages.error(
                request,
                'Calling task not found.'
            )

            if role == 'Counsellor':

                return redirect(
                    'calling:task_list'
                )


    context = {

        'page_obj':
            page_obj,

        'search':
            search,

        'status_filter':
            status_filter,

        'page_size':
            page_size,

        'total_candidates':
            total_candidates,

        'interested_count':
            interested_count,

        'waiting_count':
            waiting_count,

        'not_interested_count':
            not_interested_count,

        'counsellors':
            counsellors,

        'calling_task':
            calling_task,

        'can_manage_students':
            can_manage_students(
                request.user
            ),

        'can_delete_students':
            can_delete_students(
                request.user
            ),

        'can_export_students':
            can_export_students(
                request.user
            ),

    }


    return render(
        request,
        'students/student_list.html',
        context
    )


# =========================================================
# ADD CANDIDATE
# =========================================================

@login_required
def add_candidate(request):

    if not can_manage_students(
        request.user
    ):

        return redirect(
            'student_list'
        )


    if request.method != 'POST':

        return redirect(
            'student_list'
        )


    role = get_user_role(
        request.user
    )


    calling_task_id = request.POST.get(
        'calling_task_id',
        ''
    ).strip()


    # =====================================================
    # CANDIDATE FROM CALLING TASK
    # =====================================================

    if calling_task_id:

        try:

            with transaction.atomic():

                task = (
                    CallingTask.objects
                    .select_for_update()
                    .select_related(
                        'counsellor',
                        'candidate'
                    )
                    .get(
                        pk=calling_task_id
                    )
                )


                # Counsellor can process only assigned task.
                if role == 'Counsellor':

                    if (
                        task.counsellor_id
                        !=
                        request.user.id
                    ):

                        messages.error(
                            request,
                            'You do not have permission '
                            'to process this calling task.'
                        )

                        return redirect(
                            'calling:task_list'
                        )


                # Prevent double Candidate creation.
                if (
                    task.status == 'Completed'
                    or
                    task.candidate_id
                ):

                    messages.warning(
                        request,
                        'This calling task has already '
                        'been completed.'
                    )

                    return redirect(
                        'calling:task_list'
                    )


                # -----------------------------------------
                # FORCE TASK VALUES
                #
                # Never trust locked browser fields.
                # -----------------------------------------

                post_data = request.POST.copy()

                post_data[
                    'counsellor'
                ] = str(
                    task.counsellor_id
                )

                post_data[
                    'candidate_name'
                ] = task.candidate_name

                post_data[
                    'contact_no'
                ] = task.mobile


                # Enquiry date is system date.
                post_data[
                    'enquiry_date'
                ] = timezone.localdate().isoformat()


                form = CandidateForm(
                    post_data
                )


                if not form.is_valid():

                    error_text = ' '.join(
                        [
                            str(error)
                            for errors
                            in form.errors.values()
                            for error
                            in errors
                        ]
                    )

                    messages.error(
                        request,
                        (
                            'Candidate could not be saved. '
                            + error_text
                        )
                    )

                    return redirect(
                        (
                            '/students/'
                            '?calling_task='
                            + str(task.id)
                        )
                    )


                candidate = form.save(
                    commit=False
                )


                # Enforce again on model instance.
                candidate.counsellor = (
                    task.counsellor
                )

                candidate.candidate_name = (
                    task.candidate_name
                )

                candidate.contact_no = (
                    task.mobile
                )

                candidate.enquiry_date = (
                    timezone.localdate()
                )

                candidate.save()


                # -----------------------------------------
                # COMPLETE CALLING TASK
                # -----------------------------------------

                task.candidate = candidate

                task.status = 'Completed'

                task.completed_at = (
                    timezone.now()
                )

                task.save(
                    update_fields=[
                        'candidate',
                        'status',
                        'completed_at',
                        'updated_at',
                    ]
                )


                messages.success(
                    request,
                    'Candidate saved and calling task '
                    'completed successfully.'
                )


        except (
            CallingTask.DoesNotExist,
            ValueError
        ):

            messages.error(
                request,
                'Calling task not found.'
            )


        if role == 'Counsellor':

            return redirect(
                'calling:task_list'
            )

        return redirect(
            'student_list'
        )


    # =====================================================
    # NORMAL MANUAL ADD CANDIDATE
    # =====================================================

    form = CandidateForm(
        request.POST
    )


    if form.is_valid():

        candidate = form.save(
            commit=False
        )


        # If Counsellor manually adds a candidate,
        # force the logged-in counsellor.
        if role == 'Counsellor':

            candidate.counsellor = (
                request.user
            )


        candidate.save()


        messages.success(
            request,
            'Candidate added successfully.'
        )


    else:

        error_text = ' '.join(
            [
                str(error)
                for errors
                in form.errors.values()
                for error
                in errors
            ]
        )

        messages.error(
            request,
            (
                'Candidate could not be saved. '
                + error_text
            )
        )


    return redirect(
        'student_list'
    )


# =========================================================
# EDIT CANDIDATE
# =========================================================

@login_required
def edit_candidate(request, pk):

    if not can_manage_students(
        request.user
    ):

        return redirect(
            'student_list'
        )


    candidate = get_object_or_404(
        Candidate,
        pk=pk
    )


    role = get_user_role(
        request.user
    )


    # Counsellor can edit only own candidates.
    if role == 'Counsellor':

        if (
            candidate.counsellor_id
            !=
            request.user.id
        ):

            messages.error(
                request,
                'You do not have permission '
                'to edit this candidate.'
            )

            return redirect(
                'student_list'
            )


    if request.method == 'POST':

        post_data = request.POST.copy()


        # Counsellor cannot transfer candidate
        # to another counsellor.
        if role == 'Counsellor':

            post_data[
                'counsellor'
            ] = str(
                request.user.id
            )


        form = CandidateForm(
            post_data,
            instance=candidate
        )


        if form.is_valid():

            form.save()

            messages.success(
                request,
                'Candidate updated successfully.'
            )

        else:

            messages.error(
                request,
                'Candidate could not be updated. '
                'Please check the entered details.'
            )


    return redirect(
        'student_list'
    )


# =========================================================
# DELETE CANDIDATE
# =========================================================

@login_required
def delete_candidate(request, pk):

    if not can_delete_students(
        request.user
    ):

        return redirect(
            'student_list'
        )


    candidate = get_object_or_404(
        Candidate,
        pk=pk
    )


    if request.method == 'POST':

        candidate.delete()

        messages.success(
            request,
            'Candidate deleted successfully.'
        )


    return redirect(
        'student_list'
    )


# =========================================================
# EXPORT CANDIDATES
# =========================================================

@login_required
def export_candidates(request):

    if not can_export_students(
        request.user
    ):

        return redirect(
            'student_list'
        )


    role = get_user_role(
        request.user
    )


    search = request.GET.get(
        'search',
        ''
    ).strip()

    status_filter = request.GET.get(
        'status',
        ''
    ).strip()


    candidates = (
        Candidate.objects
        .select_related(
            'counsellor'
        )
        .all()
    )


    if role == 'Counsellor':

        candidates = candidates.filter(
            counsellor=request.user
        )


    if search:

        candidates = candidates.filter(

            Q(
                candidate_name__icontains=search
            )

            |

            Q(
                contact_no__icontains=search
            )

            |

            Q(
                guardian_name__icontains=search
            )

            |

            Q(
                location__icontains=search
            )

            |

            Q(
                other_location__icontains=search
            )

            |

            Q(
                course_interested__icontains=search
            )

            |

            Q(
                counsellor__first_name__icontains=search
            )

            |

            Q(
                counsellor__username__icontains=search
            )

        )


    if status_filter:

        candidates = candidates.filter(
            status=status_filter
        )


    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = (
        'Candidate Records'
    )


    headers = [

        'S.No',

        'Enquiry Date',

        'Counsellor Name',

        'Candidate Name',

        'Contact No.',

        'Gender',

        'Qualification',

        'Father / Guardian Name',

        'Location',

        'Address',

        'Course Interested',

        'Family Annual Income',

        'Skill Preference',

        'Status',

        'Remark',

    ]


    worksheet.append(
        headers
    )


    for index, candidate in enumerate(
        candidates,
        start=1
    ):

        counsellor_name = ''


        if candidate.counsellor:

            counsellor_name = (
                candidate.counsellor.get_full_name()
                or
                candidate.counsellor.username
            )


        if candidate.location == 'Others':

            location = (
                candidate.other_location
            )

        else:

            location = (
                candidate.location
            )


        worksheet.append(
            [

                index,

                candidate.enquiry_date.strftime(
                    '%d-%m-%Y'
                ),

                counsellor_name,

                candidate.candidate_name,

                candidate.contact_no,

                candidate.gender,

                candidate.qualification,

                candidate.guardian_name,

                location,

                candidate.address,

                candidate.course_interested,

                (
                    candidate.family_annual_income
                    if
                    candidate.family_annual_income
                    is not None
                    else ''
                ),

                candidate.skill_preference,

                candidate.status,

                candidate.remark,

            ]
        )


    response = HttpResponse(
        content_type=(
            'application/vnd.openxmlformats-'
            'officedocument.spreadsheetml.sheet'
        )
    )


    response[
        'Content-Disposition'
    ] = (
        'attachment; '
        'filename="candidate_records.xlsx"'
    )


    workbook.save(
        response
    )


    return response