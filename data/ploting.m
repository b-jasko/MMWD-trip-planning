data = xlsread('min_places2_sp');

x = data(:,2);
y = data(:,1);


figure(2);
plot(x,y, '-')
xlabel('temperature')
ylabel('satisfaction points')
set(gca, 'xDir', 'reverse')
