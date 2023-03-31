# LOAD PACKAGES ##########################################

# # Uncomment this section to begin
library(tidyverse)
library(nflreadr)
setwd("c:/Users/justi/Desktop/Run The Sims/New Sim Project")

# 
# # LOAD DATASET ###########################################
#  # Uncomment this section to begin

pbp_df <- load_pbp (2018:2022)

write.csv(pbp_df, "Play_By_Play_2018_2022.csv")