# BugBounty

## Setup

### Make a virtual environment using conda

```
conda create -m buggybus python=3.7
```

### Install dependencies

```
pip install -r requirements.txt
```

### Create migrations

```
flask db init
```

```
flask db migrate
```

```
flask db upgrade
```

### Run the application

```
python app.py
```
