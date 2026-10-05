def get_user_role(user):

    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return 'Super Admin'

    try:
        return user.profile.role.strip()
    except Exception:
        return None


def is_super_admin(user):
    return get_user_role(user) == 'Super Admin'


def is_admin(user):
    return get_user_role(user) == 'Admin'


def is_counsellor(user):
    return get_user_role(user) == 'Counsellor'


def is_trainer(user):
    return get_user_role(user) == 'Trainer'



# STUDENT MANAGEMENT


def can_view_students(user):

    return get_user_role(user) in [
        'Super Admin',
        'Admin',
        'Counsellor',
        'Trainer',
    ]


def can_manage_students(user):

    return get_user_role(user) in [
        'Super Admin',
        'Admin',
        'Counsellor',
    ]


def can_delete_students(user):

    return get_user_role(user) in [
        'Super Admin',
        'Admin',
    ]


def can_export_students(user):

    return get_user_role(user) in [
        'Super Admin',
        'Admin',
        'Counsellor',
        'Trainer',
    ]



# USER MANAGEMENT


def can_manage_users(user):

    return is_super_admin(user)



# FACULTY MANAGEMENT

def can_manage_faculty(user):

    role = get_user_role(user)

    return role in [
        'Super Admin',
        'Admin',
    ]



# TRAINING


def can_manage_training(user):

    role = get_user_role(user)

    return role in [
        'Super Admin',
        'Admin',
        'Trainer',
    ]


# MONITORING


def can_manage_monitoring(user):

    role = get_user_role(user)

    return role in [
        'Super Admin',
        'Admin',
        'Trainer',
    ]



# REPORTS


def can_view_reports(user):

    role = get_user_role(user)

    return role in [
        'Super Admin',
        'Admin',
        'Counsellor',
        'Trainer',
    ]