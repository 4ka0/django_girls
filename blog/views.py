from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.shortcuts import redirect

from .models import Post
from .forms import PostForm



def post_list(request):
    '''
    Method to display a list of posts
    '''
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    '''
    Method to display a specific post
    '''
    post = get_object_or_404(Post, pk=pk)  # Returns a 404 if the object is not found
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    '''
    Method to add a new post.
    This view is used for two purposes:
    (1) To show the new post page for the first time (to show a blank form)
    (2) To save data entered via the new post page using POST
    '''

    # Option (2), to save new post data entered by the user
    if request.method == "POST":
        form = PostForm(request.POST)
        # Check if the form is valid, i.e. if all the required fields have
        # been set and no incorrect values have been submitted.
        if form.is_valid:
            # Saves the form without saving the Post object to the database
            post = form.save(commit=False)
            # Set author as the current user
            post.author = request.user
            # Save the Post object to the database
            post.save()
            # Redirect to a detail view of the new post
            return redirect('post_detail', pk=post.pk)

    # Option (1), to show a blank form
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    '''
    Method to edit a post. Approach is similar to the above.
    '''

    # Get the post in question
    post = get_object_or_404(Post, pk=pk)

    # When saving the edited post to the database
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)

    # When showing the post to edit
    else:
        form = PostForm(instance=post)

    return render(request, 'blog/post_edit.html', {'form': form})


def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})


def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')