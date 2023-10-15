class ProfileMixin:
    def get_object(self, **kwargs):
        return self.request.user
