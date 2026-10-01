from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator


from django.http import HttpResponse
from openpyxl import Workbook
from .models import Candidate
from .forms import CandidateForm


def student_list(request):
    candidates = Candidate.objects.all()

    # SEARCH
    search = request.GET.get('search', '').strip()

    if search:
        candidates = candidates.filter(
            Q(candidate_name__icontains=search) |
            Q(contact_no__icontains=search) |
            Q(email__icontains=search) |
            Q(qualification__icontains=search)
        )

    # STATUS FILTER
    status_filter = request.GET.get('status', '')

    if status_filter:
        candidates = candidates.filter(
            status=status_filter
        )

    # SUMMARY COUNTS
    total_candidates = Candidate.objects.count()

    interested_count = Candidate.objects.filter(
        status='Interested'
    ).count()

    waiting_count = Candidate.objects.filter(
        status='Wait for Confirmation'
    ).count()

    not_interested_count = Candidate.objects.filter(
        status='Not-Interested'
    ).count()

    # PAGE SIZE
    page_size = request.GET.get('page_size', '10')

    if page_size not in ['10', '20', '50']:
        page_size = '10'

    # PAGINATION
    paginator = Paginator(
        candidates,
        int(page_size)
    )

    
    page_number = request.GET.get('page')

    page_obj = paginator.get_page(
        page_number
    )

    form = CandidateForm()

    context = {
        'page_obj': page_obj,
        'form': form,
        'search': search,
        'status_filter': status_filter,
        'page_size': page_size,
        'total_candidates': total_candidates,
        'interested_count': interested_count,
        'waiting_count': waiting_count,
        'not_interested_count': not_interested_count,
    }

    return render(
        request,
        'students/student_list.html',
        context
    )

# =====================================
# ADD CANDIDATE
# =====================================

def add_candidate(request):

    if request.method == 'POST':

        form = CandidateForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'student_list'
            )

    return redirect(
        'student_list'
    )


# =====================================
# EDIT CANDIDATE
# =====================================

def edit_candidate(request, pk):

    candidate = get_object_or_404(
        Candidate,
        pk=pk
    )

    if request.method == 'POST':

        form = CandidateForm(
            request.POST,
            instance=candidate
        )

        if form.is_valid():

            form.save()

    return redirect(
        'student_list'
    )


# =====================================
# DELETE CANDIDATE
# =====================================

def delete_candidate(request, pk):

    candidate = get_object_or_404(
        Candidate,
        pk=pk
    )

    if request.method == 'POST':

        candidate.delete()

    return redirect(
        'student_list'
    )

def export_candidates(request):

    candidates = Candidate.objects.all()

    # Apply current search
    search = request.GET.get('search', '').strip()

    if search:
        candidates = candidates.filter(
            Q(candidate_name__icontains=search) |
            Q(contact_no__icontains=search) |
            Q(email__icontains=search) |
            Q(qualification__icontains=search)
        )

    # Apply current status filter
    status_filter = request.GET.get('status', '')

    if status_filter:
        candidates = candidates.filter(
            status=status_filter
        )

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Candidates"

    # HEADINGS
    worksheet.append([
        "S.No",
        "Enquiry Date",
        "Candidate Name",
        "Contact No.",
        "Email",
        "Gender",
        "DOB",
        "Qualification",
        "Father / Guardian Name",
        "Father / Guardian Contact No.",
        "Address",
        "Status",
        "Remark",
    ])

    # DATA
    for index, candidate in enumerate(candidates, start=1):

        worksheet.append([
            index,
            candidate.enquiry_date,
            candidate.candidate_name,
            candidate.contact_no,
            candidate.email,
            candidate.gender,
            candidate.dob,
            candidate.qualification,
            candidate.guardian_name,
            candidate.guardian_contact_no,
            candidate.address,
            candidate.status,
            candidate.remark,
        ])

    response = HttpResponse(
        content_type=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )
    )

    response["Content-Disposition"] = (
        'attachment; filename="JET_SKILLS_Candidates.xlsx"'
    )

    workbook.save(response)

    return response

