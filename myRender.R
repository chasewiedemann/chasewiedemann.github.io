
library(tools)


toRender = shell("git status",intern = T)
toRender = trimws(gsub("\tmodified:","",toRender[grepl("\tmodified:",toRender)]))

for (files in toRender) {
  knitr::opts_chunk$set(eval = T)
  rmarkdown::render(files)
    
}


