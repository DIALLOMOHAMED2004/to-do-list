from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView,UpdateView, DeleteView,View
from .models import Task,NotificationSetting
from .forms import TaskForm
from django.views.generic.list import ListView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.http import HttpResponseForbidden,HttpResponse
import csv
from django.contrib import messages
from django.utils.timezone import now, timedelta

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        # Associer la tâche à l'utilisateur connecté
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'task/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        # Filtrer les tâches pour l'utilisateur connecté uniquement
        queryset = queryset.filter(user=self.request.user)
        # Identifier les tâches proches de l'échéance
        upcoming_tasks = queryset.filter(due_date__lte=now().date() + timedelta(days=2), completed=False)
        for task in upcoming_tasks:
            messages.warning(self.request, f"La tâche '{task.title}' est proche de son échéance ({task.due_date}).")
        # Appliquer les filtres si des paramètres existent
        priority = self.request.GET.get('priority')
        due_date = self.request.GET.get('due_date')

        if priority:
            queryset = queryset.filter(priority=priority)
        if due_date:
            queryset = queryset.filter(due_date=due_date)

        return queryset.distinct()




class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task/task_form.html'
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        task = form.save(commit=False)
        original_due_date = task.due_date
        new_due_date = form.cleaned_data.get('due_date')

        if original_due_date != new_due_date:
            messages.info(self.request, f"La date d'échéance de la tâche '{task.title}' a été modifiée de {original_due_date} à {new_due_date}.")

        return super().form_valid(form)

    def get_queryset(self):
        # Restreindre aux tâches de l'utilisateur connecté
        return super().get_queryset().filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task/task_confirm_delete.html'
    success_url = reverse_lazy('task-list')

    def get_queryset(self):
        # Restreindre aux tâches de l'utilisateur connecté
        return super().get_queryset().filter(user=self.request.user)


class TaskCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            task = Task.objects.get(pk=pk, user=request.user)
            task.completed = True
            task.save()
            return redirect('task-list')
        except Task.DoesNotExist:
            return HttpResponseForbidden("Vous n'avez pas l'autorisation de compléter cette tâche.")
        



class TaskExportView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        # Configurer la réponse HTTP pour un fichier CSV
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="tasks.csv"'

        # Écrire les données CSV
        writer = csv.writer(response)
        writer.writerow(['Title', 'Description', 'Due Date', 'Priority', 'Category', 'Completed'])

        # Ajouter les tâches de l'utilisateur connecté
        tasks = Task.objects.filter(user=request.user)
        for task in tasks:
            writer.writerow([task.title, task.description, task.due_date, task.priority, task.category, task.completed])

        return response
    


class TaskImportView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "Veuillez importer un fichier CSV valide.")
            return redirect('task-list')

        # Lire les données du fichier CSV
        data = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(data)

        # Ignorer la première ligne (en-tête)
        next(reader, None)

        # Ajouter les tâches pour l'utilisateur connecté
        for row in reader:
            Task.objects.create(
                title=row[0],
                description=row[1],
                due_date=row[2],
                priority=row[3],
                category=row[4],
                created_at=row[2],
                completed=(row[5].lower() == 'true'),
                user=request.user
            )
        messages.success(request, "Les tâches ont été importées avec succès.")
        return redirect('task-list')





class NotificationSettingUpdateView(LoginRequiredMixin, UpdateView):
    model = NotificationSetting
    fields = ['reminder_days']
    template_name = 'task/notification_setting_form.html'
    success_url = reverse_lazy('task-list')

    def get_object(self):
        # Récupérer ou créer les paramètres pour l'utilisateur
        obj, created = NotificationSetting.objects.get_or_create(user=self.request.user)
        return obj