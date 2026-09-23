from flask import Flask, render_template, request
from redis import Redis
import os

app = Flask(__name__)

# Connect to the Redis cache container room 
# Docker networks allow us to call the container simply by its service name: "redis"
cache = Redis(host="redis", port=6379, socket_timeout=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/vote", methods=["POST"])
def vote():
    # Catch which button value was clicked
    voted_for = request.form.get("vote")

    try:
        # Increment the count inside the high-speed Redis cache queue
        cache.incr(voted_for)
        print(f"Success: Registered vote for {voted_for} into cache!")
    except Exception as e:
        print(f"Error: Cache room is down! Could not save vote. Details: {e}")

    return f"<h1>Thank you! Registered vote for {voted_for}.</h1><a href='/'>Go Back</a>"

if __name__ == "__main__":
    # Run the web server publicly on Port 5000
    app.run(host="0.0.0.0", port=5000)
