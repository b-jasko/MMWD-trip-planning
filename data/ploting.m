data = xlsread('max_places2_sp');

x = data(:,2);
y = data(:,1);


figure(1);
plot(x,y)
xlabel('temperature')
ylabel('satisfaction points')
set(gca, 'xDir', 'reverse')
