from django.contrib import admin


def tech_get_app_list(self, request):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    ordering = {
        "Jobs": 0,
        "Job parts": 1,
        "Tech schedules": 2,
        "Job times": 3,
        "Users": 4,
        "Extra Tech Info": 5,
        "Parts": 6,
        "Pay Rates": 7,
        "Skills": 8,

    }
    app_dict = self._build_app_dict(request)
    # a.sort(key=lambda x: b.index(x[0]))
    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: ordering[x['name']])

    return app_list


admin.AdminSite.get_app_list = tech_get_app_list
