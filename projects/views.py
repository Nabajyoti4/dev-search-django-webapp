from django.shortcuts import render, redirect
from .models import Project, Tag, Review
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm, ReviewForm
from django.contrib import messages
from .utils import searchProjects, paginateProjects

# get all project
def projects(request):  # sourcery skip: min-max-identity
    """Return all Projects
    """
    project_list, search_query = searchProjects(request)
    custom_range, project_list = paginateProjects(request, project_list, 3)


    context = {
        'projects' : project_list,
        'search_query' : search_query,
        'custom_range' : custom_range
    }
    return render(request, 'projects/projects.html',context)


# return single poejct
def project(request, pk):
    """retrun single project based on pass id

    Args:
        pk (string): Project unique id

    Returns:
        dict : project dictonary item
    """
    project = Project.objects.get(id=pk)
    tags = project.tags.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        messages.success(request,'Your Review was succesfully submitted')


    return render(request, 'projects/single-project.html', {'project' : project, 'tags' : tags, 'form' : form})


# craete project
@login_required(login_url="login")
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('projects')

    context  = {'form' : form}
    return render(request, 'projects/project-form.html', context)


# update project
@login_required(login_url="login")
def updateProject(request, pk):
    profile = request.user.profile
    project  =  profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST, request.FILES,instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    context  = {'form' : form}
    return render(request, 'projects/project-form.html', context)


# delete project
@login_required(login_url="login")
def deleteProject(request, pk):
    profile = request.user.profile
    project  =  profile.project_set.get(id=pk)
    project.delete()
    return redirect('projects')