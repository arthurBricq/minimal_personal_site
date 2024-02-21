# Minimal Personal Website Creator

A minimal personal webpage creator that you can fully customize, written in python.

I use this code to generate my personal website.

## To push your code

```console
# Generate the site
python3 generate_site.py

# push to github...
git add outsite
git commit ....
git push

# Command to push the git branch
git subtree push --prefix outsite origin gh-pages
```

### Repair github pages after broken branch

If the last command did not work (*for instance, could be the case if you changed the http settings*), you can run the following two commands.

```console
git push git@github.com:arthurBricq/minimal_personal_site.git `git subtree split --prefix outsite origin gh-pages`:gh-pages --force

git subtree push --prefix outsite origin gh-pages
```

This will reset the subtree at `gh-pages` and push it again.
