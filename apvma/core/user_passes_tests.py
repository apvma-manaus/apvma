def in_resident_group(user):
    status = False
    for group in user.groups.all():
        if 'permissionários' == str(group):
            status = True
    return status
