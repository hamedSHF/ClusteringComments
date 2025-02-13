# Clustering
This is a ML project which clusters comments of a given file.</br>
Topic of comments is about the reasons of droping a course.</br>
Based on a specific excel file the number of clusters have been set to *17*.</br>
 > `Note: A file with unsimilar distribution compared to the first one, may have a false output.`

# API
This is implemented by FastAPI.</br>
- Endpoints:
  - **/**: return the index.html
     - > ![Screenshot 2025-02-13 131855](https://github.com/user-attachments/assets/3f839c6e-ed68-409e-9439-365f5a567950)
  - **/uploadFile**: return the result of Clustering in JSON format
     - > ![Screenshot 2025-02-13 125822](https://github.com/user-attachments/assets/4805dd0b-bb53-4b97-b761-1eadd6301fd4)

# How to run it locally?
Move to the directory which you cloned the repo and run ```uvicorn Endpoints:main --reload ```

# How to create docker container?
Move to the directory which you cloned the repo.</br>
Then execute ```docker compose up --build ``` in your terminal to build and run the container.</br>
You can access the API in address 127.0.0.1:8000

