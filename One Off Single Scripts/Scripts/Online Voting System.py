from flask import Flask, render_template, request, redirect
import json

app = Flask(__name__)

# Default values for the voting form
default_voting_options = ["Option 1", "Option 2", "Option 3"]
default_voting_title = "Vote for your favorite option"
default_voting_description = "Choose the best option from the following choices:"
default_voting_id = 0

# Keep track of all the voting data in a JSON file
with open("voting_data.json", "r") as file:
    voting_data = json.load(file)


# Function to add a new voting poll to the voting_data file
def add_voting_poll(options, title, description):
    global voting_data
    voting_id = len(voting_data) + 1
    voting_data.append({"id": voting_id, "options": options, "title": title, "description": description, "votes": [0] * len(options)})
    with open("voting_data.json", "w") as file:
        json.dump(voting_data, file)
    return voting_id


# Route to create a new voting poll
@app.route("/create", methods=["GET", "POST"])
def create_voting_poll():
    global default_voting_options, default_voting_title, default_voting_description
    if request.method == "POST":
        options = request.form.getlist("option")
        title = request.form.get("title")
        description = request.form.get("description")
        voting_id = add_voting_poll(options, title, description)
        return redirect(f"/vote/{voting_id}")
    else:
        return render_template("create.html", options=default_voting_options, title=default_voting_title, description=default_voting_description)


# Route to display a voting poll and process votes
@app.route("/vote/<int:voting_id>", methods=["GET", "POST"])
def vote(voting_id):
    global voting_data
    for poll in voting_data:
        if poll["id"] == voting_id:
            options = poll["options"]
            title = poll["title"]
            description = poll["description"]
            votes = poll["votes"]
            break
    else:
        return "Voting poll not found."
    if request.method == "POST":
        selected_option = int(request.form.get("option"))
        votes[selected_option] += 1
        with open("voting_data.json", "w") as file:
            json.dump(voting_data, file)
        return redirect(f"/results/{voting_id}")
    else:
        return render_template("vote.html", options=options, title=title, description=description)


# Route to display the results of a voting poll
@app.route("/results/<int:voting_id>")
def results(voting_id):
    global voting_data
    for poll in voting_data:
        if poll["id"] == voting_id:
            options = poll["options"]
            title = poll["title"]
            description = poll["description"]
            votes = poll["votes"]
            total_votes = sum(votes)
            break
    else:
        return "Voting poll not found."
    return render_template("results.html", options=options, title=title, description=description, votes=votes, total_votes=total_votes)


if __name__ == "__main__":
    app.run(debug=True)
