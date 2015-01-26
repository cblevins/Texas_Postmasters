#Program to look at Texas postmasters and identify their gender

library(dplyr)
library(plyr)
library(stringr)
options(stringsAsFactors=FALSE)

pm_durations <- read.csv(file="data/PostmastersDuration.csv")
pmg <- read.csv(file="data/PostmasterGenerals.csv")
pmg$Date.Appointed<-as.Date(pmg$Date.Appointed, "%m/%d/%Y") #convert into date format
pmg$Date.Ended<-NULL
count<-1
for (date in pmg$Date.Appointed) {
  endDate<-pmg$Date.Appointed[count+1]-1
  #print(class(endDate))
  print(endDate)
  print(pmg$Date.Ended[count])
  pmg$Date.Ended[count]=endDate
  count<-count+1
}
pmg$Date.Ended[2]-pmg$Date.Ended[3]
as.Date(pmg$Date.Ended[2], format="%m/%d/%Y")
print(as.Date(pmg$Date.Ended[2]), "%m/%d/%Y")
