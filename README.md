# ImagiMatrix
This is a repository to consolidate all the Image related utilities in one place.

💫 **Version 0.0.1**


## Installation

Install the repository via python to your python environment

```bash
pip install git+https://github.com/amunamun07/ImagiMatrix.git@master
```

## Included in this repository

<ul>
<li>[x] Birthday Post Creator </li>
</ul>

## Birthday Post Creator

```python
from datetime import date
from hbd.post_creation import PostCreation

data = [
    {"name": "John Timilsina", "image_path": "data/john.jpg"},
    {"name": "Alice Raj Prasad Acharya", "image_path": "data/alice.jpg"},
    {"name": "Harry Rai", "image_path": "data/harry.jpg"},
    {"name": "Pizza Poudel", "image_path": "data/pizza.jpeg"},
    {"name": "Apple Gurung", "image_path": "data/apple.jpeg"},
    {"name": "laptop Shrestha", "image_path": "data/laptop.jpeg"},
]

PostCreation().create_post(data)
```
