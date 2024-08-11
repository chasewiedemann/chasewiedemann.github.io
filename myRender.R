
library(tools)
all_files = list.files(paste0(getwd()),recursive = T)
toRender = all_files[file_ext(all_files) == "Rmd"]
toRender = toRender[toRender != "index.Rmd"] ### Because Render Site will do this



for (files in toRender) {
    rmarkdown::render(files)
}


rmarkdown::render_site()