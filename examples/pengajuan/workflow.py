def handle(action, requests, key):
    if action == 'submit':
        requests[key] = 'pending'
        return 'pending'
    if requests.get(key) != 'pending':
        raise ValueError('not pending')
    if action == 'approve':
        requests[key] = 'approved'
        return 'approved'
    if action == 'reject':
        requests[key] = 'rejected'
        return 'rejected'
    raise ValueError('unknown action')
