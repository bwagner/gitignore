# gitignore

## Install
```console
git clone https://github.com/bwagner/gitignore.git
cd gitignore
pip install -r requirements.txt
```

## Use
```console
 Usage: make_gitignore.py [OPTIONS] [SNIPPETS]

 Concatenates gitignore-snippets found in the local directory to form a target .gitignore.
 Optionally refreshes snippets listed in gitignore-snippets.txt beforehand by downloading them.
╭─ Arguments ──────────────────────────────────────────────────────────────────────────────────╮
│   snippets      [SNIPPETS]  gitignore-snippets file name [default: gitignore-snippets.txt]   │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Options ────────────────────────────────────────────────────────────────────────────────────╮
│ --update-gitignores  -u        update .gitignores listed in SNIPPETS                         │
│ --help                         Show this message and exit.                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────╯
```
SNIPPETS is named `gitignore-snippets.txt` by default, listing gitignore-snippets which are
urls.
E.g., the `gitignore-snippets.txt` for this project contains:
```console
https://github.com/github/gitignore/blob/main/Global/JetBrains.gitignore
https://github.com/github/gitignore/blob/main/Python.gitignore
```

### To add a new snippet:
- if it is maintained in a github repo:
  - find a url where the new snippet is maintained. Candidates:
    [https://github.com/github/gitignore/tree/main/Global](https://github.com/github/gitignore/tree/main/Global)
  - append the url to `gitignore-snippets.txt`
  - run `make_gitignore.py -u`
- if it is a file you plan to maintain locally:
  - make sure its name ends in `.gitignore`
  - add it to the repo
  - run `make_gitignore.py`


### To remove a snippet:
- remove the url from `gitignore-snippets.txt` if listed
- remove the local copy of the snippet (if it is maintained
  in the repo, `git rm` it)
- run `make_gitignore.py`

## Contributing
```console
git clone https://github.com/bwagner/gitignore
cd gitignore
pip install -r requirements.txt -r dev-requirements.txt
pre-commit install
```

## TODO
