

high = read.csv('../worldOutput-1.0-2011-09-12.csv')
medHigh  = read.csv('../worldOutput-0.99-2011-09-12.csv')
med  = read.csv('../worldOutput-0.98-2011-09-12.csv')
medLow  = read.csv('../worldOutput-0.97-2011-09-12.csv')
low  = read.csv('../worldOutput-0.96-2011-09-12.csv')

high = high$dust
high = high[500:length(high)]

medHigh = medHigh$dust
medHigh = medHigh[500:length(medHigh)]

med = med$dust
med = med[500:length(med)]

medLow = medLow$dust
medLow = medLow[500:length(medLow)]

low = low$dust
low = low[500:length(low)]

factors = c(rep(1.0,length(high)),
            rep(0.99,length(medHigh)),
            rep(0.98,length(med)),
            rep(0.97,length(medLow)),
            rep(0.96,length(low)))

dust = c(high,medHigh,med,medLow,low)


a = aov(dust ~ factors)

png(file='dustLevelsBoxplot.png')
boxplot(dust~factors,xlab='Network Reliability',ylab='Dust Levels')
dev.off()

library(gplots)
png(file='dustLevelsMeans.png')
plotmeans(dust~factors,xlab='Network Reliability',ylab='Dust Amounts')
dev.off()


#factors = factors[dust!=0]
#dust = log(dust[dust!=0])
#png(file='dustLevelsLogMeans.png')
#boxplot(dust~factors,xlab='Network Reliability',ylab='Dust Levels')
#dev.off()
