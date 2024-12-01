
def status_color(status):
    if status == 'active':
        return 'primary'
    elif status == 'completed':
        return 'success'
    elif status == 'pending':
        return 'warning'
    else:
        return 'secondary'