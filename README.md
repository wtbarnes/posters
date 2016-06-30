# posters
Poster presentations for various conferences created using the themes provided by [latex-beamerposter](https://github.com/deselaers/latex-beamerposter). This repository makes use of a [fork of latex-beamerposter](https://github.com/wtbarnes/latex-beamerposter) that contains very minor style changes. It will otherwise remain even with the main repository.

## Installing Themes Locally
Placing packages, style files, themes, etc. in arbitrary locations is discouraged in LaTeX. Typically, TeX installations will look in a central `texmf` directory for all of these files. To install the style file, `beamerposter.sty`, and the themes in `latex-beamerposter/themes`, run
```Bash
$ ./setup_themes.sh /path/to/my/texmf/
```
This will create a set of symlinks in `/path/to/my/texmf/tex/latex/beamer/beamerposter` to the relevant themes and style file. To clean up the symlinks,
```Bash
$ ./setup_themes.sh /path/to/my/texmf/
```

## Dependencies
(Mostly) comprehensive list of package dependencies. Probably runs on Linux, probably not on Windows.

* LaTeX (e.g. [TeXLive](https://www.tug.org/texlive/), usually available through MacPorts or apt-get)
* [beamer](http://www.ctan.org/pkg/beamer) (bundled with TeXLive)
* [natbib](https://www.ctan.org/pkg/natbib?lang=en) (bundled with TeXLive)
* [latex-beamerposter](https://github.com/deselaers/latex-beamerposter), and associated dependencies (included as a submodule in this repository)
