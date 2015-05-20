USERS = {
    'demo': 'demo'
    }
GROUPS = {
    'demo': ['group:todoers']
    }


def groupfinder(userid, request):
    # Has 3 potential returns:
    #   - None, meaning userid doesn't exist in our database
    #   - An empty list, meaning existing user but no groups
    #   - Or a list of groups for that userid
    if userid in USERS:
        return GROUPS.get(userid, [])
