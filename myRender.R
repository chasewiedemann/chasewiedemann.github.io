
library(tools)


smallRender = F

if (smallRender) {
  toRender = shell("git status",intern = T)
  toRender = trimws(gsub("\tmodified:","",toRender[grepl("\tmodified:",toRender)]))
} else{
  toRender = list.files(recursive = T)[grepl(".Rmd",list.files(recursive = T))]
}



for (files in toRender) {
  knitr::opts_chunk$set(eval = T)
  rmarkdown::render(files)
    
}


