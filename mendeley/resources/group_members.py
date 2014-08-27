import arrow

from mendeley.resources.profiles import LazyProfile


class GroupMembers(object):
    def __init__(self, session, id):
        self.session = session
        self.id = id

    def list(self):
        url = '/groups/%s/members' % self.id
        rsp = self.session.get(url, headers={'Accept': 'application/vnd.mendeley-membership.1+json'})

        return [GroupMember(self.session, m) for m in rsp.json()]


class GroupMember(LazyProfile):
    def __init__(self, session, member_json):
        super(GroupMember, self).__init__(session, member_json.get('profile_id'))

        self.member_json = member_json

    @property
    def joined(self):
        if 'joined' in self.member_json:
            return arrow.get(self.member_json['joined'])
        else:
            return None

    @property
    def role(self):
        return self.member_json.get('role')