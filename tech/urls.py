from django.urls import path

from . import views
app_name = 'tech'

urlpatterns = [
          path('', views.home, name='home'),
          path('register', views.register, name='register'),
          path('ajax/jobparts/<int:jobid>', views.ajax.jobparts, name='jobparts'),
          path('ajax/addpart/<int:jobid>/<int:partid>', views.ajax.addpart, name='addpart'),
          path('ajax/updatepart/<int:jobid>/<int:jobpartid>', views.ajax.updatejobpart, name='updatejobpart'),
          path('ajax/removepart/<int:jobid>/<int:jobpartid>', views.ajax.removepart, name='removepart'),
          path('ajax/jobtimes/<int:jobid>', views.ajax.jobtimes, name='jobtimes'),
          path('ajax/starttime/<int:jobid>', views.ajax.starttime, name='starttime'),
          path('ajax/stoptime/<int:jobid>', views.ajax.stoptime, name='stoptime'),
          path('ajax/removetime/<int:jobid>/<int:timeid>', views.ajax.removetime, name='removetime'),
          path('ajax/addtimecomment/<int:jobid>/<int:timeid>', views.ajax.addtimecomment, name='addtimecomment'),
          path('ajax/updatejob/<int:jobid>', views.ajax.updatejob, name='updatejob'),
]