FROM r-base:4.3.1

LABEL Khaos Research Group <khaos.uma.es>

COPY LICENSE ACKNOWLEDGEMENTS /mnt/shared/

WORKDIR /usr/src/app

COPY requirements.txt ./

# Install Ubuntu packages
RUN apt-get update && apt-get install -y $(grep "^ubuntu" requirements.txt | cut -d'/' -f2) || exit 1

# Install R packages
RUN R -e "install.packages('remotes')"

## Cran repository
RUN for line in $(grep "^cran" requirements.txt); do \
        pkg=${line#*/}; pkg=${pkg%%==*}; version=${line#*==}; \
        R -e "remotes::install_version('$pkg', version = '$version', dependencies = TRUE)" || exit 1; \
    done
    
## Bioconductor repository
RUN for line in $(grep "^bioconductor" requirements.txt); do \
        pkg=${line#*/}; pkg=${pkg%%==*}; version=${line#*==}; \
        R -e "remotes::install_bioc('$version/$pkg', dependencies = TRUE)" || exit 1; \
    done

COPY . .

ENTRYPOINT ["Rscript", "--vanilla", "main.R"]