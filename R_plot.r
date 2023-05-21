#
# Copyright 2023 Erwan Mahe (github.com/erwanM974)
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

rm(list=ls())
# ==============================================
library(ggplot2)
library(scales)
# ==============================================

# ==============================================
read_ana_report <- function(file_path) {
  # ===
  report <- read.table(file=file_path, 
                       header = FALSE, 
                       sep = ";",
                       blank.lines.skip = TRUE, 
                       fill = TRUE)
  
  names(report) <- as.matrix(report[1, ])
  report <- report[-1, ]
  report[] <- lapply(report, function(x) type.convert(as.character(x)))
  report
}
# ==============================================

# ==============================================
prepare_ana_data <- function(mydata) {
  mydata <- data.frame( mydata )
  #
  print( sprintf("number of times the timeout is exceeded : %d", 
                 nrow(mydata[mydata$verdict == "TIMEOUT",])) )
  #
  mydata$hibou_verdict[mydata$hibou_verdict=="WeakPass"]<-"Pass"
  mydata$hibou_verdict[mydata$hibou_verdict=="WeakFail"]<-"Inconc"
  mydata$hibou_verdict[mydata$hibou_verdict=="Fail"]<-"Inconc"
  mydata$hibou_verdict <- as.factor(mydata$hibou_verdict)
  #
  print( sprintf("number of ACCEPTED : %d", nrow(mydata[mydata$kind == "ACPT",])) )
  print( sprintf("number of SLICES : %d", nrow(mydata[mydata$kind == "SLIC",])) )
  print( sprintf("number of NOISE : %d", nrow(mydata[mydata$kind == "NOIS",])) )
  print( sprintf("number of CHUNKS : %d", nrow(mydata[mydata$kind == "CHNK",])) )
  #
  mydata$kind <- as.factor(mydata$kind)
  mydata$kind <- factor(mydata$kind, # Reordering group factor levels
                         levels = c("ACPT", "SLIC", "NOIS", "CHNK"))
  #
  mydata$hibou_time_median <- as.double(mydata$hibou_time_median)
  mydata$nfa_time_median <- as.double(mydata$nfa_time_median)
  mydata$trace_length <- as.integer(mydata$trace_length)
  mydata$nfa_weak_warnings_num <- as.integer(mydata$nfa_weak_warnings_num)
  mydata$nfa_strong_warnings_num <- as.integer(mydata$nfa_strong_warnings_num)
  mydata
}
# ==============================================


# ==============================================
geom_ptsize = 1
geom_stroke = 1
geom_shape = 19
# ===
draw_scatter_splot <- function(report_data,plot_title,is_log_scale,has_jitter) {
  g <- ggplot(data=report_data)
  # 
  if (has_jitter) {
    g <- g + geom_point(aes(x = trace_length, y = hibou_time_median),
                        size = geom_ptsize, 
                        stroke = geom_stroke, 
                        shape = geom_shape,
                        colour = "#1C1CD1",
                        position = position_jitter(w = 0.5, h = 0)) +
      geom_point(aes(x = trace_length, y = nfa_time_median),
                 size = geom_ptsize, 
                 stroke = geom_stroke, 
                 shape = geom_shape,
                 colour = "#117B32",
                 position = position_jitter(w = 0.5, h = 0)) 
  } else {
    g <- g + geom_point(aes(x = trace_length, y = hibou_time_median),
                        size = geom_ptsize, 
                        stroke = geom_stroke, 
                        shape = geom_shape,
                        colour = "#1C1CD1") +
      geom_point(aes(x = trace_length, y = nfa_time_median),
                 size = geom_ptsize, 
                 stroke = geom_stroke, 
                 shape = geom_shape,
                 colour = "#117B32")
  }
  #
  if (is_log_scale) {
    g <- g + scale_y_continuous(trans='log10') +
      labs(x = "trace length", y = "time (log scale)")
  } else {
    g <- g + labs(x = "trace length", y = "time")
  }
  g + ggtitle(plot_title)
}

draw_mutant_scatter_splot <- function(report_data,plot_title,is_log_scale,has_jitter,weak) {
  g <- ggplot(data=report_data)
  # 
  if (has_jitter) {
    if (weak) {
      g <- g + geom_point(aes(x = trace_length, y = nfa_time_median,colour = nfa_weak_warnings_num),
                          size = geom_ptsize, 
                          stroke = geom_stroke, 
                          shape = geom_shape,
                          position = position_jitter(w = 0.5, h = 0))
    } else {
      g <- g + geom_point(aes(x = trace_length, y = nfa_time_median,colour = nfa_strong_warnings_num),
                          size = geom_ptsize, 
                          stroke = geom_stroke, 
                          shape = geom_shape,
                          position = position_jitter(w = 0.5, h = 0)) 
    }
  } else {
    g <- g + geom_point(aes(x = trace_length, y = nfa_time_median),
                 size = geom_ptsize, 
                 stroke = geom_stroke, 
                 shape = geom_shape,
                 colour = nfa_weak_warnings_num)
  }
  #
  if (is_log_scale) {
    g <- g + scale_y_continuous(trans='log10') +
      labs(x = "trace length", y = "time (log scale)")
  } else {
    g <- g + labs(x = "trace length", y = "time")
  }
  g + ggtitle(plot_title) +
    scale_colour_gradient(low = "blue", high = "red")
}
# ==============================================

print_scatter_plot <- function(report_data,plot_title,file_name,is_log_scale,has_jitter) {
  bench_plot <- draw_scatter_splot(report_data,plot_title,is_log_scale,has_jitter)
  
  plot_file_name <- paste(gsub(" ", "_", file_name), "png", sep=".")
  
  ggsave(plot_file_name, bench_plot, width = 6000, height = 2750, units = "px")
}

print_mutant_scatter_plot <- function(report_data,plot_title,file_name,is_log_scale,has_jitter,weak) {
  bench_plot <- draw_mutant_scatter_splot(report_data,plot_title,is_log_scale,has_jitter,weak)
  
  plot_file_name <- paste(gsub(" ", "_", file_name), "png", sep=".")
  
  ggsave(plot_file_name, bench_plot, width = 6000, height = 2750, units = "px")
}



# ==============================================
treat_benchmark_data <- function(folder_path,benchmark_name,is_log_scale,has_jitter) {
  print("")
  print(benchmark_name)
  
  file_path <- paste(folder_path, benchmark_name, ".csv", sep="")

  bench_data <- read_ana_report(file_path)
  bench_data <- prepare_ana_data(bench_data)
  
  print("hibou time")
  print(summary(bench_data$hibou_time_median))
  print(sd(bench_data$hibou_time_median))
  print("")
  
  print("nfa time")
  print(summary(bench_data$nfa_time_median))
  print(sd(bench_data$nfa_time_median))
  long <- bench_data[bench_data$trace_length == 5000,]
  print("mean nfa time on long trace (5000)")
  print(mean(long$nfa_time_median))
  print("")
  
  if (is_log_scale) {
    benchmark_name <- paste(benchmark_name, "log", sep = " ")
  }
  
  acc <- bench_data[bench_data$kind == "ACPT",]
  print_scatter_plot(
    acc,
    paste(benchmark_name, "accepted traces", sep = " "),
    paste(benchmark_name, "acc", sep="_"),
    is_log_scale,has_jitter)
  
  slic <- bench_data[bench_data$kind == "SLIC",]
  print_scatter_plot(
    slic,
    paste(benchmark_name, "slices of correct behaviors", sep = " "),
    paste(benchmark_name, "slic", sep="_"),
    is_log_scale,has_jitter)
  
  nois <- bench_data[bench_data$kind == "NOIS",]
  print_mutant_scatter_plot(
    nois,
    paste(benchmark_name, "mutants via action insertion", sep = " "),
    paste(benchmark_name, "nois", sep="_"),
    is_log_scale,has_jitter,FALSE)
  
  chnk <- bench_data[bench_data$kind == "CHNK",]
  print_mutant_scatter_plot(
    chnk,
    paste(benchmark_name, "mutants via action removal", sep = " "),
    paste(benchmark_name, "chnk", sep="_"),
    is_log_scale,has_jitter,TRUE)
}
# ==============================================

treat_benchmark_data("C:/Users/ErwanMahe/rstudio_projects/nfa_ana_rv23/","abp",TRUE,TRUE)
treat_benchmark_data("C:/Users/ErwanMahe/rstudio_projects/nfa_ana_rv23/","rover",TRUE,TRUE)
treat_benchmark_data("C:/Users/ErwanMahe/rstudio_projects/nfa_ana_rv23/","smart_contract",TRUE,TRUE)




