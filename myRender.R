
library(tools)

all_files = list.files(paste0(getwd()),recursive = T)
toRender = all_files[file_ext(all_files) == "Rmd" & !grepl("_Template",all_files)]
unlink("_site",recursive = T)


for (files in toRender) {
    rmarkdown::render(files)
}


