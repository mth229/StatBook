Change to working directory

Installed all R files with

> Rscript -e 'options(repos = c(CRAN = "https://cloud.r-project.org")); install.packages("pak"); pak::local_install_deps()'

To install Julia files, I

> julia --project="."
> ] add Distributions, Random, Statistics

to see what is going on run

> quarto render
