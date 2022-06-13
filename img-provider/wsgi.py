import os
from main import app

if __name__ == "__main__":
    if not os.path.exists("imgs"):
        os.mkdir("imgs")
    
    app.run(debug=False, host="0.0.0.0", port=8081)