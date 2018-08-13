## First-time contributors

Start by [forking](https://help.github.com/articles/fork-a-repo/)
the [Napari repository](https://github.com/Napari/napari).

Clone it to your local machine and change directories:
```
$ git clone https://github.com/your-username/napari.git
$ cd napari
```

Set the upstream to the base Napari repository:
```
$ git add upstream https://github.com/Napari/napari.git
```

Then installing the required dependencies:
```
$ pip install -r requirements.txt
```

And setting it up for development:
```
$ pip install -e .
```

## Creating a pull request
You can now update your master branch:
```
$ git checkout master
$ git pull upstream master
```

And create feature branches:
```
$ git checkout master -b my-feature
```

Add and commit your changed files:
```
$ git add my-file.py
$ git commit -m "my message"
```

And update your remote branch:
```
$ git push -u origin my-feature
```

Navigate to the [Napari repository](https://github.com/Napari/napari) and click
the button to create your pull request!
