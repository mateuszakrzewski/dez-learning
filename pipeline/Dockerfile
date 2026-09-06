# base Docker image that we will build on
FROM python:3.13.15

# # set up our image by installing prerequisities; pandas in this case
# RUN pip install pandas pyarrow

# copy uv binary from official uv image (multi-stage build pattern)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin

# set up the working directory inside the container
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

#Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from losk gfile (ensures reproducible builds)
RUN uv sync --locked --no-install-project
 
# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["uv", "run", "python", "pipeline.py"]

