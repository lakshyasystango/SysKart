import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views.generic import RedirectView, View

from .forms import LoginForm, SignUpForm
from .models import EmployeeAttandance, EmployeeDetails


class EmployeeView(LoginRequiredMixin, View):
    template_name = "employeedetails.html"

    def get(self, request, *args, **kargs):
        return render(request, self.template_name)


class LoginView(View):
    def get(self, request, *args, **kargs):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect("employee:employeeview")
        return render(request, "login.html", {"form": form})

    def post(self, request, *args, **kargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(self.request, user)
                return redirect("employee:employeeview")
        return render(request, "login.html", {"form": form})


class LogoutView(RedirectView):
    url = "/login"

    def get(self, request, *args, **kwargs):
        logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)


class EmployeeAttandanceView(LoginRequiredMixin, View):
    template_name = "employee_attandance.html"

    def get(self, request, *args, **kwargs):
        var = {"text": None, "name": None, "total_time": 0, "todaydate": datetime.datetime.now().date()}
        emp_id = request.user.id
        today_datetime = datetime.datetime.now().strftime("%d/%m/%Y")
        vals = EmployeeAttandance.objects.filter(date=today_datetime, employee_id=emp_id)
        var["text"], var["name"] = "Sing_In", "signin"
        try:
            if vals.values("signout")[0]["signout"] == None:
                var["text"], var["name"] = "Sign_Out", "signout"

                vals = EmployeeAttandance.objects.filter(date=today_datetime, employee_id=emp_id).values(
                    "signin", "signout"
                )
                x = vals[0]["signin"].strftime("%T")
                y = datetime.datetime.now().strftime("%T")
                x_list = x.split(":")
                y_list = y.split(":")
                for e in range(len(x_list)):
                    x_list[e] = int(x_list[e])
                for e in range(len(y_list)):
                    y_list[e] = int(y_list[e])
                hou_list = (y_list[0] - x_list[0]) * 3600
                min_list = (y_list[1] - x_list[1]) * 60
                sec_list = y_list[2] - x_list[2]
                total = hou_list + min_list + sec_list
                hour = str(total // 3600)
                rem = total % 3600
                mins = rem % 60
                mins_n = str(rem // 60)
                rem_sec = str(mins % 60)
                lis_time = [hour, mins_n, rem_sec]
                new_time = ":".join(lis_time)
                var["total_time"] = new_time
            else:
                var["text"], var["name"] = "Sing_In", "signin"
                var["total_time"] = 0
        except:
            pass
        return render(request, self.template_name, {"var": var})

    def post(self, request, *args, **kargs):
        current_time = datetime.datetime.now().strftime("%T")
        emp_id = request.user.id
        today_datetime = datetime.datetime.now().strftime("%d/%m/%Y")
        var = {"text": "Sign_In", "name": "signin", "total_time": 0, "todaydate": datetime.datetime.now().date()}
        qs = EmployeeAttandance.objects.filter(employee_id=emp_id, date=today_datetime)

        if request.POST.get("btn") == "signin":
            obj = EmployeeAttandance(date=today_datetime, employee_id=emp_id, signin=current_time)
            if len(qs) >= 1:
                var["message"] = "You can't sign in twice in a day. Come again tommorow."
            else:
                obj.save()
                var["text"], var["name"] = "Sign_Out", "signout"
            return render(request, self.template_name, {"var": var})

        elif request.POST.get("btn") == "signout":
            r_id = qs[0].id
            EmployeeAttandance.objects.filter(id=r_id).update(id=r_id, signout=current_time)
            var["text"], var["name"] = "Sing_In", "signin"

            vals = EmployeeAttandance.objects.filter(date=today_datetime, employee_id=emp_id).values(
                "signin", "signout"
            )

            x = vals[0]["signin"].strftime("%T")
            y = vals[0]["signout"].strftime("%T")

            x_list = x.split(":")
            y_list = y.split(":")
            for e in range(len(x_list)):
                x_list[e] = int(x_list[e])

            for e in range(len(y_list)):
                y_list[e] = int(y_list[e])

            hou_list = (y_list[0] - x_list[0]) * 3600
            min_list = (y_list[1] - x_list[1]) * 60
            sec_list = y_list[2] - x_list[2]
            total = hou_list + min_list + sec_list
            hour = str(total // 3600)
            rem = total % 3600
            mins = rem % 60
            mins_n = str(rem // 60)
            rem_sec = str(mins % 60)
            lis_time = [hour, mins_n, rem_sec]
            new_time = ":".join(lis_time)
            var["total_time"] = new_time
            EmployeeAttandance.objects.filter(id=r_id).update(total_hours=new_time)

            return render(request, self.template_name, {"var": var})

        elif request.POST["from_date"] and request.POST["to_date"]:
            fd, td = request.POST["from_date"].split("-"), request.POST["to_date"].split("-")
            f_d = fd[2] + "/" + fd[1] + "/" + fd[0]
            t_d = td[2] + "/" + td[1] + "/" + td[0]
            var["data"] = EmployeeAttandance.objects.filter(
                employee_id=request.user.id, date__range=[f_d, t_d]
            ).values("date", "signin", "signout", "total_hours")
        return render(request, self.template_name, {"var": var})


class ProfileUpdate(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "profile_update.html")

    def post(self, request, *args, **kwargs):
        EmployeeDetails.objects.filter(id=request.user.id).update(
            email=request.POST["email"], phone_number=request.POST["phn"])
        return redirect("employee:employeeview")


class SignUpView(View):
    def get(self, request, *args, **kargs):
        form = SignUpForm()
        return render(request, "signup.html", {"form": form})

    def post(self, request, *args, **kargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, f"Account Created")
            return redirect("employee:login")
        return render(request, "login.html", {"form": form})
