
library(tools)
rmarkdown::render_site()
all_files = list.files(paste0(getwd()),recursive = T)
toRender = all_files[file_ext(all_files) == "Rmd"]



for (files in toRender) {
    rmarkdown::render(files)
}

unlink("_site",recursive = T)
