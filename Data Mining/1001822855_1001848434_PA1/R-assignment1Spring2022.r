library(dplyr)
library(ggplot2)

df_census <- read.csv(file = 'census1994.csv')
df_census <- subset(df_census,WorkClass!=' ?' & occupation!=' ?' & native.country!=' ?')
head(df_census,10)

#Task 1-a: Print the details of the df_data data frame (information such as number of rows,columns, name of columns, etc)
print(">>Task 1-a: Details of df_data data frame are: \n")
print(is.data.frame(df_census))
print(ncol(df_census))
print(nrow(df_census))
print(colnames(df_census))

#Task 1-b: Find the number of rows and columns in the df_data data frame.
print("\n\n>>Task 1-b: Number of rows and number of columns:")
print(dim(df_census))

#Task 1-c: Print the descriptive details (min, max, quartiles etc) for 'Age' column of the df_census
print("\n\n>>Task 1-c: Descriptive details for 'Age' column are\n")
print(summary(df_census$Age))

#Task 1-d: Print the number of unique values for 'education_num' and 'hours_per_week' columns
print("\n\n >>Task 1-d:")
# print("#####################################################")
number_unique_education <- nrow(unique(df_census[c("education.num")]))
number_unique_week <- nrow(unique(df_census[c("hours.per.week")]))

sprintf("Task 1-d: The number of unique 1 :%d", number_unique_education)
sprintf("Task 1-d: The number of unique 2 :%d", number_unique_week)


#print(df_census['education'])


#Task 2-a: Find out the sum of Captial Gain for people with education level as Bachelors and HS-Grad.
paste("Task 2-a: The sum of capital gain for education level as bachelors is and as HS-Grad is")


required1 <- subset(df_census,(education==' Bachelors'))
required2 <- subset(df_census,(education==' HS-grad'))
bachelor_sum=sum(required1['capital.gain'])
graduate_sum=sum(required2['capital.gain'])
print('The sum of capital gain for education level as bachelors is')
print(bachelor_sum)
print('The sum of capital gain for education level as HS-Grad is')
print(graduate_sum)


#Task 2-b: Find out the total number of people surveyed in months may, october and december.
#Create a new column for 'Survey_Month' by using 'Date' column
#write the code for extracting the month from the date column here

df_census$Survey_Month <- as.Date(df_census$ï..Date, format = "%m/%d/%Y")
df_census$Survey_Month <- months(df_census$Survey_Month)
# df_census
# ###############send you code here
may_mon <- subset(df_census, (Survey_Month == 'May'))
number_surveys_may <- nrow(may_mon)
october_mon <- subset(df_census, (Survey_Month == 'October'))
number_surveys_october <- nrow(october_mon)
december_mon <- subset(df_census, (Survey_Month == 'December'))
number_surveys_december <- nrow(december_mon)
sprintf("Task 2-b: The total number of surveys in may is %d, in october is %d, and in december is %d",number_surveys_may, number_surveys_october, number_surveys_december)


#Task 2-c: Let us now use multiple filtering criteria
number_surveys_september <- nrow(subset(df_census, (Survey_Month == 'September') & (WorkClass == ' Private') & Age < 50))
number_surveys_november <- nrow(subset(df_census, (Survey_Month == 'November') & (WorkClass == ' Private') & Age < 50))
sprintf("Task 2-c: The total number of surveys that meet the given conditions in september is %d and in november is %d",number_surveys_september, number_surveys_november)


#Task 2-d: Find out 3 least surveyed education categories, print their names and corresponding number of surveys for 
#periods January-June and July-December.
set_1 <- c('January','February','March','April','May','June')
set_2 <- c('July','August','September','October','November','December')
df_twod <- df_census %>% group_by(Survey_Month,education) %>% summarise(count = n())
df_param1 <- df_twod %>% filter(Survey_Month %in% set_1)
df_param2 <- df_twod %>% filter(Survey_Month %in% set_2)
order_param1 <- df_param1[order(df_param1$count),]
order_param2 <- df_param2[order(df_param2$count),]
duplicate_param1 <- order_param1[!duplicated(order_param1$education),]
duplicate_param2 <- order_param2[!duplicated(order_param2$education),]
final_param1 <- head(duplicate_param1,3)
final_param2 <- head(duplicate_param2,3)
# final_param2
print("Task 2-d: The top 3 least surveyed education categories in January-June:")
print(final_param1)
print("Task 2-d: The top 3 least surveyed education categories in July-December:")
print(final_param2)


#Task 2-e: Find out top 5 native-countries besides United-States, print their names and number of surveys belonging 
#to each.
df_task2e <- df_census %>% group_by(native.country) %>% summarise(count = n())
order_task2e <- df_task2e[order(-df_task2e$count),]
final_task2e <- order_task2e[2:6,]
print ("Task 2-e: The top 5 most surveyed native countries :")
print(final_task2e)

#Task 2-f: Find out Top-5 native-countries with the most number of samples belonging to class >50K
df_task2f <- df_census %>% group_by(native.country,class) %>% summarise(sum = sum(as.numeric(fnlwgt))) #sum(as.numeric(fnlwgt))
sub_task2f <- subset(df_task2f, (class == ' >50K'))
order_task2f <- sub_task2f[order(-sub_task2f$sum),]
final_task2f <- head(order_task2f,5)
print ("Task 2-f: The top 5 native countries with the most number of surveys with class >50K:")
print(final_task2f)




#Task 3-a: Draw a histogram for total number of surveys taken each month. Dislpay months with their corresponding 
#numbers(Eg: January is 1) 
#########################begin code for Task 3-a
print("Task 3-a")
mon <- as.numeric(as.factor(df_census$Survey_Month))
hist(mon,
main="Total survey taken each month",
xlab="Month",
ylab="Number of survey",
col="darkmagenta",
freq=FALSE
)

#Task 3-b: Draw a vertical bar chart for total number of surveys taken for each gender for each month. Display months 
#with their corresponding names.
# Remember to make the bar chart into a vertical bar chart
#########################begin code for Task 3-b
df_task3b <- df_census %>% group_by(Survey_Month,gender) %>% summarise(count = n())
ggplot(data = df_task3b, aes(x = Survey_Month, y = count, fill = gender)) + geom_bar(stat = "identity",size = 1) + ggtitle("Gender vs Month Graph")

#Task 3-c: Draw a horizontal bar chart for number of surveys taken with respect to age feature keeping the age interval as 15.
# Remember to make the bar chart into a horizontal bar chart
#########################begin code for Task 3-c
agessss_range <- c(0,15,30,45,60,75,90,105)
df_task3c <- df_census %>% group_by(cut(df_census$Age, agessss_range)) %>% summarise(sum = n())
names(df_task3c)[names(df_task3c) == 'cut(df_census$Age, agessss_range)'] <- 'agessss_range'
ggplot(df_task3c, aes(x = agessss_range, y = sum)) + geom_col() + coord_flip() + ggtitle("No. of surveys taken vs Age")


#Task 3-d: Draw a "vertical" bar chart that lists the top-5 native-countries based on the number of samples with class >50K.
# Remember to make the bar chart into a vertical bar chart
#########################begin code for Task 3-d
df_task3d <- df_census %>% group_by(native.country,class) %>% summarise(sum = n()) #sum(as.numeric(fnlwgt))
sub_task3d <- subset(df_task3d, (class == ' >50K'))
order_task3d <- sub_task3d[order(-sub_task3d$sum),]
final_task3d <- head(order_task3d,5)
final_task3d
Hama <- final_task3d$sum
Mam <- final_task3d$native.country
barplot(Hama,names.arg=Mam,xlab="Country",ylab="Number of samples",col="blue",main="Class >50k chart: Native country",border="red")

#Task 3-e: Now repeat Task 3-d based on education (again top-5)
#########################begin code for Task 3-e
df_task3e <- df_census %>% group_by(education,class) %>% summarise(sum = n()) #sum(as.numeric(fnlwgt))
sub_task3e <- subset(df_task3e, (class == ' >50K'))
order_task3e <- sub_task3e[order(-sub_task3e$sum),]
final_task3e <- head(order_task3e,5)
final_task3e
Hama <- final_task3e$sum
Mam <- final_task3e$education
barplot(Hama,names.arg=Mam,xlab="Education",ylab="Number of samples",col="black",main="Class >50k chart: Education",border="red")

#Task 3-f: Draw a scatter plot for age vs hours per week.
#########################begin code for Task 3-f
x <- df_census$Age
y <- df_census$hours.per.week
plot(x, y, main = "Age vs hour per week graph",
     xlab = "Age", ylab = "Hours per week",
     pch = 20, frame = FALSE)

#Task 3-g: Draw a line chart showing average capital gain for each education category.
# X-axis : education category, Y-axis : the avg capital gain
#########################begin code for Task 3-g
df_task3h <- df_census %>% group_by(education) %>% summarise(mean = mean(capital.gain))
df_task3h
ggplot(df_task3h, aes(x = education, y = mean, group = 1)) + geom_point() + geom_line() + ggtitle("Avg capital gains vs education")

#Task 3-h: Draw a 'horizontal' bar chart for the top-5 most common occupation. 
#########################begin code for Task 3-h
df_task3h <- df_census %>% group_by(occupation) %>% summarise(count = n())
sub_task3h <- subset(df_task3h, (count != 'NA'))
order_task3h <- sub_task3h[order(-sub_task3h$count),]
final_task3h <- head(order_task3h,5)
final_task3h
ggplot(final_task3h, aes(x = occupation, y = count)) + geom_col() + coord_flip() + ggtitle("Top 5 common occupation")

#Task 3-i: Draw a 'horizontal' bar chart for the top-5 most common workclass. 
#########################begin code for Task 3-i
df_task3i <- df_census %>% group_by(WorkClass) %>% summarise(count = n())
sub_task3i <- subset(df_task3i, (count != 'NA'))
order_task3i <- sub_task3i[order(-sub_task3i$count),]
final_task3i <- head(order_task3i,5)
final_task3i
ggplot(final_task3i, aes(x = WorkClass, y = count)) + geom_col() + coord_flip() + ggtitle("Top 5 common work class")




df_4b <- df_census %>% group_by(occupation,education) %>% summarise(Num_of_surveys = n())
ggplot(data = df_4b, aes(x = occupation, y = Num_of_surveys, fill = education)) + geom_bar(stat = "identity",size = 1) + ggtitle("Occupations for the educated")+coord_flip()
print("From graph we know that people with a bachelor's degree worked in sepciality areas")


