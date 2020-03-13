from flask import Blueprint

posts = Blueprint("posts", __name__)

@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        
        flash("Post Created", "success")
        return redirect(url_for("home"))

    return render_template("create_post.html", title = "New Post", form = form, legend = "New Post")

@posts.route("/post/<int:post_id>")
def post(post_id):
    # return the post or error page
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title = post.title, post = post)

@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
     # return the post or error page
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        # 403 for forbidden route
        abort(403)

    form = PostForm()
    
    # save the updated post to the database
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()

        flash("Post is updated", "success")
        return redirect(url_for("post", post_id = post.id))

    # populate the post form with data
    elif request.method == "GET":
        form = PostForm()
        form.title.data = post.title
        form.content.data = post.content

    return render_template("create_post.html", title = "Update Post", form = form, legend = "Update Post")

@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    # return the post or error page
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        # 403 for forbidden route
        abort(403)
    
    # remove the post from the database
    db.session.delete(post)

    # save the changes
    db.session.commit()

    flash("Post is removed", "success")
    return redirect(url_for("home"))