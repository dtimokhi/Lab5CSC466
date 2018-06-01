data = read.csv("/home/hegbert/Desktop/FML/CSC466/Lab5CSC466/times.csv")
library(ggplot2)
library(reshape2)
dataNodes = data[c("buildTime","rankTime","nodes")]
d <- melt(dataNodes,id.vars="nodes")

ggplot(data=d,aes(x=nodes,y=value,color=variable))+
  geom_point()+
  stat_smooth()+
  labs(x="Number of Nodes",y="Time(Seconds)",title="Number of Nodes Vs. Time to Build/Rank")

dataEdges = data[c("buildTime","rankTime","edges")]
d <- melt(dataEdges,id.vars="edges")

ggplot(data=d,aes(x=edges,y=value,color=variable))+
  geom_point()+
  stat_smooth()+
  labs(x="Number of Edges",y="Time(Seconds)",title="Number of Edges Vs. Time to Build/Rank")

dataNodes = data[c("iterations","nodes")]
d <- melt(dataNodes,id.vars="nodes")

ggplot(data=d,aes(x=nodes,y=value,color=variable))+
  geom_point()+
  stat_smooth()+
  labs(x="Number of Nodes",y="Iterations",title="Number of Nodes Vs. Iterations")

dataNodes = data[c("iterations","edges")]
d <- melt(dataNodes,id.vars="edges")

ggplot(data=d,aes(x=edges,y=value,color=variable))+
  geom_point()+
  stat_smooth()+
  labs(x="Number of Edges",y="Iterations",title="Number of Edges Vs. Iterations")
