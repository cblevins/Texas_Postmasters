#Program to look at Texas postmasters and identify their gender

library(dplyr)
library(plyr)
library(stringr)
options(stringsAsFactors=FALSE)

pm_durations <- read.csv(file="data/PostmastersDuration.csv")
pmg<- read.csv(file="data/PostmasterGenerals_full.csv")
pmg$Date.Appointed<-as.Date(pmg$Date.Appointed, "%B %d, %Y")

#pmg <- read.csv(file="data/PostmasterGenerals.csv")
pmg$Date.Appointed<-as.Date(pmg$Date.appointed, "%m/%d/%Y") #convert into date format
pmg$Date.Ended<-as.Date(pmg$Date.Appointed) #create new column of Date format to store end dates of PMG tenures
count<-1
for (date in pmg$Name) {
  endDate<-pmg$Date.Appointed[count+1]-1
  print(endDate)
  print(class(endDate))
  #print(endDate)
  #print(pmg$Date.Ended[count])
  pmg$Date.Ended[count]<-as.Date(format(endDate, "%Y-%m-%d"))
  count<-count+1
}
write.table(pmg, file = "data/PostmasterGenerals_dates.csv", sep=",", row.names=FALSE, quote=FALSE)
#pmg$Date.Ended<-as.Date(pmg$Date.Ended, format="%Y-%m-%d", origin="1970-01-01")

