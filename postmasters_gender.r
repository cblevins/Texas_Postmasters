#Program to look at Texas postmasters and identify their gender

library(dplyr)
library(plyr)
library(stringr)
library(gender)
options(stringsAsFactors=FALSE)

PM_data <- read.csv(file="data/Texas_Postmasters.csv")
PO_data <- read.csv(file="data/Texas_PostOffices.csv")

#Look up genders of postmasters

pm_firstnames <- as.character(PM_data$First)
pm_years <- as.numeric(as.character(PM_data$Year))

#clean up first names and add a new column with cleaned name
testcase<-c(pm_firstnames[9970], pm_firstnames[358])
prefixes<-c("Mrs.", "Dr.", "Mrs", "Miss") #list of prefixes to remove

cleaning <- function(names){
  for(p in prefixes) names<-sub(p, "", names); #remove prefixes 
  names<-str_trim(names); #trim leading whitespaces
  names<-sub(" .*", "", names); #remove everything after the first space
  names<-sub("[.]", "", names); #remove periods
  return(names)
}
cleanedNames<-cleaning(pm_firstnames)
PM_data<-mutate(PM_data, CleanedFirst=cleanedNames)

#now find gender using the Gender function 
PM_data[,"Gender"]<-NA
min_age<-18
max_age<-70
pb <- txtProgressBar(min = 0, max = 30000, style = 3)
for(i in 1:length(PM_data[,"First"])){
  appt_year<-as.numeric(PM_data[i,"Year"])
  if(i%%100==0) print(i) #progress - if it's a factor of 100, print what number it is
  if(is.na(appt_year)) { #if it's a blank value for the year, then just use default years for IPUMs method
    appt_year<-as.numeric(pm_years[i]);
    birth_min<-1789;
    birth_max<-1930
  } else { #if it is not a blank value for the appointment year, then calculate the range of birth years for the person
    if((appt_year - min_age)<1789) birth_max<-1789 else birth_max<-appt_year - min_age
    if((appt_year - max_age)<1789) birth_min<-1789 else birth_min<-appt_year - max_age
  }
  gdata<-gender(cleanedNames[i], years=c(birth_min, birth_max), method="ipums") #the output from the Gender method
  PM_data[i, "Gender"]=gdata[4] #new gender data in the original dataframe
}

#refine the gender results based on Mrs. and other clues
refine_gender<-ifelse(grepl("Mrs|Miss", PM_data$First), "female", PM_data$Gender)
refine_gender[is.na(refine_gender)] = "male" #replace all NA values for gender (stuff the program couldn't identify) with a default of "male"
PM_data$RefineGender<-refine_gender #add a new column with slightly refined gender

#write out a new file
write.csv(PM_data, file="data/postmasters_gender.csv")
